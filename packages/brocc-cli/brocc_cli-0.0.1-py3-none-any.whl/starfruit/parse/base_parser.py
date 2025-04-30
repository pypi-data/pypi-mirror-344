import abc
import re
from typing import List

from starfruit.internal.logger import get_logger
from starfruit.tasks.task_item import ParseResult

logger = get_logger(__name__)


class BaseParser(abc.ABC):
    """
    Abstract base class for parsers that extract a SINGLE dictionary item
    from an entire HTML page.
    """

    def __init__(self, url_patterns: List[str]):
        # Compile and store multiple regex patterns
        self._url_patterns = [re.compile(pattern) for pattern in url_patterns]

    def can_parse(self, url: str) -> bool:
        """Checks if this parser is appropriate for the given URL based on any of its patterns."""
        # Return True if any pattern matches
        return any(pattern.match(url) for pattern in self._url_patterns)

    @abc.abstractmethod
    def _parse_page(self, html: str, url: str) -> List[ParseResult]:
        """
        Parses the entire HTML content string into a single dictionary.

        Args:
            html: The raw HTML content string.
            url: The URL the HTML was fetched from.

        Returns None if the page cannot be parsed or should be skipped.
        """
        pass

    def parse(self, html: str, url: str) -> List[ParseResult]:
        """
        Parses the full HTML content into a single dictionary item.

        Args:
            html: The raw HTML content string.
            url: The URL the HTML was fetched from.

        Returns the parsed item dictionary, or None if parsing or validation fails.
        """
        # We might still need soup for quick checks or specific tag finding if needed,
        # but _parse_page now primarily uses the html string.
        results: List[ParseResult] = []
        try:
            results = self._parse_page(html=html, url=url)
            # Validation is now part of _parse_page's responsibility implicitly
            # by returning status='failed' or correct data model
        except Exception as e:
            # Log the specific URL that failed
            logger.error(f"Failed to parse page at {url}: {e}", exc_info=True)
            return []  # Return empty list on error

        # Return the list of results (usually just one for page parser)
        return results
