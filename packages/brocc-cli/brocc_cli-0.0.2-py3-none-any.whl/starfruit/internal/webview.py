import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Optional

from starfruit.internal.const import INTERNAL_API_URL
from starfruit.internal.env import webview_url
from starfruit.internal.logger import get_logger

logger = get_logger(__name__)

_webview_process: Optional[subprocess.Popen] = None
_webview_active: bool = False


def launch_webview(title: str):
    """Launch the webview process and monitor it."""
    global _webview_active, _webview_process

    # If already running, don't launch again (API layer should handle focus)
    if is_webview_running():
        logger.debug("Webview launch requested, but process is already running.")
        return

    try:
        launcher_path = Path(__file__).parent.parent / "proc" / "proc_webview.py"

        if not launcher_path.exists():
            logger.error(f"Webview process script not found at: {launcher_path}")
            _webview_active = False
            _webview_process = None
            return

        python_exe = sys.executable
        current_pid = os.getpid()
        url = webview_url()
        webview_debug_enabled = True
        if not url:
            webview_debug_enabled = False
            url = INTERNAL_API_URL
        cmd = [
            python_exe,
            str(launcher_path),
            "--url",
            url,
            "--api-url",
            INTERNAL_API_URL,
            "--parent-pid",
            str(current_pid),
            "--title",
            title,
        ]
        if webview_debug_enabled:
            cmd.append("--debug")
        _webview_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line buffered
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        _webview_active = True
        logger.debug(f"Webview process launched with PID: {_webview_process.pid}")

        # Give it a moment to start and check if it exited immediately
        time.sleep(0.3)
        if _webview_process and _webview_process.poll() is not None:
            errors = ""
            if _webview_process.stderr:
                try:
                    errors = _webview_process.stderr.read()
                except Exception:
                    pass  # Ignore errors reading stderr here
            logger.error(
                f"Webview process failed to start quickly. Exit code: {_webview_process.returncode}. Stderr: {errors}"
            )
            _webview_active = False
            _webview_process = None
            return  # Failed to launch

        # Start monitor thread (reads output, updates status on exit)
        threading.Thread(
            target=_monitor_webview_process,
            args=(_webview_process,),  # Pass the specific process object
            daemon=True,
            name="webview-monitor",
        ).start()

    except Exception as e:
        logger.error(f"Failed to launch webview: {e}", exc_info=True)
        _webview_active = False
        _webview_process = None


def _monitor_webview_process(proc: subprocess.Popen):
    """Monitors a given webview process, reads its output, and updates status."""
    global _webview_active, _webview_process

    if not proc:
        return

    pid = proc.pid
    logger.debug(f"Monitoring webview process PID: {pid}")

    # Read stdout line by line
    if proc.stdout:
        try:
            for line in iter(proc.stdout.readline, ""):
                if line:
                    logger.debug(f"Webview process ({pid}): {line.strip()}")
                # If the process has exited while we are reading, break
                if proc.poll() is not None:
                    break
        except (IOError, ValueError) as e:  # ValueError for closed file descriptor
            logger.debug(f"Error reading from webview stdout ({pid}): {e}")
        finally:
            try:
                if proc.stdout and not proc.stdout.closed:
                    proc.stdout.close()
            except Exception:
                pass  # Ignore close errors

    # Wait for process to ensure it has fully exited
    try:
        proc.wait(timeout=0.5)  # Short wait, should already be done
    except subprocess.TimeoutExpired:
        logger.warning(f"Webview process {pid} did not exit cleanly after stdout closed.")
    except Exception as e:
        logger.debug(f"Error during final wait for webview {pid}: {e}")

    exit_code = proc.returncode
    logger.debug(f"Webview process ({pid}) exited with code: {exit_code}")

    # Read any remaining stderr
    error_output = ""
    if proc.stderr:
        try:
            error_output = proc.stderr.read()
            if error_output:
                logger.error(f"Webview process ({pid}) final stderr output:\n{error_output}")
        except (IOError, ValueError) as e:
            logger.debug(f"Error reading final stderr from webview ({pid}): {e}")
        finally:
            try:
                if proc.stderr and not proc.stderr.closed:
                    proc.stderr.close()
            except Exception:
                pass  # Ignore close errors

    # Update global state *only if* this is the currently tracked process
    # Prevents race conditions if a new process was launched quickly
    if _webview_process and _webview_process.pid == pid:
        logger.debug(f"Updating global state for exited webview process {pid}")
        _webview_active = False
        _webview_process = None
    else:
        logger.debug(
            f"Exited webview process {pid} is not the current global process, state not updated."
        )


