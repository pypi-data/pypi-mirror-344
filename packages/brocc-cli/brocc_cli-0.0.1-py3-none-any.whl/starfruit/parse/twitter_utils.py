import re
from typing import Dict, List, Optional, Set, Tuple, TypedDict

from bs4 import Tag

from starfruit.internal.logger import get_logger

logger = get_logger(__name__)
DEBUG = False


class TwitterUser(TypedDict, total=False):
    name: Optional[str]
    url: Optional[str]


def _parse_metric_string(metric_str: str) -> int:
    """Converts metric strings like '1.2K', '5M', '1,234' to integers."""
    metric_str = metric_str.strip().replace(",", "")
    multiplier = 1
    if metric_str.lower().endswith("k"):
        multiplier = 1_000
        metric_str = metric_str[:-1]
    elif metric_str.lower().endswith("m"):
        multiplier = 1_000_000
        metric_str = metric_str[:-1]

    try:
        # Handle floats like '1.2' before converting to int
        num = float(metric_str)
        return int(num * multiplier)
    except ValueError:
        logger.warning(f"Could not parse metric string: '{metric_str}'", exc_info=True)
        return 0


def extract_user(element: Tag) -> TwitterUser:
    user: TwitterUser = {
        "name": None,
        "url": None,
    }
    user_name_section = element.select_one('[data-testid="User-Name"]')
    if not user_name_section:
        if DEBUG:
            print("Could not find User-Name section in tweet. Trying fallback.")
        # Try a fallback using common link structure near the top
        user_link = element.select_one('div > div > div > a[role="link"]')
        if isinstance(user_link, Tag):
            href = user_link.get("href")
            # Check if href looks like a user profile link or status link
            if href and isinstance(href, str) and href.startswith("/"):
                if "/status/" not in href:  # Likely a profile link
                    user["url"] = f"https://x.com{href}"
                    if DEBUG:
                        print(f"Found user URL via fallback profile link: {user['url']}")
                    # Attempt to get name from within the link
                    spans = user_link.select("span")
                    if len(spans) >= 1:
                        potential_name = spans[0].get_text(strip=True)
                        # Basic check if it looks like a name (not handle/timestamp)
                        if potential_name and not potential_name.startswith("@"):
                            user["name"] = potential_name
                            if DEBUG:
                                print(f"Found user name via fallback: {user['name']}")
                elif (
                    "/status/" in href
                ):  # It's a status link, try to extract name/handle from spans
                    spans = user_link.select("span")
                    if len(spans) >= 2:
                        potential_name = spans[0].get_text(strip=True)
                        potential_handle_el = spans[-1]
                        if isinstance(potential_handle_el, Tag):
                            potential_handle_text = potential_handle_el.get_text(strip=True)
                            if potential_handle_text.startswith("@"):
                                user["name"] = potential_name
                                handle = potential_handle_text.lstrip("@")
                                user["url"] = f"https://x.com/{handle}"  # Construct URL from handle
                                if DEBUG:
                                    print(
                                        f"Found user info via fallback (status link): {user['name']} ({user['url']})"
                                    )

        return user  # Return whatever was found, might be partially filled

    # --- Name Extraction (Primary Method) ---
    name_container = user_name_section.select_one(
        'a[role="link"] > div[dir="ltr"], div[dir="ltr"] > span'
    )
    if isinstance(name_container, Tag):
        full_name_text = name_container.get_text(separator=" ", strip=True)
        cleaned_name = (
            full_name_text.replace("Verified account", "").replace("follows you", "").strip()
        )
        user["name"] = " ".join(cleaned_name.split())
        if DEBUG:
            print(f"Extracted Name: '{user['name']}'")

    # --- URL Extraction (Primary Method) ---
    # Find handle text (@...) to construct the URL
    handle_text_element = user_name_section.find(
        lambda tag: isinstance(tag, Tag)
        and tag.name == "span"
        and bool(tag.get_text(strip=True).startswith("@"))
    )

    if isinstance(handle_text_element, Tag):
        handle_text_str = str(handle_text_element.get_text(strip=True)).strip()
        if handle_text_str.startswith("@"):
            handle = handle_text_str.lstrip("@")
            user["url"] = f"https://x.com/{handle}"  # Construct URL
            if DEBUG:
                print(f"Constructed URL from handle: {user['url']}")
    else:
        # Fallback within User-Name section: check the main link's href
        main_link = user_name_section.select_one('a[role="link"][href^="/"]')
        if isinstance(main_link, Tag):
            href = main_link.get("href")
            # Ensure it's a profile link, not a status link
            if href and isinstance(href, str) and "/status/" not in href:
                user["url"] = f"https://x.com{href}"
                if DEBUG:
                    print(f"Found user URL via main link href: {user['url']}")
            else:
                if DEBUG:
                    print("Main link in User-Name was not a profile link.")
        else:
            if DEBUG:
                print("Could not find handle span or suitable profile link in User-Name section.")

    return user


