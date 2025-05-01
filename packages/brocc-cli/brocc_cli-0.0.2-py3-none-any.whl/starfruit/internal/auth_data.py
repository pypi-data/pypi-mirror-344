import json
from typing import Any, Dict, Optional

from starfruit.internal.env import starfruit_api_key
from starfruit.internal.get_app_dir import get_app_dir
from starfruit.internal.logger import get_logger

logger = get_logger(__name__)

APP_DIR = get_app_dir()
AUTH_FILE = APP_DIR / "auth.json"


def is_logged_in(auth_data: Optional[Dict[str, Any]]) -> bool:
    """Check if the user is logged in"""
    if auth_data is None:
        return False
    return "apiKey" in auth_data and bool(auth_data.get("apiKey"))


def load_auth_data() -> Optional[Dict[str, Any]]:
    """
    Load auth data, prioritizing STARFRUIT_API_KEY env var over the auth file.
    """
    # 1. Prioritize environment variable
    env_api_key = starfruit_api_key()
    if env_api_key:
        logger.debug("Using API key from STARFRUIT_API_KEY environment variable.")
        # NOTE: Other fields like 'email' won't be present when using env var
        return {"apiKey": env_api_key}

    # 2. Fallback to auth file if env var not set
    try:
        if AUTH_FILE.exists():
            with open(AUTH_FILE) as f:
                auth_data = json.load(f)
            return auth_data
        else:
            logger.debug("No saved auth data found")
            return None
    except Exception as e:
        logger.error(f"Error loading auth data: {e}")
        return None


def save_auth_data(auth_data: Dict[str, Any]) -> bool:
    """Save auth data to JSON file."""
    try:
        # Ensure the directory exists
        APP_DIR.mkdir(parents=True, exist_ok=True)
        with open(AUTH_FILE, "w") as f:
            json.dump(auth_data, f, indent=2)  # Add indent for readability
        logger.debug(f"Saved auth data for user: {auth_data.get('email', 'unknown')}")
        return True
    except Exception as e:
        logger.error(f"Error saving auth data: {e}")
        return False


def clear_auth_data() -> bool:
    """Clear auth data file."""
    try:
        if AUTH_FILE.exists():
            AUTH_FILE.unlink()
        logger.debug("Cleared auth data")
        return True
    except Exception as e:
        logger.error(f"Error clearing auth data: {e}")
        return False


def logout():
    """
    Logs the user out by clearing their authentication data.

    Returns:
        bool: True if successful, False otherwise.
    """
    # clear_auth_data already handles logging and returns success status
    return clear_auth_data()
