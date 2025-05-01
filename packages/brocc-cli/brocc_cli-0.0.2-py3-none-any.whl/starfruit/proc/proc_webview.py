#!/usr/bin/env python
"""
standalone script to run the webview in its own process.
this ensures it has its own main thread, required for macOS.
"""

import argparse
import atexit
import json
import os
import platform
import signal
import sys
import threading
import time
import urllib.error
import urllib.request

import psutil
import webview

# --- Argument Parsing ---
parser = argparse.ArgumentParser(description="starfruit webview process")
parser.add_argument("--url", type=str, required=True, help="webview url")
parser.add_argument("--api-url", type=str, required=True, help="api url")
parser.add_argument("--parent-pid", type=int, required=True, help="Parent process ID to monitor")
parser.add_argument("--title", type=str, default="✧ starfruit ✦", help="Webview window title")
parser.add_argument("--debug", action="store_true", help="Enable webview debug mode")
args = parser.parse_args()

# --- Config from Args ---
URL = args.url
API_URL = args.api_url
PARENT_PID_ARG = args.parent_pid
TITLE = args.title

LOG_ENDPOINT = f"{API_URL}/log"
_LOGGER_NAME = "proc_webview"


def log(level: str, message: str):
    """Sends a log message to the main server's /log endpoint."""
    try:
        data = json.dumps(
            {
                "level": level,
                "message": str(message),  # Ensure message is string
                "logger_name": _LOGGER_NAME,
            }
        ).encode("utf-8")

        req = urllib.request.Request(
            LOG_ENDPOINT, data=data, headers={"Content-Type": "application/json"}, method="POST"
        )
        with urllib.request.urlopen(req, timeout=1) as response:  # Short timeout
            if response.status != 204:
                print(
                    f"[proc_webview_stderr] Log endpoint failed with status {response.status}: {message}",
                    file=sys.stderr,
                )
    except urllib.error.URLError as e:
        print(
            f"[proc_webview_stderr] Failed to connect to log endpoint ({LOG_ENDPOINT}): {e}. Log: {level} - {message}",
            file=sys.stderr,
        )
    except Exception as e:
        # Catch potential JSON errors, timeouts, etc.
        print(
            f"[proc_webview_stderr] Error sending log ({LOG_ENDPOINT}): {e}. Log: {level} - {message}",
            file=sys.stderr,
        )


class RemoteLogger:
    def debug(self, msg):
        log("debug", msg)

    def info(self, msg):
        log("info", msg)

    def warning(self, msg):
        log("warning", msg)

    def error(self, msg, exc_info=None):  # exc_info not easily transferable, log message only
        if exc_info and isinstance(msg, Exception):
            log("error", f"{type(msg).__name__}: {msg}")
        elif exc_info:
            log("error", f"{msg} (Exception info not sent remotely)")
        else:
            log("error", msg)

    def exception(self, msg):
        # Similar limitation to error with exc_info=True
        log("error", f"{msg} (Exception trace not sent remotely)")


logger = RemoteLogger()

window = None
shutting_down = False
parent_pid = PARENT_PID_ARG


def signal_handler(sig, frame):
    global shutting_down
    logger.info(f"Received signal {sig}, closing webview")
    shutting_down = True
    cleanup()
    sys.exit(0)


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

#  Windows-specific signal handlers
if platform.system() == "Windows":
    try:
        # Use getattr to avoid linter errors
        win_break_signal = getattr(signal, "SIGBREAK", None)
        if win_break_signal is not None:
            signal.signal(win_break_signal, signal_handler)
    except (AttributeError, ValueError):
        # SIGBREAK doesn't exist or can't be used on this Windows installation
        logger.warning("SIGBREAK signal not available on this Windows installation.")


def cleanup():
    global window, shutting_down
    shutting_down = True

    # First destroy the window to release all UI resources
    if window and hasattr(webview, "windows") and webview.windows:
        try:
            logger.info("Destroying window on exit")
        except Exception as e:
            # Use error method, exc_info is implicitly handled (message only)
            logger.error(f"Error destroying window: {e}")

    # Force exit the process after cleanup to ensure nothing keeps it alive
    logger.info("Cleanup complete - exiting process")
    # Give a moment for cleanup to complete before exit
    threading.Timer(1.0, lambda: os._exit(0)).start()


atexit.register(cleanup)


def on_window_close():
    global shutting_down
    shutting_down = True
    # This will trigger the atexit handler after the function completes
    sys.exit(0)


def monitor_parent_process():
    """Monitor the parent process and exit if it terminates"""
    global shutting_down, parent_pid

    if parent_pid is None:
        # This case should not happen anymore as parent_pid is required arg
        logger.error("Parent PID not provided via arguments, cannot monitor.")
        return

    logger.info(f"Starting parent process monitor for PID: {parent_pid}")

    while not shutting_down:
        try:
            # Check if parent process exists
            if not psutil.pid_exists(parent_pid):
                logger.info(f"Parent process (PID: {parent_pid}) no longer exists, shutting down")
                shutting_down = True
                cleanup()
                os._exit(0)  # Force exit

            # Check if parent is zombie/dead but still in process table
            try:
                parent = psutil.Process(parent_pid)
                if parent.status() == psutil.STATUS_ZOMBIE:
                    logger.info("Parent process is zombie, shutting down")
                    shutting_down = True
                    cleanup()
                    os._exit(0)  # Force exit
            except psutil.NoSuchProcess:
                logger.info("Parent process no longer exists (race condition), shutting down")
                shutting_down = True
                cleanup()
                os._exit(0)  # Force exit

        except Exception as e:
            logger.error(f"Error monitoring parent process: {e}")
            # Don't exit on monitoring errors

        # Check every second
        time.sleep(1)


if __name__ == "__main__":

    def delayed_watchdog():
        global shutting_down, window
        # Give the app 30 seconds to properly initialize
        time.sleep(30)
        # If we're still running (GUI is active) after 30 seconds, don't exit
        if not shutting_down and window is None:
            logger.error("Watchdog: Window failed to initialize after 30 seconds. Exiting.")
            os._exit(1)  # Force exit if window never appears

    # Start watchdog timer
    threading.Thread(target=delayed_watchdog, daemon=True).start()
    # Start parent process monitor
    threading.Thread(target=monitor_parent_process, daemon=True).start()
    # Create and start the window
    try:
        # Check if create_window exists
        if hasattr(webview, "create_window"):
            window = webview.create_window(
                TITLE, URL, width=420, height=800, resizable=True, on_top=False
            )
            # Set on_close handler if supported
            if hasattr(window, "events") and hasattr(window.events, "closed"):
                window.events.closed += on_window_close
            # Use the debug flag passed via command-line arguments
            logger.info(f"Starting webview with debug={args.debug}")
            webview.start(func=lambda: None, debug=args.debug)
            logger.info("Webview closed")
            # If we get here, it means the webview loop has ended
            # Make sure we exit
            on_window_close()
        else:
            logger.error("ERROR: The webview module doesn't have create_window attribute")
            logger.error(f"Available attributes: {dir(webview)}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"ERROR creating window: {e}")
        # logger.exception sends error level log with simplified message
        logger.exception(f"Traceback for error creating window: {e}")
        sys.exit(1)