def extract_tweet_text(element: Tag) -> str:
    """Extract and format tweet text content."""
    tweet_text_element = element.select_one('[data-testid="tweetText"]')
    if not isinstance(tweet_text_element, Tag):
        if DEBUG:
            print("No tweet text element found in tweet")
        return ""

    # Get all links to correctly format them
    links = []
    for a_tag in tweet_text_element.select("a"):
        # Ensure a_tag is a Tag before proceeding
        if not isinstance(a_tag, Tag):
            continue

        href_val = a_tag.get("href", "")
        link_text = a_tag.get_text().strip()
        is_user_mention = False
        is_hash_cash_tag = False
        is_external_link = False

        # Check if it's a user handle link (starts with /, no /status/, text starts with @)
        if (
            href_val
            and isinstance(href_val, str)
            and href_val.startswith("/")
            and not href_val.startswith(
                ("/search", "/i/", "/settings")
            )  # Exclude known non-profile paths
            and "/status/" not in href_val
            and link_text.startswith("@")
        ):
            is_user_mention = True
            full_url = f"https://x.com{href_val}"
            links.append((link_text, full_url))
            if DEBUG:
                print(
                    f"Identified user mention: text='{link_text}', href='{href_val}', full_url='{full_url}'"
                )
        # Check if it's a hashtag/cashtag
        elif (
            href_val
            and isinstance(href_val, str)  # Check href is string
            and (
                href_val.startswith("/search?q=%23")  # Hashtag
                or href_val.startswith("/search?q=%24")  # Cashtag
            )
        ):
            is_hash_cash_tag = True
            full_url = f"https://x.com{href_val}"
            links.append((link_text, full_url))
            if DEBUG:
                print(
                    f"Identified hash/cash tag: text='{link_text}', href='{href_val}', full_url='{full_url}'"
                )
        # Check if it's an external link (starts with http) or potentially other relative links we want to capture
        elif (
            href_val
            and isinstance(href_val, str)  # Check href is string
            and href_val.startswith("http")
        ):
            is_external_link = True
            # Check if the display text looks like a t.co shortened link, but isn't the href itself
            # Sometimes twitter displays the full url but links the t.co version
            link_text_raw = a_tag.get_text().strip()  # Get raw text first
            tco_match = re.search(r"https://t\\.co/[a-zA-Z0-9]+", link_text_raw)
            actual_display_text = link_text_raw
            if tco_match and tco_match.group(0) != href_val:
                # Attempt to find the real display text elsewhere in the tag if available
                possible_display_text = a_tag.get_text(strip=True)
                if possible_display_text != href_val:  # Prefer non-href text if different
                    actual_display_text = possible_display_text

            # Normalize the text we intend to replace *before* adding to list
            normalized_display_text = " ".join(actual_display_text.split())

            links.append((normalized_display_text, href_val))
            if DEBUG:
                print(
                    f"Identified external link: text='{normalized_display_text}' (normalized), href='{href_val}'"
                )
        elif DEBUG and not is_user_mention and not is_hash_cash_tag and not is_external_link:
            pass  # Keep logic path

    # Get initial content
    content = tweet_text_element.get_text(separator=" ", strip=True)
    # Targeted fix for potential extra space after schema added by get_text
    content = content.replace("https:// ", "https://").replace("http:// ", "http://")
    # General normalization
    content = " ".join(content.split())

    if DEBUG:
        print(
            f"--- Content before replacements (fixed+normalized) ---\n{content}\n---------------------------------"
        )

    # Replace links sequentially using re.sub
    links.sort(key=lambda x: len(x[0]), reverse=True)
    for link_text, href in links:  # link_text IS normalized for external links
        # Remove explicit check: if link_text not in content
        if not isinstance(link_text, str):
            if DEBUG:
                print(f"Skipping replacement: link_text '{link_text}' is not a string.")
            continue

        markdown_link = f"[{link_text}]({href})"
        # Use normalized link_text for pattern
        escaped_text = re.escape(link_text)
        # Simpler pattern: Not preceded by [, not followed by ](
        pattern = r"(?<!\[)" + escaped_text + r"(?!\]\()"

        try:
            # Attempt replacement on potentially un-normalized content
            new_content = re.sub(pattern, markdown_link, content, count=1)
            if new_content != content:
                if DEBUG:
                    print(f"  Replaced '{link_text}' -> '{markdown_link}'")
                content = new_content  # Update content with the result
            elif DEBUG:
                print(f"  Pattern '{pattern}' did not match for '{link_text}' in content.")
        except Exception as e:
            if isinstance(e, re.error):
                if DEBUG:
                    print(f"  Regex error for pattern '{pattern}': {e}")
            elif DEBUG:
                print(f"  Error during re.sub for '{link_text}': {e}")

    if DEBUG:
        print(f"--- Content AFTER replacements ---\n{content}\n------------------------------")

    return content


