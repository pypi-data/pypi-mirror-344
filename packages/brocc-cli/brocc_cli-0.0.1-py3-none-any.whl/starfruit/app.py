import logging
import os
import re
import subprocess
import sys
import threading
import time
from typing import Optional

import httpx
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.css.query import NoMatches
from textual.widgets import Button, Footer, Header, TabbedContent

from starfruit.cli.cli_debug import CLIDebug
from starfruit.cli.cli_main import CLIMain
from starfruit.db.sqlite_manager import sqlite_manager
from starfruit.internal.const import API_HOST, API_PORT, PACKAGE_NAME
from starfruit.internal.get_update import get_update
from starfruit.internal.get_version import get_version
from starfruit.internal.internal_api_client import req_post
from starfruit.internal.logger import get_logger
from starfruit.internal.webview import (
    launch_webview,
    terminate_webview,
)
from starfruit.server.fastapi import run_server_in_thread

SIMULATE_UPDATE = False
SERVER_URL = f"http://{API_HOST}:{API_PORT}"

logger = get_logger(__name__)


class StarfruitApp(App):
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

    def compose(self) -> ComposeResult:
        yield Header()

        with TabbedContent("✦ menu", "✧ debug", id="main-tab"):
            yield CLIMain(self, id="main-tab")
            yield CLIDebug(id="debug-tab")

        yield Footer()

    def on_mount(self) -> None:
        self.theme = "catppuccin-mocha"

        try:
            self.app_main_ref = self.query_one("#main-tab", CLIMain)
        except NoMatches:
            logger.error("could not find main tab")

        self.server_thread = run_server_in_thread()
        if not self.server_thread:
            logger.error("failed to start server thread.")
        self._start_huey_consumer()
        self.run_worker(self._initial_update_check, thread=True, name="UpdateCheck")
        self.run_worker(self._initial_webview_launch, thread=True, name="WebviewInit")

    def _start_huey_consumer(self):
        """Starts the Huey consumer as a background process."""
        if self.huey_consumer_process and self.huey_consumer_process.poll() is None:
            logger.info("Huey consumer process already running.")
            return

        huey_instance_path = "starfruit.tasks.consumer.huey"
        # NOTE: We run the Huey consumer with its default settings (1 thread worker).
        command = [
            sys.executable,
            "-m",
            "huey.bin.huey_consumer",
            huey_instance_path,
        ]

        try:
            consumer_env = os.environ.copy()
            consumer_env["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
            # Use Popen to run in the background.
            self.huey_consumer_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,  # Capture stdout
                stderr=subprocess.PIPE,  # Capture stderr
                text=True,  # Decode stdout/stderr as text
                env=consumer_env,  # Pass the modified environment
            )
            logger.info(f"Huey consumer process started with PID: {self.huey_consumer_process.pid}")
            threading.Thread(
                target=self._monitor_subprocess_pipe,
                args=(self.huey_consumer_process.stdout, "Huey-stdout"),
                daemon=True,
                name="HueyStdoutMonitor",
            ).start()
            threading.Thread(
                target=self._monitor_subprocess_pipe,
                args=(self.huey_consumer_process.stderr, "Huey-stderr"),
                daemon=True,
                name="HueyStderrMonitor",
            ).start()
        except FileNotFoundError:
            logger.error(
                f"Error: Could not find '{command[0]}' or 'huey_consumer'. "
                "Make sure Huey is installed correctly in the environment."
            )
            self.huey_consumer_process = None
        except Exception as e:
            logger.error(f"Failed to start Huey consumer process: {e}", exc_info=True)
            self.huey_consumer_process = None

    def _monitor_subprocess_pipe(self, pipe, pipe_name: str):
        """Monitors a subprocess pipe (stdout/stderr) and logs its output,
        Attempting to parse the log level from the subprocess output.
        """
        # Regex to capture our standard log format from the consumer
        log_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}\s+\[(DBG|INF|WRN|ERR|CRT)\]\s+\[.*\]\s+(.*)")

        try:
            if pipe:
                for line in iter(pipe.readline, ""):
                    stripped_line = line.strip()
                    if not stripped_line:
                        continue

                    match = log_pattern.match(stripped_line)
                    if match:
                        level_str = match.group(1)
                        message = match.group(2)
                        # Map abbreviation back to logging level constant
                        level_map = {
                            "DBG": logging.DEBUG,
                            "INF": logging.INFO,
                            "WRN": logging.WARNING,
                            "ERR": logging.ERROR,
                            "CRT": logging.CRITICAL,
                        }
                        log_level = level_map.get(level_str, logging.INFO)  # Default to INFO
                        # Log using the parsed level
                        logger.log(log_level, f"[{pipe_name}] {message}")
                    else:
                        # If it doesn't match our format, log as INFO
                        logger.info(f"[{pipe_name}] {stripped_line}")

                pipe.close()
                logger.info(f"Pipe closed for {pipe_name}")
            else:
                logger.warning(f"Pipe object for {pipe_name} is None, cannot monitor.")
        except Exception as e:
            logger.error(f"Error monitoring subprocess pipe '{pipe_name}': {e}", exc_info=True)

    def _terminate_huey_consumer(self):
        """Attempts to terminate the Huey consumer process gracefully."""
        if self.huey_consumer_process and self.huey_consumer_process.poll() is None:
            logger.info(
                f"Terminating Huey consumer process (PID: {self.huey_consumer_process.pid})..."
            )
            try:
                self.huey_consumer_process.terminate()  # Send SIGTERM
                try:
                    # Wait a short time for graceful shutdown
                    self.huey_consumer_process.wait(timeout=5)
                    logger.info("Huey consumer process terminated gracefully.")
                except subprocess.TimeoutExpired:
                    logger.warning("Huey consumer did not terminate gracefully, killing...")
                    self.huey_consumer_process.kill()  # Send SIGKILL
                    self.huey_consumer_process.wait()  # Wait for kill
                    logger.info("Huey consumer process killed.")
            except Exception as e:
                logger.error(f"Error terminating Huey consumer process: {e}", exc_info=True)
        else:
            logger.debug("Huey consumer process not running or already terminated.")
        self.huey_consumer_process = None

    def _initial_webview_launch(self):
        """Worker: Waits for server, then launches or focuses webview."""
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
                return  # Don't try if server thread died
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
            return
        try:
            launch_webview(title="🥦")
        except Exception as e:
            logger.error(
                f"({threading.current_thread().name}) Error launching webview directly: {e}",
                exc_info=True,
            )

    def _initial_update_check(self):
        """Worker to check for updates and update UI if needed."""
        update_message = get_update(PACKAGE_NAME)
        if SIMULATE_UPDATE:
            update_message = (
                f"Update available → v2.0.0\n\nRun: [bold]pipx upgrade {PACKAGE_NAME}[/bold]"
            )
        if update_message and self.app_main_ref:
            self.call_from_thread(self.app_main_ref.show_alert, update_message)

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

        try:
            logger.info("attempting to terminate huey consumer process...")
            self._terminate_huey_consumer()
            logger.info("huey consumer termination attempt finished.")
        except Exception as huey_term_e:
            logger.error(f"error during huey consumer cleanup: {huey_term_e}")

        try:
            logger.info("Shutting down metadata manager...")
            sqlite_manager.shutdown()
            logger.info("Metadata manager shutdown complete.")
        except Exception as db_shutdown_e:
            logger.error(f"Error during metadata manager shutdown: {db_shutdown_e}")

        self.exit()


if __name__ == "__main__":
    app = StarfruitApp()
    app.run()
