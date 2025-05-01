import subprocess
import threading
import time
from typing import Optional

import httpx
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.css.query import NoMatches
from textual.widgets import Button, Footer, Header, TabbedContent

from brocc.cli.cli_debug import CLIDebug
from brocc.cli.cli_main import CLIMain
from brocc.internal.const import API_HOST, API_PORT
from brocc.internal.get_version import get_version
from brocc.internal.internal_api_client import req_post
from brocc.internal.logger import get_logger
from brocc.internal.webview import (
    launch_webview,
    terminate_webview,
)
from brocc.lifecycle import (
    check_for_updates,
    shutdown_db,
    start_huey_consumer,
    start_server,
    terminate_huey_consumer,
)

SIMULATE_UPDATE = False
SERVER_URL = f"http://{API_HOST}:{API_PORT}"

logger = get_logger(__name__)


class BroccApp(App):
    TITLE = f"✧ 🥦 v{get_version()}"
    BINDINGS = [
        Binding(
            key="ctrl+c",
            action="quit",
            description="Quit App",
            show=False,
        ),
        Binding(
            key="ctrl+q",
            action="quit",
            description="Quit App",
            show=True,
        ),
    ]
    CSS_PATH = ["app.tcss"]
    server_thread: Optional[threading.Thread] = None
    huey_consumer_process: Optional[subprocess.Popen] = None
    app_main_ref: Optional[CLIMain] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent("✦ menu", "✧ debug", id="main-tab"):
            yield CLIMain(self, id="main-tab-content")
            yield CLIDebug(id="debug-tab")
        yield Footer()

    def on_mount(self) -> None:
        self.theme = "catppuccin-mocha"
        try:
            self.app_main_ref = self.query_one("#main-tab-content", CLIMain)
        except NoMatches:
            logger.error("could not find main tab content")
            self.app_main_ref = None

        self.server_thread = start_server()
        self.huey_consumer_process = start_huey_consumer()

        update_message = check_for_updates()
        if update_message and self.app_main_ref:
            self.call_from_thread(self.app_main_ref.show_alert, update_message)

        self.run_worker(self._initial_webview_launch, thread=True, name="WebviewInit")

    def _initial_webview_launch(self):
        health_url = f"{SERVER_URL}/health"
        server_ready = False
        max_wait_seconds = 10
        poll_interval = 0.2
        start_wait = time.time()
        logger.info(f"({threading.current_thread().name}) Waiting for server at {health_url}...")

        while time.time() - start_wait < max_wait_seconds:
            if not self.server_thread or not self.server_thread.is_alive():
                logger.error(
                    f"({threading.current_thread().name}) Server thread terminated unexpectedly. Aborting webview launch."
                )
                return
            try:
                response = httpx.get(health_url, timeout=0.5)
                if response.status_code == 200:
                    server_ready = True
                    break
                else:
                    logger.debug(
                        f"({threading.current_thread().name}) Server not ready yet (status {response.status_code}), retrying..."
                    )
            except httpx.RequestError:
                logger.debug(
                    f"({threading.current_thread().name}) Server not ready yet (connection error), retrying..."
                )
            time.sleep(poll_interval)
        if not server_ready:
            logger.error(
                f"({threading.current_thread().name}) Server failed to become ready after {max_wait_seconds} seconds. Cannot initialize webview."
            )
            if self.app_main_ref:
                self.call_from_thread(
                    self.app_main_ref.show_alert,
                    "[bold red]Error:[/bold red] Server failed to start. Webview unavailable.",
                )
            return
        try:
            launch_webview(title="🥦")
        except Exception as e:
            logger.error(
                f"({threading.current_thread().name}) Error launching webview directly: {e}",
                exc_info=True,
            )
            if self.app_main_ref:
                self.call_from_thread(
                    self.app_main_ref.show_alert,
                    f"[bold red]Error:[/bold red] Failed to launch webview: {e}",
                )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_name = event.button.name
        if button_name == "open_webapp":
            logger.info(f"Button '{button_name}' pressed. Requesting webview focus.")
            thread = threading.Thread(target=self._request_webview_focus, daemon=True)
            thread.start()

    def _request_webview_focus(self):
        response = req_post("/webview/launch_or_focus", caller_logger=logger)
        if response:
            try:
                result = response.json()
                logger.info(
                    f"({threading.current_thread().name}) Focus webview request successful: {result.get('message', 'No message')}"
                )
            except Exception as e:
                logger.error(
                    f"({threading.current_thread().name}) Error processing focus webview response: {e}",
                    exc_info=True,
                )
        else:
            logger.error(f"({threading.current_thread().name}) Failed to focus webview via API.")

    async def action_quit(self) -> None:
        try:
            logger.info("attempting to clean up webview process...")
            terminate_webview()
            logger.info("webview cleanup function called.")
        except Exception as webview_term_e:
            logger.error(f"error during webview cleanup: {webview_term_e}")

        terminate_huey_consumer(self.huey_consumer_process)
        shutdown_db()

        self.exit()


if __name__ == "__main__":
    app = BroccApp()
    app.run()
