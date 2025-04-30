import hashlib
from typing import Optional

from starfruit.internal.logger import get_logger

logger = get_logger(__name__)


def hash_content(text: Optional[str]) -> Optional[str]:
    """Calculates the SHA256 hash of the given text content.

    Args:
        text_content: The string content to hash.

    Returns:
        The hex digest of the SHA256 hash, or None if input is None or hashing fails.
    """
    if not text:
        return None

    try:
        # Ensure content is encoded to bytes before hashing
        content_bytes = text.encode("utf-8")
        content_hash = hashlib.sha256(content_bytes).hexdigest()
        return content_hash
    except Exception as e:
        logger.error(f"Error calculating content hash: {e}", exc_info=True)
        return None
