import asyncio
import json
import re
from typing import Any, AsyncGenerator, Dict, List, Optional, Tuple

import httpx
import websockets
import websockets.protocol
from pydantic import BaseModel, Field

from starfruit.browser.chrome_process import REMOTE_DEBUG_PORT
from starfruit.internal.logger import get_logger

logger = get_logger(__name__)

# Default timeout for Chrome info retrieval via CDP (seconds)
CHROME_INFO_TIMEOUT = 2

# Default timeout for HTML content retrieval via CDP (seconds)
GET_HTML_TIMEOUT = 2


class ChromeTab(BaseModel):
    id: str
    title: str = Field(default="Untitled")
    url: str = Field(default="about:blank")
    window_id: Optional[int] = None
    webSocketDebuggerUrl: Optional[str] = None
    devtoolsFrontendUrl: Optional[str] = None


async def get_tabs() -> List[ChromeTab]:
    """
    Get all Chrome browser tabs via CDP HTTP API.

    Connects to Chrome DevTools Protocol to retrieve tab information.
    Only returns actual page tabs (not DevTools, extensions, etc).

    Returns:
        List of ChromeTab objects representing open browser tabs
    """
    tabs = []

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://localhost:{REMOTE_DEBUG_PORT}/json/list",
                timeout=2.0,  # Use float timeout for httpx
            )
            response.raise_for_status()  # Check for non-2xx status codes
            cdp_tabs_json = response.json()

        # Process each tab
        for tab_info in cdp_tabs_json:
            # Only include actual tabs (type: page), not devtools, etc.
            if tab_info.get("type") == "page":
                # Create a dict with all fields we want to extract
                tab_data = {
                    "id": tab_info.get("id"),
                    "title": tab_info.get("title", "Untitled"),
                    "url": tab_info.get("url", "about:blank"),
                    "webSocketDebuggerUrl": tab_info.get("webSocketDebuggerUrl"),
                    "devtoolsFrontendUrl": tab_info.get("devtoolsFrontendUrl"),
                }

                # Get window ID from debug URL if available
                devtools_url = tab_info.get("devtoolsFrontendUrl", "")
                if "windowId" in devtools_url:
                    try:
                        window_id_match = re.search(r"windowId=(\d+)", devtools_url)
                        if window_id_match:
                            tab_data["window_id"] = int(window_id_match.group(1))
                    except Exception as e:
                        logger.debug(f"Could not extract window ID: {e}")

                # Create Pydantic model instance
                try:
                    tabs.append(ChromeTab(**tab_data))
                except Exception as e:
                    logger.error(f"Failed to parse tab data: {e}")

        return tabs

    # Update exception handling for httpx
    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to get tabs: HTTP {e.response.status_code}")
    except httpx.RequestError as e:
        logger.error(f"Failed to connect to Chrome DevTools API: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Chrome DevTools API response: {e}")
    except Exception as e:
        logger.error(f"Error getting tabs via Chrome DevTools API: {e}")

    # Return empty list if we couldn't get tabs
    return []


