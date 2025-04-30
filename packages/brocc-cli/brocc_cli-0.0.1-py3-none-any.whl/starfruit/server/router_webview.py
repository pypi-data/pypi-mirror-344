import platform
import subprocess

import psutil
from fastapi import APIRouter

from starfruit.internal.logger import get_logger
from starfruit.internal.webview import (
    get_webview_pid,
    get_webview_status,
    is_webview_running,
    launch_webview,
    terminate_webview,
)

logger = get_logger(__name__)


router = APIRouter(prefix="/webview")


@router.post("/focus")
async def focus_webview():
    # Use internal check
    if not is_webview_running():
        return {"status": "not_running", "message": "No webview process is running"}

    # Call focus helper (which now uses internal pid getter)
    if _focus_webview_window():
        return {"status": "focused", "message": "Brought webview to the foreground"}
    else:
        return {"status": "error", "message": "Couldn't focus webview window"}


@router.post("/launch_or_focus")
async def launch_or_focus_webview():
    logger.debug("Received request to launch or focus webview.")
    if is_webview_running():
        logger.info("Webview is running, attempting to focus.")
        if _focus_webview_window():
            return {"status": "focused", "message": "Brought existing webview to foreground"}
        else:
            # Focus failed, maybe the window is gone but process lingers?
            # Try launching again as a fallback?
            # For now, return error if focus fails
            logger.warning("Focus attempt failed even though process seems running.")
            return {
                "status": "error",
                "message": "Webview process running, but couldn't focus window",
            }
    else:
        logger.info("Webview not running, attempting to launch.")
        try:
            # TODO: Make title configurable or pull from constants?
            launch_webview(title="🥦")
            # Give it a tiny moment to potentially start before reporting success
            # Note: launch_webview is async internally with its monitor thread
            return {
                "status": "launched",
                "message": "Webview launch initiated.",
            }  # Indicate launch was *started*
        except Exception as e:
            logger.error(f"Error launching webview via API: {e}", exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to initiate webview launch: {e}",
            }


@router.get("/status")
async def webview_status():
    # Get status directly from internal module
    return get_webview_status()


@router.post("/close")
async def close_webview():
    if not is_webview_running():
        return {"status": "not_running", "message": "No webview process is running"}

    try:
        # Call internal termination function
        terminate_webview()
        return {"status": "closed", "message": "Webview process terminated"}
    except Exception as e:
        logger.error(f"Error closing webview via API: {e}")
        return {"status": "error", "message": f"Error closing webview: {e}"}


# --- Helper Functions ---
def _focus_webview_window() -> bool:
    """
    Platform-specific function to focus the webview window
    Returns True if successful, False otherwise
    """
    webview_pid = get_webview_pid()

    if not webview_pid:
        logger.debug("Focus requested but no webview PID found.")
        return False

    try:
        system = platform.system()

        if system == "Darwin":  # macOS
            script = f"""
            tell application \"System Events\"
                set frontmost of every process whose unix id is {webview_pid} to true
            end tell
            """
            subprocess.run(["osascript", "-e", script], check=False, capture_output=True)
            logger.debug(f"Attempted to focus macOS webview window for PID {webview_pid}")
            # osascript doesn't reliably indicate success, assume it worked if no error
            return True

        elif system == "Windows":
            try:
                proc = psutil.Process(webview_pid)
                ps_cmd = f"(Get-Process -Id {proc.pid} | Where-Object {{$_.MainWindowTitle}} | ForEach-Object {{ (New-Object -ComObject WScript.Shell).AppActivate($_.MainWindowTitle) }})"
                result = subprocess.run(
                    ["powershell", "-command", ps_cmd], check=False, capture_output=True, text=True
                )
                logger.debug(
                    f"Attempted to focus Windows webview window for PID {webview_pid}. Result: {result.returncode}, Output: {result.stdout}, Error: {result.stderr}"
                )
                # Powershell might return non-zero even if activation worked partially
                return True  # Assume success if command ran
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                logger.error(
                    f"Could not focus webview window (PID {webview_pid}) - process error: {e}"
                )
                return False
            except FileNotFoundError:
                logger.error("Could not focus webview window - powershell not found?")
                return False

        elif system == "Linux":
            try:
                # Use psutil to check process exists before calling wmctrl
                if not psutil.pid_exists(webview_pid):
                    logger.error(
                        f"Could not focus webview window (PID {webview_pid}) - process does not exist."
                    )
                    return False
                # Try using wmctrl (if installed)
                result = subprocess.run(
                    ["wmctrl", "-i", "-a", str(webview_pid)],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                logger.debug(
                    f"Attempted to focus Linux webview window via wmctrl for PID {webview_pid}. Result: {result.returncode}, Output: {result.stdout}, Error: {result.stderr}"
                )
                if result.returncode == 0:
                    return True
                else:
                    logger.warning(
                        f"wmctrl failed for PID {webview_pid}, trying xdotool as fallback."
                    )
                    # Try xdotool as a fallback (requires PID lookup for window ID)
                    # This is more complex and less reliable, skipping for now
                    return False  # Consider wmctrl failure as focus failure

            except FileNotFoundError:
                logger.error(
                    f"Could not focus webview window (PID {webview_pid}) - wmctrl (or potentially xdotool) not found."
                )
                return False
            except Exception as e:  # Catch broader exceptions during Linux focus
                logger.error(f"Error focusing Linux webview window (PID {webview_pid}): {e}")
                return False

        logger.warning(f"No focus implementation attempted for platform: {system}")
        return False

    except Exception as e:
        logger.error(f"Error focusing webview window (PID: {webview_pid}): {e}", exc_info=True)
        return False
