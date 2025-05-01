"""Core application lifecycle management (server, tasks, db)."""

import logging
import os
import re

# Add signal and time imports
import signal
import subprocess
import sys
import threading
import time
from typing import IO, Optional

from brocc.db.sqlite_manager import sqlite_manager
from brocc.internal.const import PACKAGE_NAME
from brocc.internal.get_update import get_update
from brocc.internal.logger import get_logger
from brocc.server.fastapi import run_server_in_thread

logger = get_logger(__name__)

# Flag to signal termination
_should_terminate = threading.Event()


# --- Signal Handling ---
def _handle_signal(signum, frame):
    """Signal handler to initiate graceful shutdown."""
    logger.info(f"Received signal {signal.Signals(signum).name}. Initiating shutdown...")
    _should_terminate.set()


# --- Headless Runner ---
def run_headless():
    """Runs the application core components without the TUI."""
    logger.info("Starting application in HEADLESS mode.")

    # Setup signal handlers
    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    server_thread = None
    huey_process = None

    try:
        # Start core components
        server_thread = start_server()
        huey_process = start_huey_consumer()

        if not server_thread or not huey_process:
            logger.critical("Failed to start critical components. Exiting.")
            # Attempt cleanup even if startup failed
            raise SystemExit(1)  # Use SystemExit for clearer exit intent

        # Check for updates and log
        update_message = check_for_updates()
        if update_message:
            # Log update availability clearly in headless mode
            logger.info(f"-- UPDATE AVAILABLE --\n{update_message}")

        logger.info("Headless application running. Press Ctrl+C to exit.")

        # Wait for termination signal
        while not _should_terminate.is_set():
            # Check if critical components are still alive
            if server_thread and not server_thread.is_alive():
                logger.warning("Server thread unexpectedly terminated.")
                _should_terminate.set()
                break
            if huey_process and huey_process.poll() is not None:
                logger.warning(
                    f"Huey process unexpectedly terminated with code {huey_process.poll()}."
                )
                _should_terminate.set()
                break
            # Sleep briefly to avoid busy-waiting
            time.sleep(0.5)

    except Exception as e:
        logger.error(f"Unhandled exception during headless run: {e}", exc_info=True)
        _should_terminate.set()  # Ensure cleanup runs
    finally:
        logger.info("Starting headless shutdown sequence...")
        # Terminate components (order might matter)
        terminate_huey_consumer(huey_process)
        # Server thread is daemon, should exit automatically
        shutdown_db()
        logger.info("Headless shutdown complete.")


# --- Server Lifecycle ---


def start_server() -> Optional[threading.Thread]:
    """Starts the FastAPI server in a daemon thread."""
    logger.info("Starting server thread...")
    server_thread = run_server_in_thread()
    if not server_thread:
        logger.error("Failed to start server thread.")
        return None
    logger.info("Server thread started.")
    return server_thread


# --- Huey Consumer Lifecycle ---


def _monitor_subprocess_pipe(pipe: Optional[IO[str]], pipe_name: str):
    """Monitors a subprocess pipe (stdout/stderr) and logs its output,
    Attempting to parse the log level from the subprocess output.
    """
    if not pipe:
        logger.warning(f"Pipe object for {pipe_name} is None, cannot monitor.")
        return

    # Regex to capture our standard log format from the consumer
    log_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}\s+\[(DBG|INF|WRN|ERR|CRT)\]\s+\[.*?\]\s+(.*)")

    try:
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
    except Exception as e:
        logger.error(f"Error monitoring subprocess pipe '{pipe_name}': {e}", exc_info=True)


def start_huey_consumer() -> Optional[subprocess.Popen]:
    """Starts the Huey consumer as a background process."""
    logger.info("Attempting to start Huey consumer process...")
    huey_instance_path = "brocc.tasks.consumer.huey"
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
        huey_process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,  # Capture stdout
            stderr=subprocess.PIPE,  # Capture stderr
            text=True,  # Decode stdout/stderr as text
            env=consumer_env,  # Pass the modified environment
        )
        logger.info(f"Huey consumer process started with PID: {huey_process.pid}")
        # Start monitoring threads
        threading.Thread(
            target=_monitor_subprocess_pipe,
            args=(huey_process.stdout, "consumer"),
            daemon=True,
            name="HueyStdoutMonitor",
        ).start()
        threading.Thread(
            target=_monitor_subprocess_pipe,
            args=(huey_process.stderr, "consumer"),
            daemon=True,
            name="HueyStderrMonitor",
        ).start()
        return huey_process
    except FileNotFoundError:
        logger.error(
            f"Error: Could not find '{command[0]}' or 'huey_consumer'. "
            "Make sure Huey is installed correctly in the environment."
        )
        return None
    except Exception as e:
        logger.error(f"Failed to start Huey consumer process: {e}", exc_info=True)
        return None


def terminate_huey_consumer(huey_process: Optional[subprocess.Popen]):
    """Attempts to terminate the Huey consumer process gracefully."""
    if huey_process and huey_process.poll() is None:
        logger.info(f"Terminating Huey consumer process (PID: {huey_process.pid})...")
        try:
            huey_process.terminate()  # Send SIGTERM
            try:
                # Wait a short time for graceful shutdown
                huey_process.wait(timeout=5)
                logger.info("Huey consumer process terminated gracefully.")
            except subprocess.TimeoutExpired:
                logger.warning("Huey consumer did not terminate gracefully, killing...")
                huey_process.kill()  # Send SIGKILL
                huey_process.wait()  # Wait for kill
                logger.info("Huey consumer process killed.")
        except Exception as e:
            logger.error(f"Error terminating Huey consumer process: {e}", exc_info=True)
    else:
        logger.debug("Huey consumer process not running or already terminated.")


# --- DB Lifecycle ---


def shutdown_db():
    """Shuts down the metadata manager."""
    logger.info("Shutting down metadata manager...")
    try:
        sqlite_manager.shutdown()
        logger.info("Metadata manager shutdown complete.")
    except Exception as db_shutdown_e:
        logger.error(f"Error during metadata manager shutdown: {db_shutdown_e}")


# --- Update Check ---


def check_for_updates() -> Optional[str]:
    """Checks for application updates."""
    logger.debug("Checking for updates...")
    try:
        # TODO: Make SIMULATE_UPDATE configurable if needed for testing
        # SIMULATE_UPDATE = False
        # if SIMULATE_UPDATE:
        #     return f"Update available → v2.0.0\n\nRun: [bold]pipx upgrade {PACKAGE_NAME}[/bold]"
        update_message = get_update(PACKAGE_NAME)
        if update_message:
            logger.info(f"Update available: {update_message}")
        else:
            logger.debug("No updates found.")
        return update_message
    except Exception as e:
        logger.error(f"Failed to check for updates: {e}", exc_info=True)
        return None
