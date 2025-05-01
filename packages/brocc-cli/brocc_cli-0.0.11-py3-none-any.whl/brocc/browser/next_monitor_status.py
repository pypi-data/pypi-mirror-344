from brocc.internal.logger import get_logger
from brocc.server.types import MonitorStatus

logger = get_logger(__name__)


def next_monitor_status(
    current_status: MonitorStatus,
    chrome_connected: bool,
) -> MonitorStatus:
    """Determines the target monitoring state based on external conditions."""
    if not chrome_connected:
        return MonitorStatus.PAUSED_CHROME_DISCONNECTED

    # If currently in a paused, inactive, or error state,
    # and all conditions are met, transition to ACTIVE.
    if current_status in [
        MonitorStatus.PAUSED_CHROME_DISCONNECTED,
        MonitorStatus.INACTIVE,
        MonitorStatus.ERROR,
    ]:
        return MonitorStatus.ACTIVE
    # Otherwise, maintain the current status (likely ACTIVE already).
    return current_status
