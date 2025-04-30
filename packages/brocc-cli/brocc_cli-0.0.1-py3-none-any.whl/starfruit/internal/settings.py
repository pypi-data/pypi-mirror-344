import json
from typing import Dict, Optional

from starfruit.internal.get_app_dir import get_app_dir
from starfruit.internal.logger import get_logger

logger = get_logger(__name__)

APP_DIR = get_app_dir()
SETTINGS_FILE = APP_DIR / "settings.json"


def load_settings() -> Dict[str, str]:
    """Load settings from JSON file."""
    try:
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE) as f:
                settings = json.load(f)
                # Ensure all values are strings, basic validation
                if not isinstance(settings, dict) or not all(
                    isinstance(k, str) and isinstance(v, str) for k, v in settings.items()
                ):
                    logger.error("Invalid settings format found. Re-initializing.")
                    return {}
                return settings
        else:
            logger.debug("No saved settings found")
            return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding settings JSON: {e}. Re-initializing.")
        return {}
    except Exception as e:
        logger.error(f"Error loading settings: {e}. Re-initializing.")
        return {}


def save_settings(settings: Dict[str, str]) -> bool:
    """Save settings to JSON file."""
    try:
        # Ensure all keys and values are strings before saving
        if not all(isinstance(k, str) and isinstance(v, str) for k, v in settings.items()):
            logger.error("Attempted to save settings with non-string keys or values.")
            return False

        APP_DIR.mkdir(parents=True, exist_ok=True)
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=2)
        logger.debug("Saved settings.")
        return True
    except Exception as e:
        logger.error(f"Error saving settings: {e}")
        return False


def get_setting(key: str) -> Optional[str]:
    """Get a specific setting by key."""
    settings = load_settings()
    return settings.get(key)


def set_setting(key: str, value: str) -> bool:
    """Set a specific setting."""
    if not isinstance(key, str) or not isinstance(value, str):
        logger.error("Setting key and value must be strings.")
        return False
    settings = load_settings()
    settings[key] = value
    return save_settings(settings)


def clear_settings() -> bool:
    """Clear settings file."""
    try:
        if SETTINGS_FILE.exists():
            SETTINGS_FILE.unlink()
        logger.debug("Cleared settings")
        return True
    except Exception as e:
        logger.error(f"Error clearing settings: {e}")
        return False