def extract_media(element: Tag) -> List[str]:
    """Extract images video preview images"""
    media_strings = []
    processed_urls: Set[str] = set()

    images = element.select(
        'article [data-testid="tweetPhoto"] img, article a[href*="/photo/"] img'
    )
    for img in images:
        if not isinstance(img, Tag):
            continue  # Type check
        src = img.get("src")
        if (
            src
            and isinstance(src, str)
            and "profile_images" not in src
            and "emoji" not in src
            and not src.startswith("data:")
            and src not in processed_urls
        ):
            parent_link = img.find_parent("a")
            if isinstance(parent_link, Tag):
                link_href = parent_link.get("href")
                if (
                    isinstance(link_href, str)
                    and "/status/" in link_href
                    and "/photo/" in link_href
                ):
                    if DEBUG:
                        print(f"Found image link: {link_href}, using src: {src}")

            # Store only the URL
            media_strings.append(src)
            processed_urls.add(src)

    videos = element.select("article video")
    for video in videos:
        if not isinstance(video, Tag):
            continue  # Type check
        poster = video.get("poster")
        if (
            poster
            and isinstance(poster, str)
            and "profile_images" not in poster
            and poster not in processed_urls
            and not poster.startswith("data:")
        ):
            parent_link = video.find_parent("a")
            video_url = poster
            if isinstance(parent_link, Tag):
                link_href = parent_link.get("href")
                if link_href and isinstance(link_href, str) and "/status/" in link_href:
                    full_link = (
                        f"https://x.com{link_href}" if link_href.startswith("/") else link_href
                    )
                    if DEBUG:
                        if print(f"Found video link: {full_link}, using poster: {poster}"):
                            video_url = poster  # Keep using poster for now

            # Store only the URL (poster)
            media_strings.append(video_url)
            processed_urls.add(poster)
            if video_url != poster:
                processed_urls.add(video_url)

        else:
            source = video.select_one("source")
            if isinstance(source, Tag):
                src = source.get("src")
                if (
                    src
                    and isinstance(src, str)
                    and src not in processed_urls
                    and not src.startswith("blob:")
                ):
                    media_strings.append(src)
                    processed_urls.add(src)

    gif_containers = element.select(
        'article div[aria-label="Embedded video"], article [data-testid="tweetPhoto"] video'
    )
    for container in gif_containers:
        video_tag = (
            container
            if isinstance(container, Tag) and container.name == "video"
            else container.find("video")
        )
        if isinstance(video_tag, Tag):
            poster = video_tag.get("poster")
            if poster and isinstance(poster, str) and poster not in processed_urls:
                # Store only the URL (poster)
                media_strings.append(poster)
                processed_urls.add(poster)

    return media_strings


