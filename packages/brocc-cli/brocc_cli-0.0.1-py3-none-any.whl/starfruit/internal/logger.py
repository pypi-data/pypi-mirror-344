import logging
import sys
import time

from starfruit.internal.get_app_dir import get_app_dir

APP_DIR = get_app_dir()
LOG_FILE = APP_DIR / "starfruit_session.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

_log_formatter = None
_file_handler = None
_console_handler = None
_handlers_initialized = False


class ImmediateDuplicateFilter(logging.Filter):
    """Suppresses log records identical to the immediate predecessor."""

    def __init__(self, name=""):
        super().__init__(name)
        # Stores (name, levelno, msg) of the last *allowed* record
        self.last_log_details = None

    def filter(self, record):
        current_details = (record.name, record.levelno, record.getMessage())
        if current_details == self.last_log_details:
            return False  # Suppress duplicate
        self.last_log_details = current_details
        return True


def _initialize_handlers():
    global _log_formatter, _file_handler, _console_handler, _handlers_initialized
    if _handlers_initialized:
        return

    class CustomFormatter(logging.Formatter):
        _level_map = {
            logging.DEBUG: "DBG",
            logging.INFO: "INF",
            logging.WARNING: "WRN",
            logging.ERROR: "ERR",
            logging.CRITICAL: "CRT",
        }

        def format(self, record):
            record.levelname = self._level_map.get(record.levelno, record.levelname[:3])
            if record.name.startswith("starfruit."):
                record.name = record.name[len("starfruit.") :]
            return super().format(record)

        def formatTime(self, record, datefmt=None):
            ct = self.converter(record.created)
            if datefmt:
                s = time.strftime(datefmt, ct)
            else:
                t = time.strftime("%Y-%m-%d %H:%M:%S", ct)
                s = "%s,%03d" % (t, record.msecs)
            return s

    _log_formatter = CustomFormatter(
        fmt="%(asctime)s [%(levelname)-3s] [%(name)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    _file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
    _file_handler.setFormatter(_log_formatter)
    _file_handler.setLevel(logging.DEBUG)  # File always logs DEBUG

    _console_handler = logging.StreamHandler(sys.stderr)
    _console_handler.setFormatter(_log_formatter)
    _console_handler.setLevel(logging.INFO)  # Console defaults to INFO

    # Add the filter to prevent immediate duplicates
    duplicate_filter = ImmediateDuplicateFilter()
    _file_handler.addFilter(duplicate_filter)
    _console_handler.addFilter(duplicate_filter)

    _handlers_initialized = True

    # Add only the file handler to the root logger initially
    root_logger = logging.getLogger()
    root_logger.addHandler(_file_handler)
    root_logger.setLevel(logging.DEBUG)  # Root logger level is DEBUG to allow handlers to filter

    # Set specific library log levels higher to reduce noise
    logging.getLogger("pywebview").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    logging.getLogger("websockets.client").setLevel(logging.WARNING)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
    logging.getLogger("docling.backend.html_backend").setLevel(logging.WARNING)
    logging.getLogger("openai._base_client").setLevel(logging.WARNING)
    logging.getLogger("charset_normalizer").setLevel(logging.WARNING)
    logging.getLogger("filelock").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Gets a logger instance configured with standard file and console handlers."""
    _initialize_handlers()
    logger = logging.getLogger(name)
    # Individual loggers propagate to root, so set their level low
    # The root logger's level and handler levels control final output
    logger.setLevel(logging.DEBUG)
    return logger


def enable_console_logging():
    """Adds the console handler to the root logger if not already present."""
    _initialize_handlers()
    root_logger = logging.getLogger()
    if _console_handler and _console_handler not in root_logger.handlers:
        # Set level back to INFO when enabling, in case it was changed
        _console_handler.setLevel(logging.INFO)
        root_logger.addHandler(_console_handler)


def disable_console_logging():
    """Removes the console handler from the root logger if present."""
    _initialize_handlers()
    root_logger = logging.getLogger()
    if _console_handler and _console_handler in root_logger.handlers:
        root_logger.removeHandler(_console_handler)


# --- Initial Setup --- #
_initialize_handlers()  # Initialize handlers when module is loaded
module_logger = get_logger(__name__)
# Console logging is OFF by default after initial load
disable_console_logging()
