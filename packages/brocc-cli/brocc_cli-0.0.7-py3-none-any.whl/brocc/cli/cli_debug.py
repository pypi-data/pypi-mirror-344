from io import StringIO
from pathlib import Path

import httpx
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Log, Static

from brocc.internal.const import API_HOST, API_PORT
from brocc.internal.logger import LOG_FILE, get_logger

logger = get_logger(__name__)


API_BASE_URL = f"http://{API_HOST}:{API_PORT}"
OPEN_LOG_FILE_URL = f"{API_BASE_URL}/open_log_file"
OPEN_APP_DIR_URL = f"{API_BASE_URL}/open_app_dir"


class CLIDebug(Static):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._log_file_path: Path = LOG_FILE
        self._log_file_handle: StringIO | None = None
        self._last_log_position: int = 0

    def compose(self) -> ComposeResult:
        with Vertical(id="logs-container"):
            yield Log(highlight=True, auto_scroll=True, id="app-logs")
            with Horizontal(id="logs-buttons-container"):
                yield Button("Open .log file", id="open-log-file-btn", name="open_log_file")
                yield Button("Open app dir", id="open-app-dir-btn", name="open_app_dir")

    def on_mount(self) -> None:
        # Load initial logs and start watching
        self._load_initial_logs()
        self.set_interval(0.5, self._watch_log_file)  # Check every 500ms

    def _load_initial_logs(self) -> None:
        log_widget = self.query_one("#app-logs", Log)
        try:
            with open(self._log_file_path, "r", encoding="utf-8") as f:
                log_content = f.read()
                log_widget.write(log_content)
                self._last_log_position = f.tell()
        except Exception as e:
            log_widget.write(f"Error loading log file {self._log_file_path}: {e}")
            logger.error(f"Error loading log file {self._log_file_path}: {e}")

    def _watch_log_file(self) -> None:
        """Periodically check the log file for new content and append it."""
        log_widget = self.query_one("#app-logs", Log)
        try:
            with open(self._log_file_path, "r", encoding="utf-8") as f:
                f.seek(self._last_log_position)
                new_content = f.read()
                if new_content:
                    log_widget.write(new_content)
                    self._last_log_position = f.tell()
        except Exception as e:
            logger.error(f"Error reading log file {self._log_file_path}: {e}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.name == "open_log_file":
            self.action_open_log_file()
        elif event.button.name == "open_app_dir":
            self.action_open_app_dir()

    def _make_api_call(self, url: str, action_name: str):
        """Helper to make POST request to an action endpoint."""
        try:
            logger.debug(f"Attempting to call API action: {action_name} at {url}")
            with httpx.Client() as client:
                response = client.post(url, timeout=10.0)
                response.raise_for_status()  # Raise exception for 4xx/5xx errors
            logger.info(f"Successfully triggered action '{action_name}' via API.")
        except httpx.RequestError as req_err:
            logger.error(
                f"Failed to trigger action '{action_name}' via API (request error): {req_err}"
            )
        except httpx.HTTPStatusError as status_err:
            logger.error(
                f"Failed to trigger action '{action_name}' via API (status {status_err.response.status_code}): {status_err.response.text[:200]}"
            )
        except Exception as e:
            logger.error(
                f"Unexpected error triggering action '{action_name}' via API: {e}", exc_info=True
            )

    def action_open_log_file(self) -> None:
        """Calls the API to open the log file."""
        self._make_api_call(OPEN_LOG_FILE_URL, "open_log_file")

    def action_open_app_dir(self) -> None:
        """Calls the API to open the application directory."""
        self._make_api_call(OPEN_APP_DIR_URL, "open_app_dir")