def terminate_webview():
    """Terminate the webview process gracefully, with fallback to kill."""
    global _webview_active, _webview_process

    # Capture current process to avoid race condition if it changes mid-function
    proc_to_terminate = _webview_process

    if not proc_to_terminate:
        logger.debug("No webview process to terminate")
        return

    pid = proc_to_terminate.pid
    logger.debug(f"Attempting to terminate webview process (PID: {pid})")

    try:
        if proc_to_terminate.poll() is None:
            logger.debug(f"Sending SIGTERM to webview process {pid}")
            proc_to_terminate.terminate()
            try:
                # Wait for termination
                proc_to_terminate.wait(1.0)
                logger.debug(f"Webview process (PID: {pid}) terminated gracefully after SIGTERM.")
            except subprocess.TimeoutExpired:
                # Force kill if terminate didn't work
                logger.warning(
                    f"Webview process (PID: {pid}) did not terminate after SIGTERM, sending SIGKILL"
                )
                proc_to_terminate.kill()
                try:
                    # Wait briefly after kill
                    proc_to_terminate.wait(0.5)
                    logger.debug(f"Webview process (PID: {pid}) terminated after SIGKILL.")
                except Exception as e_inner:
                    logger.warning(f"Error waiting after killing webview process {pid}: {e_inner}")
        else:
            logger.debug(
                f"Webview process (PID: {pid}) already terminated (poll={proc_to_terminate.poll()})."
            )

    except Exception as e:
        logger.error(f"Error during webview termination for PID {pid}: {e}", exc_info=True)
    finally:
        # Update state *only if* we were trying to terminate the currently active process
        if _webview_process and _webview_process.pid == pid:
            logger.debug(
                f"Clearing global webview state for PID {pid}. Active was: {_webview_active}"
            )
            _webview_active = False
            _webview_process = None
        else:
            logger.debug(
                f"Global state for PID {pid} not cleared; current process is {_webview_process.pid if _webview_process else 'None'}."
            )


def is_webview_running() -> bool:
    """Check if the managed webview process is currently running."""
    global _webview_active, _webview_process

    if not _webview_process:
        if _webview_active:  # Correct inconsistent state
            logger.warning(
                "is_webview_running: _webview_active is True but _webview_process is None. Resetting."
            )
            _webview_active = False
        return False

    poll_result = _webview_process.poll()

    if poll_result is None:
        # Process is running
        if not _webview_active:
            logger.warning(
                f"is_webview_running: Process {_webview_process.pid} running but _webview_active is False. Correcting."
            )
            _webview_active = True
        return True
    else:
        # Process is not running
        if _webview_active:
            logger.warning(
                f"is_webview_running: Process {_webview_process.pid} exited (code {poll_result}) but _webview_active is True. Correcting."
            )
            _webview_active = False
            # Don't clear _webview_process here, let monitor/terminate handle it
        return False


def get_webview_status() -> dict:
    """Return the current status of the webview process."""
    running = is_webview_running()
    pid = _webview_process.pid if _webview_process else None
    # Make status reflect reality more closely
    return {
        "active": _webview_active and running,
        "process_running": running,
        "pid": pid if running else None,
    }


def get_webview_pid() -> Optional[int]:
    """Return the PID of the running webview process, if any."""
    if is_webview_running() and _webview_process:
        return _webview_process.pid
    return None
