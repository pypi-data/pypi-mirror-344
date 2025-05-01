import re
from typing import Optional, Tuple
from urllib.parse import urlparse

from markdownify import markdownify

from starfruit.internal.logger import get_logger
from starfruit.parse.parser_registry import get_parser_for_url
from starfruit.tasks.hash_content import hash_content

logger = get_logger(__name__)

# Minimum character length for markdown content to be considered save-worthy
MIN_MARKDOWN_LENGTH = 100

# File extensions to ignore early
IGNORED_FILE_EXTENSIONS = {
    # Styles/Scripts (less common direct nav, but possible)
    ".css",
    ".js",
    ".json",
    ".xml",
    # Images (Chrome often renders these directly)
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".ico",
    # Media (Chrome might render a simple player)
    ".mp3",
    ".mp4",
    ".avi",
    ".mov",
    ".wav",
}

# Common path segments indicating non-content pages
# Check for these *exact* keywords as components in the URL path
NOISE_URL_PATH_COMPONENTS = {
    "login",
    "log-in",
    "log_in",
    "signin",
    "sign-in",
    "sign_in",
    "auth",
    "oauth",
    "register",
    "signup",
    "sign-up",
    "sign_up",
    "passwordreset",
    "passwordchange",
    "password-reset",
    "password-change",
    "password_reset",
    "password_change",
    "forgotpassword",
    "forgot-password",
    "forgot_password",
}

# Hostnames/suffixes for common password managers
PASSWORD_MANAGER_HOSTNAMES = {
    ".lastpass.com",
    ".bitwarden.com",
    ".dashlane.com",
    ".keepersecurity.com",
    ".roboform.com",
    ".nordpass.com",
    ".nordaccount.com",
    ".1password.com",
}

# Path components indicating 2FA/MFA or verification steps
TWO_FACTOR_AUTH_PATH_COMPONENTS = {
    "2fa",
    "mfa",
    "twofactor",
    "multifactor",
    "two-factor",
    "multi-factor",
    "two_factor",
    "multi_factor",
    "2fa_settings",
    "setup-mfa",
    "verify",
    "challenge",
    "otp",
    "security-key",
    "security_key",
    "authentication",
}

# Path components indicating CAPTCHA challenges
CAPTCHA_PATH_COMPONENTS = {
    "captcha",
    "captcha-verify",
    "captcha_verify",
    "recaptcha",
    "hcaptcha",
    "hcaptcha-verify",
    "hcaptcha_verify",
    "challenge",  # Already in 2FA, but highly relevant here too
    "verify-human",
    "verify_human",
    "are-you-human",
    "are_you_human",
}

# Simple pattern to find <input type=password>
PASSWORD_INPUT_PATTERN = re.compile(
    r"<input[^>]+type=[" + "'" + r"]?password[" + "'" + r"]?[^>]*>", re.IGNORECASE
)
# Simple pattern to extract <title> content
TITLE_TAG_PATTERN = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def _log_skip(url: str, reason: str, level: str = "debug") -> None:
    """Helper to log skipping a URL with truncation."""
    truncated_url = f"{url[:50]}{'...' if len(url) > 50 else ''}"
    log_func = getattr(logger, level)
    log_func(f"should_save_content: Skipping {truncated_url} - {reason}")