def extract_metrics(element: Tag) -> Dict[str, int]:
    """Extracts metrics (replies, retweets, likes, views) from action bar."""
    metrics: Dict[str, int] = {"replies": 0, "retweets": 0, "likes": 0, "views": 0}
    action_bar = element.select_one('article [role="group"]')
    if not isinstance(action_bar, Tag):
        if DEBUG:
            print('Could not find action bar group [role="group"] within article')
        # Even without an action bar, views might still exist, so continue to view search
    else:
        if DEBUG:
            print('Found action bar [role="group"]')
        # --- Extract from Buttons --- #
        button_map = {
            "reply": "replies",
            "retweet": "retweets",
            "like": "likes",
        }
        for test_id, metric_key in button_map.items():
            button = action_bar.select_one(f'button[data-testid="{test_id}"]')
            if isinstance(button, Tag):
                text_span = button.select_one(
                    'span[data-testid="app-text-transition-container"] span span'
                )
                if isinstance(text_span, Tag):
                    count_text = text_span.get_text(strip=True)
                    if (
                        count_text.replace(",", "")
                        .replace(".", "")
                        .replace("K", "")
                        .replace("M", "")
                        .isdigit()
                    ) or re.match(r"^\\d*\\.?\\d+[KkMm]?$", count_text):  # Improved check for K/M
                        metrics[metric_key] = _parse_metric_string(count_text)
                        if DEBUG:
                            print(f"Found {metric_key} count '{count_text}' from button.")
                    else:
                        if DEBUG:
                            print(
                                f"Button span text '{count_text}' not recognized as count for {metric_key}."
                            )
                else:
                    if DEBUG:
                        print(f"Could not find count text span for {metric_key} button.")
            else:
                if DEBUG:
                    print(f"Could not find button with data-testid='{test_id}'.")

    # --- Extract Views (Unified Logic) --- #
    view_link_found = False
    # Prioritize /analytics links, then /status/ links
    candidate_links = element.select('article a[href*="/analytics"]') + element.select(
        'article a[href*="/status/"]'
    )

    if DEBUG:
        print(f"Found {len(candidate_links)} candidate links for views.")

    for link in candidate_links:
        if view_link_found:
            break  # Stop if we already found views
        if not isinstance(link, Tag):
            continue

        href = link.get("href", "")
        if not isinstance(href, str):
            continue
        if DEBUG:
            print(f"Checking link {href} for view count...")

        potential_spans = link.select("span")
        for span in potential_spans:
            if not isinstance(span, Tag):
                continue
            span_text = span.get_text(strip=True)

            if re.fullmatch(r"[\d,.]+[KkMm]?", span_text) or span_text.isdigit():
                if DEBUG:
                    print(f"Found potential view count span '{span_text}' in link {href}")
                view_count_match = re.search(r"([\d,.]+[KkMm]?)", span_text)
                if view_count_match:
                    raw_count = view_count_match.group(1)
                    metrics["views"] = _parse_metric_string(raw_count)
                    if DEBUG:
                        print(
                            f"Extracted view count '{raw_count}' from link {href}. Assigning and stopping search."
                        )
                    view_link_found = True
                    break  # Exit inner span loop
            # else: print(f"Span text '{span_text}' did not match pattern.")
        # End inner span loop
    # End outer link loop

    if not view_link_found:
        if DEBUG:
            print("Could not find a suitable link/span containing view count.")

    if DEBUG:
        print(f"Final metrics: {metrics}")
    return metrics


