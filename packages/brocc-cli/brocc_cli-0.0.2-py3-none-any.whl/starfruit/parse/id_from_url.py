import base64
import hashlib
import logging

# Use the root logger or create a specific one if needed
logger = logging.getLogger(__name__)


def id_from_url(url: str) -> str:
    """a compact, URL-safe hash ID from a URL string."""
    if not url or not isinstance(url, str):
        logger.warning(f"Cannot generate hash for invalid URL: {url}")
        # Return a specific marker or raise an error? Let's return a marker for now.
        return "invalid_url_hash_value"
    try:
        url_bytes = url.encode("utf-8")
        sha256_digest = hashlib.sha256(url_bytes).digest()
        # Encode using URL-safe base64 and remove padding ('=')
        base64_hash = base64.urlsafe_b64encode(sha256_digest).rstrip(b"=").decode("utf-8")
        return f"stf_{base64_hash}"
    except Exception as e:
        logger.error(f"Error generating hash for URL {url}: {e}", exc_info=True)
        return "hash_generation_error"
