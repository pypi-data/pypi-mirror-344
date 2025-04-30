from urllib.parse import urlparse, urlunparse

from starfruit.internal.logger import get_logger

logger = get_logger(__name__)


def normalize_url(url: str) -> str:
    """Removes query parameters and fragment identifiers from a URL.

    Ensures a consistent format, e.g., http://example.com -> http://example.com/
    """
    if not url:  # Handle empty or None urls gracefully
        return ""
    try:
        parsed = urlparse(url)
        # Reconstruct the URL without query and fragment
        # Ensure path starts with '/' if netloc exists and path is empty or missing
        path = parsed.path
        if parsed.netloc and not path:
            path = "/"
        elif not parsed.netloc and path.startswith("//"):
            # Handle schemeless urls like //example.com/path
            # urlparse puts //example.com in netloc if scheme is missing.
            pass  # Path is likely correct as parsed

        normalized_url = urlunparse(
            (
                parsed.scheme,
                parsed.netloc,
                path or "",  # Ensure path is not None
                "",  # params - usually empty, keep empty
                "",  # query - remove
                "",  # fragment - remove
            )
        )

        # Handle case where path was originally just '/' and got potentially removed by urlunparse if empty path resulted
        # Example: urlparse('http://example.com/') -> ParseResult(scheme='http', netloc='example.com', path='/', ...)
        # urlunparse(('http','example.com','/','','','')) -> 'http://example.com/' (Correct)
        # Example: urlparse('http://example.com') -> ParseResult(scheme='http', netloc='example.com', path='', ...)
        # path becomes '/' above.
        # urlunparse(('http','example.com','/','','','')) -> 'http://example.com/' (Correct)

        return normalized_url
    except Exception as e:
        # Log error and return original url if parsing fails
        logger.error(f"Failed to normalize URL '{url}': {e}. Returning original.", exc_info=False)
        return url