def extract_tweet_metadata(
    tweet_element: Tag,
) -> Tuple[Optional[str], Optional[str]]:
    """Extracts timestamp and url from a tweet element."""
    timestamp: Optional[str] = None
    url: Optional[str] = None

    # Strategy: Find the primary link associated with the timestamp first.
    # This link usually contains the tweet's canonical URL and has a <time> tag.

    # Look for a link containing "/status/" that also contains a <time> element.
    # Prioritize links within the User-Name section if available.
    user_name_section = tweet_element.select_one('[data-testid="User-Name"]')
    primary_link = None
    if isinstance(user_name_section, Tag):
        primary_link = user_name_section.find(
            "a", href=lambda h: isinstance(h, str) and "/status/" in h and bool(h.count("/") >= 3)
        )
        # Check if this link actually contains a time tag
        if isinstance(primary_link, Tag) and not primary_link.find("time", datetime=True):
            primary_link = None  # Reset if time tag isn't inside

    # Fallback: Search the whole tweet article for such a link if not found in user section
    if not primary_link:
        links_with_time = tweet_element.select('article a[href*="/status/"] time[datetime]')
        if links_with_time:
            time_tag = links_with_time[0]  # Get the first time tag found
            if isinstance(time_tag, Tag):
                primary_link = time_tag.find_parent("a")  # Find its parent link

    # Extract URL and Timestamp from the primary link if found
    if isinstance(primary_link, Tag):
        href = primary_link.get("href")
        if href and isinstance(href, str):
            url = f"https://x.com{href}" if href.startswith("/") else href
            if DEBUG:
                print(f"Found primary tweet link: {href}")

        time_tag = primary_link.find("time", datetime=True)
        if isinstance(time_tag, Tag):
            datetime_val = time_tag.get("datetime")
            if datetime_val and isinstance(datetime_val, str):
                timestamp = datetime_val
                if DEBUG:
                    print(f"Found timestamp in primary link: {datetime_val}")

    # Last resort fallbacks if primary link method failed
    if not url:
        # Find any link with /status/ anywhere
        any_status_link = tweet_element.select_one('article a[href*="/status/"]')
        if isinstance(any_status_link, Tag):
            href = any_status_link.get("href")
            # Check if href matches the expected pattern: /<username>/status/<digits>
            if href and isinstance(href, str) and re.match(r"^/[^/]+/status/\d+/?$", href):
                url = f"https://x.com{href}"  # Only assign if it looks like a real status link
                if DEBUG:
                    print(f"Found tweet URL via general /status/ link fallback: {href}")
            elif DEBUG and href and isinstance(href, str):
                print(f"Fallback link found ('{href}') but rejected as invalid status URL pattern.")

    if not timestamp:
        # Find any time tag with datetime anywhere
        any_time_tag = tweet_element.select_one("article time[datetime]")
        if isinstance(any_time_tag, Tag):
            datetime_val = any_time_tag.get("datetime")
            if datetime_val and isinstance(datetime_val, str):
                timestamp = datetime_val
                if DEBUG:
                    print(f"Found timestamp via general time[datetime] fallback: {datetime_val}")

    if DEBUG:
        print(f"Final extracted metadata: timestamp='{timestamp}', url='{url}'")
    return timestamp, url


# ---- Quoted Tweet Extraction ----


class QuotedTweet(TypedDict, total=False):
    text: Optional[str]
    author_name: Optional[str]
    author_url: Optional[str]
    url: Optional[str]


def extract_quoted_tweet(element: Tag) -> Optional[QuotedTweet]:
    """Extracts content from a quoted tweet within a main tweet element."""
    # TODO: Implement selector based on actual HTML structure
    quote_tweet_container = element.select_one(
        'div[role="link"][tabindex="0"]:not([aria-labelledby])'  # Placeholder selector - NEEDS VERIFICATION
    )

    if not isinstance(quote_tweet_container, Tag):
        if DEBUG:
            print("No potential quoted tweet container found.")
        return None

    if DEBUG:
        print("Potential quoted tweet container found. Extracting...")

    quoted_data: QuotedTweet = {}

    # Try extracting user - adapt selectors if needed within the quote structure
    # Assuming quoted user info might be within a specific nested div
    user_element = quote_tweet_container  # Or a more specific selector within it
    user_info = extract_user(user_element)
    quoted_data["author_name"] = user_info.get("name")
    quoted_data["author_url"] = user_info.get("url")

    # Try extracting text - adapt selectors for quoted text
    # Assuming quoted text might be in a specific nested div
    text_element = quote_tweet_container  # Or a more specific selector
    quoted_data["text"] = extract_tweet_text(text_element)

    # Try extracting metadata (URL, timestamp) - might be less reliable/necessary
    # timestamp_str, url = extract_tweet_metadata(quote_tweet_container)
    # quoted_data["url"] = url

    # Return data only if we found some text
    if quoted_data.get("text"):
        if DEBUG:
            print(f"Extracted quoted tweet data: {quoted_data}")
        return quoted_data
    else:
        if DEBUG:
            print("Extracted quoted tweet container, but failed to get text.")
        return None
