from typing import Optional

from bs4 import BeautifulSoup

from starfruit.internal.logger import get_logger

logger = get_logger(__name__)


def safe_get_soup(html: str) -> Optional[BeautifulSoup]:
    """Safely creates a BeautifulSoup object from HTML string.
    Returns:
        A BeautifulSoup object, or None if parsing fails.
    """
    try:
        # Using 'lxml' for performance and robustness.
        soup = BeautifulSoup(html, "lxml")
        return soup
    except ImportError:
        # Fallback to 'html.parser' if lxml is not installed
        logger.warning(
            "lxml not found, falling back to html.parser. Install lxml for better performance."
        )
        try:
            soup = BeautifulSoup(html, "html.parser")
            return soup
        except Exception as e:
            logger.warning(
                f"Failed to parse HTML with html.parser after lxml failed: {e}", exc_info=False
            )
            return None
    except Exception as e:
        # Catching other potential exceptions during lxml parsing.
        logger.warning(f"Failed to parse HTML with lxml: {e}", exc_info=False)
        return None
