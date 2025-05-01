import datetime
from datetime import timezone
from typing import List

from bs4 import BeautifulSoup, Tag

from brocc.internal.logger import get_logger
from brocc.parse.base_parser import BaseParser
from brocc.parse.id_from_url import id_from_url
from brocc.parse.twitter_utils import (
    extract_media,
    extract_metrics,
    extract_tweet_metadata,
    extract_tweet_text,
    extract_user,
)
from brocc.parse.types import ParsedContent, ParsedMetadata
from brocc.tasks.hash_content import hash_content

logger = get_logger(__name__)
DEBUG = False


class TwitterFeedParser(BaseParser):
    # Define the specific URL patterns for Twitter/X
    TWITTER_URL_PATTERNS: List[str] = [r"https://(?:www\.)?x\.com/.*"]
    TWEET_SELECTOR = 'article[data-testid="tweet"]'.replace("\\", "")

    def __init__(self):
        # Initialize BasePageParser with the URL patterns
        super().__init__(url_patterns=self.TWITTER_URL_PATTERNS)

    def _process_tweet_article(self, item: Tag, source_url_for_feed: str) -> ParsedContent | None:
        try:
            user_info = extract_user(item)
            content = extract_tweet_text(item)
            timestamp_str, url = extract_tweet_metadata(item)
            media = extract_media(item)
            metrics = extract_metrics(item)

            # Basic check if essential parts were found during parsing
            if not ((user_info.get("url") or user_info.get("name")) and (timestamp_str or url)):
                if DEBUG:
                    logger.debug(
                        "Skipping item pre-parsing validation due to missing user/timestamp/URL."
                    )
                return None

            # Convert timestamp string to datetime object (UTC)
            timestamp_dt: datetime.datetime | None = None
            if timestamp_str:
                try:
                    timestamp_dt = datetime.datetime.fromisoformat(timestamp_str).astimezone(
                        timezone.utc
                    )
                except (ValueError, TypeError):
                    logger.warning(
                        f"Could not parse timestamp: {timestamp_str}. Storing as NULL.",
                        exc_info=True,
                    )

            # Prepare data fields
            tweet_text = content or ""
            tweet_id = id_from_url(url) if url else None

            if not tweet_id or not url:
                logger.warning(f"Skipping tweet due to missing id or url after parsing: {url}")
                return None

            # Calculate hash
            content_hash = hash_content(tweet_text)
            if not content_hash:
                logger.error(f"Failed to calculate content hash for tweet {url}. Skipping.")
                return None

            # Construct ParsedMetadata
            parsed_metadata = ParsedMetadata(
                title=None,  # Tweets don't have titles
                author_name=user_info.get("name"),
                author_url=user_info.get("url"),
                source_url=source_url_for_feed,  # The feed URL where it was found
                created_at=timestamp_dt,
                media=media if media else None,
                metrics=metrics if metrics else None,
                additional_metadata=None,
            )

            # Construct ParsedContent
            parsed_content = ParsedContent(
                id=tweet_id,
                url=url,
                content_to_embed=tweet_text,
                content_to_store=tweet_text,  # Store original text
                metadata=parsed_metadata,
                is_summary_required=False,  # No summary needed
                raw_content_hash=content_hash,
            )
            return parsed_content

        except Exception as e:
            logger.error(f"Error parsing tweet article: {e}", exc_info=True)
            # Return None on internal error, indicates failure for this specific article
            return None

    def _parse_page(self, html: str, url: str) -> List[ParsedContent]:
        soup = BeautifulSoup(html, "html.parser")
        tweet_articles = soup.select(self.TWEET_SELECTOR)

        if not tweet_articles:
            logger.warning(f"No tweet articles found using '{self.TWEET_SELECTOR}' on page: {url}")
            return []  # Return empty list

        results: List[ParsedContent] = []
        for article in tweet_articles:
            # Pass the feed URL `url` to be used as source_url
            result = self._process_tweet_article(article, source_url_for_feed=url)
            if result is not None:
                # Append the successful ParsedContent object
                results.append(result)

        if not results:
            logger.warning(f"No valid tweet items could be processed from page: {url}")
            return []  # Return empty list

        return results
