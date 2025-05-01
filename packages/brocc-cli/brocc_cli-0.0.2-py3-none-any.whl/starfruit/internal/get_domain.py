from typing import Optional
from urllib.parse import urlparse

from starfruit.internal.logger import get_logger

logger = get_logger(__name__)


def get_domain(url: str) -> Optional[str]:
    """
    Extracts the registrable domain from a URL.

    - Handles http/https schemes.
    - Removes 'www.' prefix.
    - Removes port number.
    - Returns None for invalid schemes or parsing errors.
    """
    if not url or not url.startswith(("http://", "https://")):
        return None
    try:
        domain = urlparse(url).netloc
        # Remove www. prefix if present
        if domain.startswith("www."):
            domain = domain[4:]
        # Remove port if present
        domain = domain.split(":")[0]
        return domain
    except Exception as e:
        logger.warning(f"Could not parse domain from URL '{url}': {e}")
        return None
