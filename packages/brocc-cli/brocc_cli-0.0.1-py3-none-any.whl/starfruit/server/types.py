from enum import Enum

from starfruit.internal.logger import get_logger

logger = get_logger(__name__)


class MonitorStatus(Enum):
    """Enumerates the possible states of the monitoring service."""

    INACTIVE = "inactive"  # Not running or explicitly stopped
    ACTIVE = "active"  # Running and monitoring
    PAUSED_CHROME_DISCONNECTED = "paused_chrome_disconnected"  # Running but Chrome not reachable
    PAUSED_NEEDS_LOGIN = "paused_needs_login"  # Running but user not logged in
    ERROR = "error"  # An unrecoverable error occurred