# --- New function to get raw CDP targets ---
async def get_cdp_targets() -> List[Dict[str, Any]]:
    """
    Get the raw list of all targets from Chrome via CDP HTTP API.

    Returns:
        List of target dictionaries as returned by CDP, or empty list on error.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://localhost:{REMOTE_DEBUG_PORT}/json/list",
                timeout=2.0,  # Keep a reasonable timeout
            )
            response.raise_for_status()  # Check for non-2xx status codes
            targets_json = response.json()
            # Return the raw list of dictionaries
            return targets_json if isinstance(targets_json, list) else []

    # Reuse similar error handling as get_tabs
    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to get targets: HTTP {e.response.status_code}")
    except httpx.RequestError as e:
        logger.error(f"Failed to connect to Chrome DevTools API for targets: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Chrome DevTools API target response: {e}")
    except Exception as e:
        logger.error(f"Error getting targets via Chrome DevTools API: {e}")

    return []  # Return empty list on any error


async def get_chrome_info():
    """
    Get Chrome version info and check connection via CDP HTTP API.

    Makes a single request to get both connection status and Chrome version.

    Returns:
        dict: {
            "connected": bool indicating if connection succeeded,
            "version": Chrome version string (or "Unknown" if not connected),
            "data": Full response data if connected (or None if not connected)
        }
    """
    result = {"connected": False, "version": "Unknown", "data": None}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://localhost:{REMOTE_DEBUG_PORT}/json/version",
                timeout=float(CHROME_INFO_TIMEOUT),  # Ensure timeout is float
            )
            result["connected"] = response.status_code == 200

            if result["connected"]:
                data = response.json()
                result["data"] = data
                result["version"] = data.get("Browser", "Unknown")

    # Catch specific httpx errors and general exceptions
    except httpx.RequestError as e:
        logger.debug(f"Error getting Chrome info (httpx RequestError): {e}")
    except json.JSONDecodeError as e:
        logger.debug(f"Error parsing Chrome info JSON: {e}")
    except Exception as e:
        logger.debug(f"Unexpected error getting Chrome info: {e}")
        # Keep defaults (not connected, Unknown version)

    return result


async def get_tab_html_content(ws_url: str) -> Tuple[Optional[str], Optional[str]]:
    """Get HTML and URL with hard timeout using asyncio.wait_for"""
    try:
        # Give up after 10 seconds total for entire CDP operation
        return await asyncio.wait_for(_get_html_using_dom(ws_url), timeout=10.0)
    except asyncio.TimeoutError:
        logger.error("CDP HTML retrieval timed out after 10 seconds")
        return None, None
    except Exception as e:
        logger.error(f"CDP failed: {e}")
        return None, None


async def _send_cdp_command(ws, msg_id: int, method: str, params: Optional[dict] = None) -> dict:
    """Send a CDP command and wait for the specific response matching the ID."""
    command = {"id": msg_id, "method": method}
    if params:
        command["params"] = params

    # logger.debug(f"Sending CDP command (id={msg_id}): {method}")
    await ws.send(json.dumps(command))

    # Loop until we get the response matching our msg_id
    while True:
        response_raw = await ws.recv()
        response = json.loads(response_raw)

        # Check if it's the response we are waiting for
        if response.get("id") == msg_id:
            # logger.debug(f"Received response for id={msg_id}")
            return response
        elif "method" in response:  # It's an event, ignore
            pass
        else:  # Unexpected message format
            pass


async def _get_html_using_dom(ws_url: str) -> Tuple[Optional[str], Optional[str]]:
    """Get HTML content and final URL using DOM.getOuterHTML CDP method"""
    msg_counter = 1  # Use a counter for unique message IDs
    current_url: Optional[str] = None  # Store the URL found
    try:
        async with websockets.connect(
            ws_url,
            open_timeout=GET_HTML_TIMEOUT,
            close_timeout=GET_HTML_TIMEOUT,
            max_size=20 * 1024 * 1024,  # default is 1mb, we use 20mb
        ) as ws:
            # First check if page is ready using Page.getResourceTree
            # This will tell us quickly if it's a blank/loading page
            try:
                # Enable Page domain (required for getResourceTree)
                await _send_cdp_command(ws, msg_counter, "Page.enable")
                msg_counter += 1

                # Get Resource Tree
                resource_result = await _send_cdp_command(ws, msg_counter, "Page.getResourceTree")
                msg_counter += 1

                # Check if this is an about:blank or empty page
                frame = resource_result.get("result", {}).get("frameTree", {}).get("frame", {})
                current_url = frame.get("url", None)  # Store the URL from frame
                if current_url in ["about:blank", ""]:
                    logger.debug("Detected blank/empty page - returning empty HTML")
                    return None, current_url  # Return None HTML, but the URL
            except Exception as e:
                # If this fails, just continue with normal DOM method
                logger.debug(f"Resource check failed: {e}, continuing with DOM method")

            # Enable DOM domain
            await _send_cdp_command(ws, msg_counter, "DOM.enable")
            msg_counter += 1

            # Get document root node
            doc_result = await _send_cdp_command(ws, msg_counter, "DOM.getDocument")
            msg_counter += 1
            # logger.debug(f"DOM.getDocument result: {doc_result}")

            # Extract document URL if available (more reliable than frame URL sometimes)
            root_data = doc_result.get("result", {}).get("root", {})
            doc_url = root_data.get("documentURL")
            if doc_url:
                current_url = doc_url  # Prefer documentURL if found

            # Extract root node ID from response
            root_node_id = root_data.get("nodeId")
            if not root_node_id:
                logger.error("Failed to get root node ID")
                return None, current_url  # Return None HTML, but potentially URL

            # Get outer HTML using the root node ID
            html_result = await _send_cdp_command(
                ws, msg_counter, "DOM.getOuterHTML", {"nodeId": root_node_id}
            )
            msg_counter += 1

            # Extract HTML content and log summary
            html_content = html_result.get("result", {}).get("outerHTML", "")
            if "error" in html_result:
                error_message = html_result["error"].get("message", "Unknown error")
                logger.warning(f"DOM.getOuterHTML failed: {error_message}")
            elif html_content:
                # logger.debug(f"DOM.getOuterHTML success: HTML length = {len(html_content)}")
                pass
            else:
                logger.warning("DOM.getOuterHTML succeeded but returned empty HTML")

            if html_content:
                return html_content, current_url
            else:
                return None, current_url  # Return None HTML, but the URL we found

    except asyncio.TimeoutError:
        # websockets uses asyncio.TimeoutError for connection timeouts?
        logger.warning("ws connection timed out")
        return None, None
    except websockets.ConnectionClosedError as e:
        if "403 Forbidden" in str(e):
            logger.error("chrome rejected ws connection.")
        else:
            logger.error(f"ws connection error: {e}")
        return None, None
    except Exception as e:
        logger.error(f"failed to connect to tab via ws: {e}")
        return None, None


async def monitor_user_interactions(ws_url: str) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Monitor clicks and scrolls in a tab using CDP and yield events.

    Connects to the tab's WebSocket, injects JS listeners, and listens
    for console messages indicating user interaction.

    Yields:
        dict: Structured event data like {"type": "click", "data": {...}} or {"type": "scroll", "data": {...}}
    """
    msg_counter = 1
    connection = None  # Keep track of the connection to close it reliably
    ws = None  # Initialize ws outside the try block
    try:
        # --- Connection Attempt w/ Retry ---
        max_retries = 3
        retry_delay = 0.5  # Initial delay in seconds
        for attempt in range(max_retries):
            try:
                connection = await websockets.connect(
                    ws_url,
                    open_timeout=5.0,  # Timeout for each attempt
                    close_timeout=5.0,
                    max_size=20 * 1024 * 1024,
                )
                ws = connection  # Assign to ws if connection is successful
                break  # Exit retry loop on success
            except (
                OSError,
                websockets.exceptions.InvalidMessage,
                asyncio.TimeoutError,
            ) as conn_err:
                logger.warning(
                    f"ws connection attempt {attempt + 1}/{max_retries} failed for {ws_url}: {type(conn_err).__name__}",
                    exc_info=False,
                )
                if attempt + 1 == max_retries:
                    logger.error(
                        f"Max retries reached for WebSocket connection to {ws_url}. Giving up."
                    )
                    return  # Exit generator if all retries fail
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff

        # If loop finishes without connecting (shouldn't happen due to return above, but safety check)
        if not ws:
            logger.error(f"Failed to establish WebSocket connection after retries for {ws_url}.")
            return

        # === Step 1: Enable Runtime domain FIRST ===
        await _send_cdp_command(ws, msg_counter, "Runtime.enable")
        msg_counter += 1
        # === Step 2: Enable dependent domains (Page, Log) ===
        await _send_cdp_command(ws, msg_counter, "Page.enable")
        msg_counter += 1
        # === Step 3: Subscribe to consoleAPICalled event ===
        # Inject JS listeners
        js_code = """
        (function() {
            console.log('STARFRUIT_DEBUG: Injecting listeners...'); // Debug log
            // Use a closure to prevent polluting the global scope too much
            let lastScrollTimestamp = 0;
            let lastClickTimestamp = 0;
            const DEBOUNCE_MS = 250; // Only log if events are spaced out

            document.addEventListener('click', e => {
                const now = Date.now();
                if (now - lastClickTimestamp > DEBOUNCE_MS) {
                    const clickData = {
                        x: e.clientX,
                        y: e.clientY,
                        target: e.target ? e.target.tagName : 'unknown',
                        timestamp: now
                    };
                    console.log('STARFRUIT_CLICK_EVENT', JSON.stringify(clickData));
                    lastClickTimestamp = now;
                }
            }, { capture: true, passive: true }); // Use capture phase, non-blocking

            document.addEventListener('scroll', e => {
                 const now = Date.now();
                 if (now - lastScrollTimestamp > DEBOUNCE_MS) {
                    const scrollData = {
                        scrollX: window.scrollX,
                        scrollY: window.scrollY,
                        timestamp: now
                    };
                    console.log('STARFRUIT_SCROLL_EVENT', JSON.stringify(scrollData));
                    lastScrollTimestamp = now;
                 }
            }, { capture: true, passive: true }); // Use capture phase, non-blocking

            console.log('STARFRUIT_DEBUG: Listeners successfully installed.'); // Debug log
            return "Interaction listeners installed.";
        })();
        """
        _eval_result = await _send_cdp_command(
            ws,
            msg_counter,
            "Runtime.evaluate",
            {"expression": js_code, "awaitPromise": False, "returnByValue": True},
        )
        msg_counter += 1
        # Listen for console entries
        while True:
            response_raw = await ws.recv()
            response = json.loads(response_raw)

            if response.get("method") == "Runtime.consoleAPICalled":
                call_type = response.get("params", {}).get("type")
                args = response.get("params", {}).get("args", [])

                # Check if it's a log message with our specific prefix
                if call_type == "log" and len(args) >= 1:
                    first_arg_value = args[0].get("value")

                    # --- Handle STARFRUIT_DEBUG messages ---
                    if first_arg_value == "STARFRUIT_DEBUG: Injecting listeners...":
                        pass
                        # logger.info(f"[{ws_url[-10:]}] JS Injection: Starting setup.")
                    elif first_arg_value == "STARFRUIT_DEBUG: Listeners successfully installed.":
                        pass
                        # logger.info(
                        #     f"[{ws_url[-10:]}] JS Injection: Listeners confirmed installed."
                        # )
                    # --- Handle STARFRUIT_CLICK_EVENT ---
                    elif first_arg_value == "STARFRUIT_CLICK_EVENT" and len(args) >= 2:
                        try:
                            click_data = json.loads(args[1].get("value", "{}"))
                            yield {"type": "click", "data": click_data}
                        except json.JSONDecodeError:
                            logger.warning("Failed to parse click event data from CDP console")
                    elif first_arg_value == "STARFRUIT_SCROLL_EVENT" and len(args) >= 2:
                        try:
                            scroll_data = json.loads(args[1].get("value", "{}"))
                            yield {"type": "scroll", "data": scroll_data}
                        except json.JSONDecodeError:
                            logger.warning("Failed to parse scroll event data from CDP console")

    except (
        websockets.ConnectionClosedOK,
        websockets.ConnectionClosedError,
        websockets.ConnectionClosed,
    ) as e:
        # These are expected closures, log as info or debug
        logger.info(f"ws connection closed for {ws_url}: {e}")
    # Keep generic exception for unexpected errors during the loop
    except Exception as e:
        # Log errors happening *after* successful connection as ERROR
        logger.error(
            f"Error during interaction monitoring for {ws_url}: {type(e).__name__} - {e}",
            exc_info=True,
        )
    finally:
        # Check state before attempting to close
        if connection and connection.state != websockets.protocol.State.CLOSED:
            await connection.close()
        # This generator stops yielding when an error occurs or connection closes.
