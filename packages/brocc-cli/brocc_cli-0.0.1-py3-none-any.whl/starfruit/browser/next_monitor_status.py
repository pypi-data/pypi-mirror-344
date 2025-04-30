from starfruit.internal.logger import get_logger
from starfruit.server.types import MonitorStatus

logger = get_logger(__name__)


def next_monitor_status(
    current_status: MonitorStatus,
    chrome_connected: bool,
    user_logged_in: bool,
) -> MonitorStatus:
    """Determines the target monitoring state based on external conditions."""
    if not chrome_connected:
        return MonitorStatus.PAUSED_CHROME_DISCONNECTED
    if not user_logged_in:
        return MonitorStatus.PAUSED_NEEDS_LOGIN

    # If currently in a paused, inactive, or error state,
    # and all conditions are met, transition to ACTIVE.
    if current_status in [
        MonitorStatus.PAUSED_CHROME_DISCONNECTED,
        MonitorStatus.PAUSED_NEEDS_LOGIN,
        MonitorStatus.INACTIVE,
        MonitorStatus.ERROR,
    ]:
        return MonitorStatus.ACTIVE
    # Otherwise, maintain the current status (likely ACTIVE already).
    return current_status
