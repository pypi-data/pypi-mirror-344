import asyncio
import time
from typing import Dict, List

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request

from starfruit.browser.chrome_process import launch_chrome, quit_chrome
from starfruit.browser.tab_monitor import (
    TabMonitorStatusRes,
    chrome_manager,
    tab_monitor,
)
from starfruit.internal.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/chrome")


async def try_initial_connect(quiet=True):
    """Try to auto-connect to Chrome on server start asynchronously"""
    try:
        # Use imported instance
        state = await chrome_manager.refresh_state()
        if state.has_debug_port:
            # Use imported instance
            is_connected = await chrome_manager.ensure_connection()
            if is_connected:
                if not quiet:
                    logger.debug("Successfully auto-connected to Chrome on server start")
                return True
    except Exception as e:
        if not quiet:
            logger.error(f"Error during initial auto-connect: {e}")
    return False


def try_initial_connect_sync(quiet=True):
    """Synchronous wrapper for try_initial_connect for backward compatibility"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(try_initial_connect(quiet=quiet))
    finally:
        loop.close()


# --- Chrome Manager API ---
@router.get("/status")
async def chrome_status():
    """Get the current status of Chrome connection"""
    try:
        # Use imported instance
        await chrome_manager.refresh_state()
    except Exception as e:
        logger.error(f"Error refreshing Chrome state: {e}")

    # Use imported instance
    status_code = await chrome_manager.status_code()

    return {
        "status_code": status_code.value,
        "timestamp": time.time(),
    }


@router.post("/launch")
async def chrome_launch_endpoint(
    request: Request, background_tasks: BackgroundTasks, force_relaunch: bool = False
):
    """
    Launch Chrome with a debug port or connect to an existing instance.
    ... (endpoint logic remains the same, uses helper)
    """
    if not force_relaunch:
        try:
            body = await request.json()
            if isinstance(body, dict) and "force_relaunch" in body:
                force_relaunch = bool(body["force_relaunch"])
        except Exception:
            pass
    if not force_relaunch:
        try:
            # Use imported instance
            chrome_connected = chrome_manager.connected
            if chrome_connected:
                return {"status": "already_connected", "message": "Already connected to Chrome"}
        except Exception as e:
            logger.debug(f"Error checking Chrome connection: {e}")

    async def run_in_thread():
        try:
            # Pass the imported manager to the helper if needed, or ensure helper uses it
            await _launch_chrome_in_thread(force_relaunch)
        except Exception as e:
            logger.error(f"Error running Chrome launch in thread: {e}")

    background_tasks.add_task(run_in_thread)

    return {
        "status": "launching",
        "message": f"{'Relaunching' if force_relaunch else 'Launching'} Chrome in background",
    }


async def _launch_chrome_in_thread(force_relaunch: bool = False):
    """Launch or relaunch Chrome in a background thread"""
    try:
        logger.debug(f"Starting Chrome {'relaunch' if force_relaunch else 'launch'} process")
        # Use imported instance
        state = await chrome_manager.refresh_state()
        logger.debug(
            f"Chrome state: running={state.is_running}, has_debug_port={state.has_debug_port}"
        )

        if force_relaunch or (state.is_running and not state.has_debug_port):
            logger.debug("Quitting existing Chrome instances")
            quit_success = await quit_chrome()
            if not quit_success:
                logger.error("Failed to quit existing Chrome instances")
                return
            logger.debug("Successfully quit existing Chrome instances")
            needs_launch = True
        else:
            needs_launch = not state.is_running
            logger.debug(f"Chrome needs launch: {needs_launch}")

        if needs_launch:
            logger.debug("Launching Chrome with debug port")
            launch_success = await launch_chrome()
            if not launch_success:
                logger.error("Failed to launch Chrome")
                return
            wait_time = 3 if force_relaunch else 2
            logger.debug(f"Waiting {wait_time}s for Chrome to initialize")
            await asyncio.sleep(wait_time)
        else:
            logger.debug("Chrome already running with debug port, skipping launch")

        logger.debug("Attempting to connect to Chrome")
        try:
            # Use imported instance
            connected = await chrome_manager.ensure_connection()
            if connected:
                logger.debug("Successfully connected to Chrome")
            else:
                logger.error("Failed to connect to Chrome")
        except Exception as e:
            logger.error(f"Error connecting to Chrome: {e}")
    except Exception as e:
        logger.error(f"Error in Chrome launch thread: {e}")
        import traceback

        logger.error(f"Stack trace: {traceback.format_exc()}")


# --- Tab Monitoring API ---
@router.get("/monitoring/status", response_model=TabMonitorStatusRes)
async def get_monitoring_status():
    """Get the current status of the tab monitoring service"""
    # Use imported instance
    return tab_monitor.get_status()


@router.post("/monitoring/start")
async def start_monitoring():
    """Start the tab monitoring service"""
    # Use imported instance
    success = await tab_monitor.start_monitoring()
    if success:
        return {"status": "started", "message": "Tab monitoring started successfully"}
    else:
        # Use imported instance
        status = tab_monitor.get_status()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start tab monitoring: {status.status} - {status.details or 'unknown error'}",
        )


@router.post("/monitoring/stop")
async def stop_monitoring():
    """Stop the tab monitoring service"""
    # Use imported instance
    success = await tab_monitor.stop_monitoring()
    if success:
        return {"status": "stopped", "message": "Tab monitoring stopped successfully"}
    else:
        # Use imported instance
        status = tab_monitor.get_status()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to stop tab monitoring: {status.status} - {status.details or 'unknown error'}",
        )


@router.get("/tabs", response_model=List[Dict])
async def get_current_chrome_tabs():
    """
    Get a list of currently open Chrome tabs via CDP.
    """
    try:
        # Use imported instance
        is_connected = await chrome_manager.ensure_connection()
        if not is_connected:
            raise HTTPException(status_code=503, detail="Chrome is not connected or available.")

        # Use imported instance
        tabs = await chrome_manager.get_all_tabs()
        return tabs
    except HTTPException as http_exc:
        raise http_exc from http_exc
    except Exception as e:
        logger.error(f"Error getting Chrome tabs: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Internal server error getting tabs: {str(e)}"
        ) from e
