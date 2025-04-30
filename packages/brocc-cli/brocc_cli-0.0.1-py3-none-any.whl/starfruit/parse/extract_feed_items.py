from typing import List

from bs4 import BeautifulSoup, Tag

from starfruit.internal.logger import get_logger

logger = get_logger(__name__)


def extract_feed_items(html: str, selector: str) -> List[Tag]:
    try:
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select(selector)
        if not items:
            logger.warning(f"No items found using selector '{selector}'. ")
            return []
        return list(items)
    except Exception as e:
        logger.error(f"Error parsing HTML to extract tweet containers: {e}", exc_info=True)
        return []
