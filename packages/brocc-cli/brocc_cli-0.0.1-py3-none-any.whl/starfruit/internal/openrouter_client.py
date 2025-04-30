from typing import Optional

from openai import AsyncOpenAI, OpenAI

from starfruit.internal.auth_data import load_auth_data
from starfruit.internal.env import openrouter_api_key
from starfruit.internal.logger import get_logger

log = get_logger(__name__)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
HTTP_REFERER = "https://www.starfruit.sh"


def _get_app_openrouter_key() -> Optional[str]:
    """Loads auth data and attempts to find the OpenRouter API key."""
    auth_data = load_auth_data()
    if not auth_data:
        log.warning("Could not load auth data.")
        return None

    # Try the new format first (single apiKey)
    api_key = auth_data.get("apiKey")
    if api_key:
        log.debug("Found OpenRouter API key in auth data (new format).")
        return api_key

    # Fall back to old format (list of apiKeys)
    api_keys = auth_data.get("apiKeys")
    if not isinstance(api_keys, list):
        log.warning("No API key found in auth data.")
        return None

    for key_info in api_keys:
        if isinstance(key_info, dict) and key_info.get("keyType") == "openrouter":
            secret = key_info.get("secret")
            if secret:
                log.debug("Found OpenRouter API key in auth data (old format).")
                return secret
            else:
                log.warning("Found 'openrouter' key entry but 'secret' is missing.")

    log.warning("OpenRouter API key not found in auth data.")
    return None


def get_openrouter_client() -> OpenAI:
    """Initializes and returns the OpenAI client configured for OpenRouter."""
    api_key = openrouter_api_key()
    if api_key:
        log.debug("Using OpenRouter API key from environment variable.")
        return OpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=api_key,
            default_headers={"HTTP-Referer": HTTP_REFERER},
            timeout=20.0,
        )

    # Fall back to auth_data
    api_key = _get_app_openrouter_key()
    if not api_key:
        log.error(
            "OpenRouter API key not found in environment or auth data. Remote calls will fail."
        )
        raise ValueError("OpenRouter API key is required for remote LM calls.")

    return OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=api_key,
        default_headers={"HTTP-Referer": HTTP_REFERER},
        timeout=20.0,
    )


def get_async_openrouter_client() -> AsyncOpenAI:
    """Initializes and returns the AsyncOpenAI client configured for OpenRouter."""
    api_key = openrouter_api_key()
    if api_key:
        return AsyncOpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=api_key,
            default_headers={"HTTP-Referer": HTTP_REFERER},
            timeout=20.0,
        )

    # Fall back to auth_data
    api_key = _get_app_openrouter_key()
    if not api_key:
        log.error(
            "OpenRouter API key not found in environment or auth data. Async remote calls will fail."
        )
        raise ValueError("OpenRouter API key is required for remote LM calls.")

    return AsyncOpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=api_key,
        default_headers={"HTTP-Referer": HTTP_REFERER},
        timeout=20.0,
    )
