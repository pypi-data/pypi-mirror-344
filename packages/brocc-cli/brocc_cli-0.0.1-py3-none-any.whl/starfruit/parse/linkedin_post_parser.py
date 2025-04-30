import datetime
import json
import re
import urllib.parse
from typing import List

from bs4 import BeautifulSoup, Tag
from dateutil.relativedelta import relativedelta
from pydantic import ValidationError

from starfruit.internal.logger import get_logger
from starfruit.parse.base_parser import BaseParser
from starfruit.parse.id_from_url import id_from_url
from starfruit.tasks.task_item import ParseResult, ProcessingItem

logger = get_logger(__name__)


def _parse_count(text: str | None) -> int | None:
    """Helper to parse potentially comma-separated number strings into integers."""
    if not text:
        return None
    try:
        # Remove commas and convert to int
        return int(re.sub(r"[\s,]+", "", text))
    except (ValueError, TypeError):
        # Log parsing failure only if it happens
        logger.warning(f"Could not parse count: '{text}'")
        return None


def _parse_relative_time(time_str: str) -> datetime.datetime | None:
    """Parses relative time strings like '1h', '2d', '3w' into approximate datetimes."""
    if not time_str or not isinstance(time_str, str):
        return None

    # Add $ anchor to ensure the whole string matches the pattern
    match = re.match(r"^(\d+)([hdwmy])$", time_str.strip())
    if not match:
        # Log pattern failure
        logger.warning(f"Could not match relative time pattern in: '{time_str}'")
        return None

    value = int(match.group(1))
    unit = match.group(2)

    now = datetime.datetime.now(datetime.timezone.utc)
    delta = None

    if unit == "h":
        delta = relativedelta(hours=value)
    elif unit == "d":
        delta = relativedelta(days=value)
    elif unit == "w":
        delta = relativedelta(weeks=value)
    elif unit == "m":  # Assuming 'm' is months, could be minutes but less likely for posts
        delta = relativedelta(months=value)
    elif unit == "y":
        delta = relativedelta(years=value)

    if delta:
        approx_time = now - delta
        # Do not log successful parsing (happy path)
        return approx_time
    else:
        logger.warning(f"Unknown relative time unit '{unit}' in '{time_str}'")
        return None


