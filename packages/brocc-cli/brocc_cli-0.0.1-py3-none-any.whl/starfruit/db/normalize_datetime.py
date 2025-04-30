import datetime
from datetime import timezone
from typing import Any, Optional

from starfruit.internal.logger import get_logger

logger = get_logger(__name__)


def normalize_datetime_to_utc(value: Any) -> Optional[datetime.datetime]:
    """Parses various inputs (datetime obj, ISO string) to a timezone-aware UTC datetime object.

    Handles naive datetime objects, timezone conversion, and invalid inputs.

    Args:
        value: The input value to normalize (datetime, ISO string, or None).

    Returns:
        A timezone-aware datetime object in UTC, or None if input is None or invalid.
    """
    if value is None:
        return None

    if isinstance(value, datetime.datetime):
        # If already a datetime object, ensure it's UTC
        if value.tzinfo is None:
            # Assign UTC timezone to naive datetime objects
            return value.replace(tzinfo=timezone.utc)
        else:
            # Convert timezone-aware datetime objects to UTC
            return value.astimezone(timezone.utc)

    if isinstance(value, str):
        # If it's a string, attempt to parse as ISO format
        try:
            dt_obj = datetime.datetime.fromisoformat(value)
            # Ensure the parsed object is UTC
            if dt_obj.tzinfo is None:
                return dt_obj.replace(tzinfo=timezone.utc)
            else:
                return dt_obj.astimezone(timezone.utc)
        except ValueError:
            # Log only the problematic value, not the full traceback for cleaner logs
            logger.warning(f"Could not parse datetime string '{value}'. Input is invalid.")
            return None
        except Exception as e:
            # Catch any other unexpected parsing errors
            logger.error(f"Unexpected error parsing datetime string '{value}': {e}", exc_info=True)
            return None

    # Log if the input type is unexpected
    logger.warning(f"Unexpected type for datetime normalization: {type(value)}. Value: {value}")
    return None
