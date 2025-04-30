import datetime
from datetime import timezone
from typing import List

from bs4 import BeautifulSoup, Tag
from pydantic import ValidationError

from starfruit.internal.logger import get_logger
from starfruit.parse.base_parser import BaseParser
from starfruit.parse.id_from_url import id_from_url
from starfruit.parse.twitter_utils import (
    extract_media,
    extract_metrics,
    extract_tweet_metadata,
    extract_tweet_text,
    extract_user,
)
from starfruit.tasks.task_item import ParseResult, ProcessingItem

logger = get_logger(__name__)
DEBUG = False


class TwitterFeedParser(BaseParser):
    # Define the specific URL patterns for Twitter/X
    TWITTER_URL_PATTERNS: List[str] = [r"https://(?:www\.)?x\.com/.*"]
    TWEET_SELECTOR = 'article[data-testid="tweet"]'

    def __init__(self):
        # Initialize BasePageParser with the URL patterns
        super().__init__(url_patterns=self.TWITTER_URL_PATTERNS)

    def _process_tweet_article(self, item: Tag) -> ParseResult | None:
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

            # Construct the dictionary
            parsed_dict = {
                "id": id_from_url(url) if url else None,
                "url": url,
                "source_url": None,
                "text": content or "",
                "author_name": user_info.get("name"),
                "author_url": user_info.get("url"),
                "title": None,
                "created_at": timestamp_dt,
                "media": media if media else None,
                "metrics": metrics if metrics else None,
                "additional_metadata": None,
            }
            # Validate and return ParseResult
            try:
                if not parsed_dict.get("id") or not parsed_dict.get("url"):
                    raise ValueError("Missing essential id or url")

                processing_item = ProcessingItem.model_validate(parsed_dict)
                return ParseResult(status="ready_to_embed", data=processing_item)
            except (ValidationError, ValueError) as e:
                error_msg = f"Failed to validate/create ProcessingItem: {e}"
                logger.warning(f"{error_msg} for item {parsed_dict.get('url')}")
                return ParseResult(status="failed", error=error_msg, data=None)

        except Exception as e:
            logger.error(f"Error parsing tweet article: {e}", exc_info=True)
            return ParseResult(status="failed", error=f"Internal parsing error: {e}", data=None)

    def _parse_page(self, html: str, url: str) -> List[ParseResult]:
        soup = BeautifulSoup(html, "html.parser")
        tweet_articles = soup.select(self.TWEET_SELECTOR)

        if not tweet_articles:
            logger.warning(f"No tweet articles found using '{self.TWEET_SELECTOR}' on page: {url}")
            return [ParseResult(status="failed", error="No tweet articles found", data=None)]

        results: List[ParseResult] = []
        for article in tweet_articles:
            result = self._process_tweet_article(article)
            if result is not None:
                if result.data and result.status == "ready_to_embed":
                    result.data.source_url = url
                results.append(result)

        if not results:
            logger.warning(f"No valid tweet items could be processed from page: {url}")
            return [ParseResult(status="failed", error="No valid items processed", data=None)]

        return results
