import datetime
from datetime import timezone
from typing import List

from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString
from pydantic import ValidationError

from starfruit.internal.logger import get_logger
from starfruit.parse.base_parser import BaseParser
from starfruit.parse.id_from_url import id_from_url
from starfruit.parse.twitter_utils import (
    DEBUG,
    extract_media,
    extract_metrics,
    extract_quoted_tweet,
    extract_tweet_metadata,
    extract_tweet_text,
    extract_user,
)
from starfruit.tasks.task_item import ParseResult, ProcessingItem

logger = get_logger(__name__)


# Helper to format media URLs as Markdown images
def _format_media_as_markdown(media_list: List[str]) -> str:
    if not media_list:
        return ""
    markdown_images = [f"![]({url})" for url in media_list]
    # Add newline before and after the block of images
    return "\n" + "\n".join(markdown_images) + "\n"


class TwitterThreadParser(BaseParser):
    """
    Parses a Twitter thread page (a single status URL) into a single item,
    combining text from the main author's tweets in the thread.
    """

    # Pattern for individual tweet/status URLs
    TWITTER_THREAD_URL_PATTERNS: List[str] = [r"https://(?:www\.)?x\.com/[^/]+/status/\d+/?"]

    def __init__(self):
        super().__init__(url_patterns=self.TWITTER_THREAD_URL_PATTERNS)

    def _parse_single_tweet_article(self, item: Tag) -> dict | None:
        """Parses a single <article> tag into a dictionary, similar to feed parser but simpler."""
        try:
            user_info = extract_user(item)
            content = extract_tweet_text(item)
            timestamp_str, url = extract_tweet_metadata(item)
            media = extract_media(item)
            metrics = extract_metrics(item)
            quoted_tweet = extract_quoted_tweet(item)

            if not ((user_info.get("url") or user_info.get("name")) and (timestamp_str or url)):
                if DEBUG:
                    logger.debug("Skipping item due to missing user/timestamp/URL.")
                return None

            timestamp_dt: datetime.datetime | None = None
            if timestamp_str:
                try:
                    timestamp_dt = datetime.datetime.fromisoformat(timestamp_str).astimezone(
                        timezone.utc
                    )
                except (ValueError, TypeError):
                    logger.warning(f"Could not parse timestamp: {timestamp_str}", exc_info=True)

            return {
                "id": id_from_url(url) if url else None,
                "url": url,
                "text": content or "",
                "author_name": user_info.get("name"),
                "author_url": user_info.get("url"),
                "created_at": timestamp_dt,
                "media": media if media else [],  # Ensure list
                "metrics": metrics if metrics else {},  # Ensure dict
                "quoted_tweet": quoted_tweet,
            }
        except Exception as e:
            logger.warning(f"Error parsing individual tweet article: {e}", exc_info=True)
            return None

    def _parse_page(self, html: str, url: str) -> List[ParseResult]:
        soup = BeautifulSoup(html, "html.parser")
        tweet_articles = soup.select('article[data-testid="tweet"]')

        if not tweet_articles:
            logger.warning(f"No tweet articles found on page: {url}")
            return [ParseResult(status="failed", error="No tweet articles found")]

        parsed_tweets = []
        for article in tweet_articles:
            # Find the tweet text element within the article first
            tweet_text_el = article.select_one('[data-testid="tweetText"]')
            if isinstance(tweet_text_el, Tag):
                for br in tweet_text_el.find_all("br"):
                    if isinstance(br, Tag):
                        # Replace <br> with a unique placeholder string IN THE SOUP
                        br.replace_with(NavigableString(" __NEWLINE__ "))

            parsed = self._parse_single_tweet_article(article)
            if parsed and parsed.get("url") and parsed.get("author_url"):
                # Replace placeholder back to \n AFTER text extraction
                if parsed.get("text"):
                    parsed["text"] = parsed["text"].replace("__NEWLINE__", "\n")
                parsed_tweets.append(parsed)

        if not parsed_tweets:
            logger.warning(f"No valid tweets could be parsed from articles on page: {url}")
            return [ParseResult(status="failed", error="No valid tweets parsed")]

        # Identify the source tweet (matching the input URL)
        source_tweet = None
        for tweet in parsed_tweets:
            # Normalize URLs slightly for comparison (remove trailing slash)
            if tweet.get("url") and tweet["url"].rstrip("/") == url.rstrip("/"):
                source_tweet = tweet
                break

        if not source_tweet:
            logger.warning(f"Source tweet matching URL {url} not found among parsed tweets.")
            # Optionally, take the *first* tweet as a fallback source?
            # source_tweet = parsed_tweets[0] # Let's error out for now
            return [ParseResult(status="failed", error="Source tweet not found")]

        source_author_url = source_tweet.get("author_url")
        if not source_author_url:
            logger.warning(f"Source tweet {url} has no author URL.")
            return [ParseResult(status="failed", error="Source tweet missing author URL")]

        # Filter tweets by the source author and maintain order
        thread_tweets = [
            tweet for tweet in parsed_tweets if tweet.get("author_url") == source_author_url
        ]

        if not thread_tweets:
            # This shouldn't happen if source_tweet was found, but safety check
            logger.error(
                f"Logic error: thread_tweets list is empty after filtering for author {source_author_url}"
            )
            return [ParseResult(status="failed", error="Internal error filtering thread tweets")]

        # Combine text and inline media
        combined_parts = []
        for _i, tweet in enumerate(thread_tweets):
            text_part = tweet.get("text", "")
            # Escape actual newline characters (including those from <br>) for markdown compatibility
            text_part = text_part.replace("\n", "\\n")

            media_part = _format_media_as_markdown(tweet.get("media", []))
            quoted_tweet_data = tweet.get("quoted_tweet")

            if quoted_tweet_data:
                quoted_text = quoted_tweet_data.get("text", "")
                if quoted_text:
                    # Escape actual newline characters in quoted text as well
                    quoted_text = quoted_text.replace("\n", "\\n")
                    # Format as a markdown blockquote, joining lines with newline + '> '
                    # Use splitlines() on the *already escaped* quoted_text
                    lines = quoted_text.split("\\n")
                    formatted_quote = "> " + "\n> ".join(lines)
                    # Combine main text (already escaped) with the formatted quote
                    text_part = f"{text_part}\\n\\n{formatted_quote}"

            combined_parts.append(text_part + media_part)

        # Join parts with double newlines
        combined_text = "\n\n".join(combined_parts).strip()

        # Construct the final ProcessingItem based on the source tweet
        final_data = {
            "id": source_tweet.get("id"),
            "url": url,  # Use the canonical input URL
            "source_url": url,
            "text": combined_text,
            "author_name": source_tweet.get("author_name"),
            "author_url": source_tweet.get("author_url"),
            "title": None,  # No specific title for threads
            "created_at": source_tweet.get("created_at"),
            "media": None,  # Media is now embedded in text
            "metrics": source_tweet.get("metrics"),
            "additional_metadata": None,  # Could add e.g., thread_tweet_count
        }

        try:
            processing_item = ProcessingItem.model_validate(final_data)
            return [ParseResult(status="ready_to_embed", data=processing_item)]
        except (ValidationError, ValueError) as e:
            error_msg = f"Failed to validate final ProcessingItem for thread {url}: {e}"
            logger.warning(error_msg)
            return [ParseResult(status="failed", error=error_msg)]