def should_save_content(
    url: str, html_content: Optional[str]
) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Determines if the content for a given URL should be saved based on:
    1. URL Scheme (must be http/https)
    2. Hostname (not localhost)
    3. File extension
    4. Parser existence
    5. URL path noise components
    6. HTML heuristics (password fields)
    7. Minimum markdown length
    8. Content duplication (markdown hash)

    Returns:
        A tuple containing:
        - bool: True if the content should be saved, False otherwise.
        - Optional[str]: The reason for skipping, if applicable (e.g., "No parser found", "Duplicate content").
        - Optional[str]: The SHA256 hash of the *markdownified* HTML content if it exists and hashing succeeded, otherwise None.
    """
    # 0. Pre-checks: Parse URL and check scheme/hostname first
    try:
        parsed_url = urlparse(url)

        # Check scheme
        if parsed_url.scheme not in ["http", "https"]:
            reason = f"Non-HTTP(S) scheme ('{parsed_url.scheme}')"
            _log_skip(url, reason)
            return False, reason, None

        # Check hostname for localhost or password managers
        hostname = parsed_url.hostname.lower() if parsed_url.hostname else ""
        if hostname == "localhost" or hostname == "127.0.0.1":
            reason = f"Localhost URL ('{hostname}')"
            _log_skip(url, reason)
            return False, reason, None
        # Check if hostname ends with any password manager domains OR exactly matches the domain without the leading dot
        if any(
            hostname.endswith(pm_host) or hostname == pm_host.lstrip(".")
            for pm_host in PASSWORD_MANAGER_HOSTNAMES
        ):
            reason = f"Password manager URL ('{hostname}')"
            _log_skip(url, reason)
            return False, reason, None

    except Exception as url_parse_err:
        reason = "URL parse error"
        logger.error(
            f"should_save_content: Critical error parsing URL {url}: {url_parse_err}. Cannot proceed.",
            exc_info=True,
        )
        return False, reason, None

    # 1. Check for ignored file extensions in URL path
    try:
        # Reuse parsed_url
        path = parsed_url.path.lower()
        # Efficiently check if the path ends with any of the ignored extensions
        if any(path.endswith(ext) for ext in IGNORED_FILE_EXTENSIONS):
            reason = f"URL has ignored file extension ('{path}')"
            _log_skip(url, reason)
            return False, reason, None
    except Exception as ext_check_err:  # More specific error handling if needed
        logger.warning(f"Error checking file extension for {url}: {ext_check_err}. Skipping check.")

    # 2. Check if there's a parser for the URL
    parser = get_parser_for_url(url)
    if not parser:
        reason = "No parser found"
        _log_skip(url, reason)
        return False, reason, None

    # 3. Check for noise patterns (login, auth, etc.) in URL path components
    try:
        path = parsed_url.path.lower()  # Path already lowercased
        path_components = {c for c in path.strip("/").split("/") if c}
        noisy_components_found = path_components.intersection(NOISE_URL_PATH_COMPONENTS)
        if noisy_components_found:
            reason = f"URL indicates noise page (components: {noisy_components_found})"
            _log_skip(url, reason)
            return False, reason, None
    except Exception as url_parse_err:
        logger.warning(
            f"Error parsing URL {url} for noise component check: {url_parse_err}. Skipping check."
        )

    # 4. Check for 2FA/MFA/Verify patterns in URL path components
    try:
        # Reuse path_components if available from previous check
        if "path_components" not in locals():
            path = parsed_url.path.lower()
            path_components = {c for c in path.strip("/").split("/") if c}
        two_factor_components_found = path_components.intersection(TWO_FACTOR_AUTH_PATH_COMPONENTS)
        if two_factor_components_found:
            reason = f"URL indicates 2FA/MFA page (components: {two_factor_components_found})"
            _log_skip(url, reason)
            return False, reason, None
    except Exception as url_parse_err:
        logger.warning(
            f"Error parsing URL {url} for 2FA/MFA component check: {url_parse_err}. Skipping check."
        )

    # 5. Check for CAPTCHA patterns in URL path components
    try:
        # Reuse path_components if available from previous checks
        if "path_components" not in locals():
            path = parsed_url.path.lower()
            path_components = {c for c in path.strip("/").split("/") if c}
        captcha_components_found = path_components.intersection(CAPTCHA_PATH_COMPONENTS)
        if captcha_components_found:
            reason = f"URL indicates CAPTCHA page (components: {captcha_components_found})"
            _log_skip(url, reason)
            return False, reason, None
    except Exception as url_parse_err:
        logger.warning(
            f"Error parsing URL {url} for CAPTCHA component check: {url_parse_err}. Skipping check."
        )

    # 6. Check if HTML content is present (needed for subsequent checks)
    if not html_content:
        reason = "HTML content missing"
        # Use warning level here as it might indicate a problem upstream
        _log_skip(url, reason, level="warning")
        return False, reason, None

    # 7. Check for password input fields in HTML
    try:
        if PASSWORD_INPUT_PATTERN.search(html_content):
            reason = "HTML contains password input"
            _log_skip(url, reason)
            return False, reason, None
    except Exception as pw_err:
        logger.warning(
            f"Error checking for password field in {url[:50]}{'...' if len(url) > 50 else ''}: {pw_err}."
        )  # Kept separate as it's an error *during* check, not a skip reason

    # 9. Convert HTML to Markdown
    try:
        markdown_content = markdownify(html_content)
        if not markdown_content:
            reason = "Empty markdown content"
            _log_skip(url, reason, level="warning")  # Use warning
            return False, reason, None
    except Exception as md_err:
        reason = "Markdown conversion error"
        logger.error(
            f"should_save_content: Error converting HTML to Markdown for {url[:50]}{'...' if len(url) > 50 else ''}: {md_err}",
            exc_info=True,
        )
        return False, reason, None

    # 10. Check minimum length
    if len(markdown_content) < MIN_MARKDOWN_LENGTH:
        reason = f"Markdown content too short ({len(markdown_content)} chars)"
        # Adding min length to the reason string itself is cleaner
        _log_skip(url, f"{reason}. Minimum: {MIN_MARKDOWN_LENGTH}")
        return False, reason, None

    # 11. Calculate markdown hash using the utility function
    markdown_hash = hash_content(markdown_content)

    # If all checks passed (or hashing failed but we proceed)
    return True, None, markdown_hash
