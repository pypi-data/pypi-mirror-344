from typing import Any, Dict, Optional, Union

import httpx

from starfruit.internal.const import INTERNAL_API_URL
from starfruit.internal.logger import get_logger

logger = get_logger(__name__)


def notify_frontend(source_task: str, item_id: Optional[Union[int, str]] = None):
    """Sends a notification to the frontend via internal API."""
    try:
        notify_url = f"{INTERNAL_API_URL}/ws/frontend/internal/notify_update"
        # Include source task and optionally item ID in payload
        notify_payload: Dict[str, Any] = {"source_task": source_task}
        if item_id is not None:
            notify_payload["item_id"] = str(item_id)  # Ensure ID is string

        response = httpx.post(notify_url, json=notify_payload, timeout=5.0)  # Shorter timeout
        response.raise_for_status()
        if response.status_code == 202:
            pass
        else:
            logger.warning(
                f"Frontend notification request ({source_task}) returned unexpected status: {response.status_code}"
            )
    except httpx.RequestError as req_err:
        logger.error(
            f"HTTP request error notifying frontend ({source_task}): {req_err}", exc_info=False
        )  # Less noisy log
    except httpx.HTTPStatusError as status_err:
        logger.error(
            f"HTTP status error notifying frontend ({source_task}): {status_err.response.status_code}",
            exc_info=False,  # Less noisy log
        )
    except Exception as notify_err:
        logger.error(
            f"Unexpected error notifying frontend ({source_task}): {notify_err}", exc_info=True
        )