class LinkedInPostParser(BaseParser):
    """
    Parses a LinkedIn post page (activity URL) into a single item.
    """

    # Pattern for LinkedIn post URLs (e.g., https://www.linkedin.com/posts/duolingo_activity-id)
    LINKEDIN_POST_URL_PATTERNS: List[str] = [
        r"https://(?:www\.)?linkedin\.com/posts/[^/]+_activity-(\d+)-[^/]+/?",
        r"https://(?:www\.)?linkedin\.com/posts/activity-(\d+)-[^/]+/?",  # Simplified pattern
        r"https://(?:www\.)?linkedin\.com/feed/update/urn:li:activity:\d+/?",  # URN pattern
        r"https://(?:www\.)?linkedin\.com/feed/update/urn:li:ugcPost:\d+/?",  # UGC Post URN pattern
        r"https://(?:www\.)?linkedin\.com/feed/?$",
        r"https://(?:www\.)?linkedin\.com/in/[^/]+/?$",  # Profile pages
        r"https://(?:www\.)?linkedin\.com/in/[^/]+/recent-activity/[^/]+/?$",  # Profile activity pages (added)
        # TODO: bespoke profile parser
    ]

    def __init__(self):
        super().__init__(url_patterns=self.LINKEDIN_POST_URL_PATTERNS)

    def _extract_post_data(self, post_element: Tag, base_url: str) -> dict | None:
        """Extracts the main post content from a single post element."""
        # Use logger.info only if absolutely necessary for context, avoid otherwise.

        # --- Get Post URN for better logging/ID --- (NEW)
        post_urn = post_element.get("data-urn", "unknown_urn")

        # --- Reset Placeholders ---
        author_name = "Unknown Author"
        author_url = None
        post_text = None
        timestamp_dt = None
        media = []
        metrics = {}
        # --- End Reset ---

        # --- IMPORTANT: All selectors now run relative to post_element --- (MODIFIED)

        # Author
        actor_link_selector = "a.update-components-actor__meta-link"
        actor_link_tag = post_element.select_one(actor_link_selector)
        if isinstance(actor_link_tag, Tag):
            # Check for "Promoted" text *before* extracting other author details
            description_span = actor_link_tag.select_one(
                '.update-components-actor__description span[aria-hidden="true"]'
            )
            if description_span and "Promoted" in description_span.get_text(strip=True):
                logger.debug(f"Skipping promoted post: {post_urn}")
                return None  # Skip this post element entirely

            raw_author_url = actor_link_tag.get("href")
            if isinstance(raw_author_url, str):
                author_url = urllib.parse.urljoin(base_url, raw_author_url)

            author_name_selector = '.update-components-actor__title span[aria-hidden="true"]'
            author_name_span = actor_link_tag.select_one(author_name_selector)
            if author_name_span:
                author_name = author_name_span.get_text(strip=True) or author_name
            else:
                author_name = actor_link_tag.get_text(separator=" ", strip=True) or author_name
                logger.debug(
                    f"Author name span not found within '{actor_link_selector}', used link text for {post_urn}."
                )
        else:
            logger.warning(
                f"Could not find primary actor link using '{actor_link_selector}' in post {post_urn} on {base_url}"
            )

        # Timestamp
        timestamp_text_selector = (
            '.update-components-actor__sub-description span[aria-hidden="true"]'
        )
        # Use post_element.select_one
        timestamp_text_element = post_element.select_one(timestamp_text_selector)
        if timestamp_text_element:
            full_text = timestamp_text_element.get_text(strip=True)
            relative_time_match = re.match(r"^(\d+[hdwmy])", full_text)
            if relative_time_match:
                relative_time_str = relative_time_match.group(1)
                timestamp_dt = _parse_relative_time(relative_time_str)

        # Text
        text_selector = ".feed-shared-update-v2__description .update-components-text"
        # Use post_element.select_one
        text_container = post_element.select_one(text_selector)
        if text_container:
            post_text = text_container.get_text(separator="\n", strip=True)
        else:
            show_more_selector = ".feed-shared-inline-show-more-text"
            # Use post_element.select_one
            show_more_container = post_element.select_one(show_more_selector)
            if show_more_container:
                post_text = show_more_container.get_text(separator="\n", strip=True)

        # Media (Images and Video Posters)
        processed_media_urls = set()

        # 1. Look for images
        image_selectors = [
            "img.update-components-image__image",
            "div.update-components-update-v2__commentary img",
        ]
        for selector in image_selectors:
            image_elements = post_element.select(selector)
            for img_tag in image_elements:
                img_src_candidate = (
                    img_tag.get("data-sources")
                    or img_tag.get("data-delayed-url")
                    or img_tag.get("src")
                )
                img_src = None

                if isinstance(img_src_candidate, str) and img_src_candidate.strip().startswith("["):
                    try:
                        sources = json.loads(img_src_candidate)
                        if sources and isinstance(sources, list) and sources[0].get("src"):
                            img_src = sources[0]["src"]
                    except json.JSONDecodeError:
                        logger.warning(
                            f"Failed to parse JSON from data-sources in {post_urn} on {base_url}: {img_src_candidate[:100]}..."
                        )
                        img_src = None

                if img_src is None and isinstance(img_src_candidate, str):
                    img_src = img_src_candidate

                if isinstance(img_src, str):
                    if not img_src.startswith("data:"):
                        resolved_media_url = urllib.parse.urljoin(base_url, img_src)
                        if resolved_media_url not in processed_media_urls:
                            media.append(resolved_media_url)
                            processed_media_urls.add(resolved_media_url)

        # 2. Look for video posters
        video_selector = ".feed-shared-linkedin-video video"
        video_elements = post_element.select(video_selector)
        for video_tag in video_elements:
            poster_url = video_tag.get("poster")
            if isinstance(poster_url, str) and not poster_url.startswith("data:"):
                resolved_poster_url = urllib.parse.urljoin(base_url, poster_url)
                if resolved_poster_url not in processed_media_urls:
                    media.append(resolved_poster_url)
                    processed_media_urls.add(resolved_poster_url)

        # Metrics
        likes_selector = (
            'button[aria-label*="reaction"] .social-details-social-counts__reactions-count'
        )
        # Use post_element.select_one
        likes_element = post_element.select_one(likes_selector)
        if likes_element:
            likes_text = likes_element.get_text(strip=True)
            metrics["likes"] = _parse_count(likes_text)

        comments_selector = "button.social-details-social-counts__comments"
        # Use post_element.select_one
        comments_button = post_element.select_one(comments_selector)
        if comments_button:
            comments_text = comments_button.get_text(separator=" ", strip=True)
            match = re.search(
                r"(\d[\d,\s]*)\s*(comment|reply|answer)", comments_text, re.IGNORECASE
            )
            if match:
                extracted_count_text = match.group(1).strip()
                metrics["comments"] = _parse_count(extracted_count_text)

        # --- Derive URL and ID --- (MODIFIED)
        # Try to find a permalink within the post element
        # Attempting a different selector based on timestamp link structure (MODIFIED)
        permalink_selector = (
            'a.update-components-actor__sub-description-link[href*="urn:li:activity:"]'
            # Also check for ugcPost permalinks often found here
            ', a.update-components-actor__sub-description-link[href*="urn:li:ugcPost:"]'
        )
        permalink_tag = post_element.select_one(permalink_selector)
        post_url = base_url  # Fallback to base_url initially
        constructed_url = None  # Variable for constructed URL

        # Check if tag exists before getting attribute
        if permalink_tag:
            href_value = permalink_tag.get("href")
            if isinstance(href_value, str):
                if href_value.startswith("/feed/update/urn:li:activity:") or href_value.startswith(
                    "/feed/update/urn:li:ugcPost:"
                ):
                    post_url = urllib.parse.urljoin(base_url, href_value)
                else:
                    pass  # Keep post_url as base_url (will try construction next)
            else:
                pass  # Keep post_url as base_url (will try construction next)

        # --- If selector failed or didn't yield a valid URL, try constructing from URN --- (NEW)
        if post_url == base_url and post_urn != "unknown_urn":
            constructed_url = f"https://www.linkedin.com/feed/update/{post_urn}/"
            if any(
                re.match(pattern, constructed_url) for pattern in self.LINKEDIN_POST_URL_PATTERNS
            ):
                post_url = constructed_url
            else:
                logger.warning(
                    f"[{post_urn}] Constructed URL '{constructed_url}' does not match known patterns, falling back to base URL."
                )
                # Keep post_url as base_url

        post_id = id_from_url(post_url)

        # --- Final Checks ---
        if not post_text:
            logger.warning(f"No post text content found for post {post_urn} on {base_url}")
            # Continue processing other posts, just return None for this one
            return None

        return {
            "id": post_id,  # Use derived ID
            "url": post_url,  # Use derived URL
            "source_url": base_url,  # Keep original feed/page URL as source
            "text": post_text,
            "author_name": author_name,
            "author_url": author_url,
            "title": None,  # no title for linkedin posts
            "created_at": timestamp_dt,
            "media": media if media else None,
            "metrics": metrics if metrics else None,
            "additional_metadata": {"post_urn": post_urn},  # Add URN as metadata
        }

    def _parse_page(self, html: str, url: str) -> List[ParseResult]:
        soup = BeautifulSoup(html, "html.parser")
        # Selector for potential post containers (divs with specific data-urn prefixes)
        post_container_selector = (
            "div[data-urn^='urn:li:share:'], "  # Shares
            "div[data-urn^='urn:li:activity:'], "  # Activities (posts, reactions, etc.)
            "div[data-urn^='urn:li:ugcPost:']"  # User Generated Content Posts
        )

        post_elements = soup.select(post_container_selector)
        results: List[ParseResult] = []

        if not post_elements:
            logger.warning(
                f"No potential post elements found using selector '{post_container_selector}' in {url}"
            )
            # Try extracting data from the soup directly as a fallback (original behavior)
            post_data = self._extract_post_data(soup, url)  # Call with soup if no elements found
            if post_data:
                logger.info(f"Falling back to parsing the whole page as a single item for {url}")
                try:
                    processing_item = ProcessingItem.model_validate(post_data)
                    results.append(ParseResult(status="ready_to_embed", data=processing_item))
                except (ValidationError, ValueError) as e:
                    error_msg = f"Failed validation (fallback parse) for {url}: {e}"
                    logger.warning(error_msg, exc_info=True)
                    results.append(ParseResult(status="failed", error=error_msg))
                except Exception as e:
                    logger.error(
                        f"Unexpected error during fallback final processing for {url}: {e}",
                        exc_info=True,
                    )
                    results.append(ParseResult(status="failed", error=f"Unexpected error: {e}"))
            else:
                return [
                    ParseResult(
                        status="failed", error="No post elements found and fallback parse failed"
                    )
                ]

        else:
            logger.info(f"Found {len(post_elements)} potential post elements in {url}")
            for post_element in post_elements:
                # Pass the individual post element Tag and the original URL (as base)
                post_data = self._extract_post_data(post_element, url)

                if not post_data:
                    # _extract_post_data already logs warnings if needed
                    # Just continue to the next element
                    continue

                try:
                    processing_item = ProcessingItem.model_validate(post_data)
                    results.append(ParseResult(status="ready_to_embed", data=processing_item))
                except (ValidationError, ValueError) as e:
                    post_urn = post_element.get("data-urn", "unknown_urn")
                    error_msg = f"Failed to validate ProcessingItem for LinkedIn post element {post_urn} on {url}: {e}"
                    logger.warning(error_msg, exc_info=True)
                    # Pass data=None for failed results (Fixes Linter Error)
                    results.append(ParseResult(status="failed", error=error_msg, data=None))
                except Exception as e:
                    post_urn = post_element.get("data-urn", "unknown_urn")
                    logger.error(
                        f"Unexpected error during final processing for element {post_urn} on {url}: {e}",
                        exc_info=True,
                    )
                    # Pass data=None for failed results (Fixes Linter Error)
                    results.append(
                        ParseResult(status="failed", error=f"Unexpected error: {e}", data=None)
                    )

        if not results:
            logger.warning(f"Parsing completed for {url}, but no valid items were extracted.")
            return [ParseResult(status="failed", error="No valid items extracted")]

        return results
