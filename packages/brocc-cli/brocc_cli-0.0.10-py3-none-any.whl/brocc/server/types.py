from enum import Enum

from brocc.internal.logger import get_logger

logger = get_logger(__name__)


class MonitorStatus(Enum):
    """Enumerates the possible states of the monitoring service."""

    INACTIVE = "inactive"  # Not running or explicitly stopped
    ACTIVE = "active"  # Running and monitoring
    PAUSED_CHROME_DISCONNECTED = "paused_chrome_disconnected"  # Running but Chrome not reachable
    ERROR = "error"  # An unrecoverable error occurred
