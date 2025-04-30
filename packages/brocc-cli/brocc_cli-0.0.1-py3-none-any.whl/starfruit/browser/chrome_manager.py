import asyncio
from enum import Enum
from typing import List, NamedTuple, Optional, Tuple

from starfruit.browser.chrome_cdp import (
    get_chrome_info,
    get_tab_html_content,
    get_tabs,
)
from starfruit.browser.chrome_process import (
    is_chrome_debug_port_active,
    is_chrome_process_running,
)
from starfruit.internal.logger import get_logger

logger = get_logger(__name__)


class ChromeState(NamedTuple):
    is_running: bool
    has_debug_port: bool


class ChromeStatus(Enum):
    CONNECTED = "connected"
    NOT_RUNNING = "not_running"
    RUNNING_WITHOUT_DEBUG_PORT = "running_without_debug_port"
    CONNECTING = "connecting"


class ChromeManager:
    """Manages the connection to a Chrome instance with remote debugging."""

    def __init__(self):
        self._state: ChromeState = ChromeState(False, False)  # Initial state
        self._connected: bool = False
        self._initialized = False

    async def _ensure_initialized(self):
        """Ensure async initialization has been performed"""
        if not self._initialized:
            await self._init_async()
            self._initialized = True

    async def _init_async(self):
        """Initialize the state asynchronously"""
        self._state = await self._get_chrome_state()
        if self._state.has_debug_port:
            await self._test_connection(quiet=True)

    async def _test_connection(self, quiet: bool = False) -> bool:
        """Tests connection to Chrome debug port, updates status"""
        try:
            # Try to connect - directly use async function
            chrome_info = await get_chrome_info()
            if chrome_info["connected"]:
                self._connected = True
                if not quiet:
                    logger.debug(f"Auto-connected to Chrome {chrome_info['version']}")
                return True
            else:
                if not quiet:
                    logger.warning("Auto-connect: Failed to connect despite active debug port")
        except Exception as e:
            if not quiet:
                logger.error(f"Auto-connect error: {e}")

        return False

    async def _get_chrome_state(self) -> ChromeState:
        """Get the current state of Chrome (running and debug port status)."""
        has_debug_port = await is_chrome_debug_port_active()
        is_running = has_debug_port or await is_chrome_process_running()
        return ChromeState(
            is_running=is_running,
            has_debug_port=has_debug_port,
        )

    @property
    def connected(self) -> bool:
        return self._connected and self._state.has_debug_port

    async def status_code(self) -> ChromeStatus:
        """Returns the machine-readable enum status of Chrome."""
        await self._ensure_initialized()
        self._state = await self._get_chrome_state()
        if self._connected and self._state.has_debug_port:
            return ChromeStatus.CONNECTED
        elif not self._state.is_running:
            return ChromeStatus.NOT_RUNNING
        elif self._state.is_running and not self._state.has_debug_port:
            return ChromeStatus.RUNNING_WITHOUT_DEBUG_PORT
        else:
            return ChromeStatus.CONNECTING

    async def refresh_state(self) -> ChromeState:
        """Refresh and return the current Chrome state."""
        await self._ensure_initialized()
        self._state = await self._get_chrome_state()
        # Try to auto-connect if configured and debug port is active
        if self._state.has_debug_port and not self._connected:
            await self._test_connection()
        return self._state

    async def ensure_connection(self) -> bool:
        """
        Ensures Chrome is running with the debug port and attempts to connect to it.
        NOTE: This method WILL NOT launch or relaunch Chrome. It only checks the
        current state and tries to connect if the debug port is active.
        """
        await self._ensure_initialized()
        # Always refresh state before attempting connection
        self._state = await self._get_chrome_state()

        # Check if we already have a confirmed connection
        if self._connected and self._state.has_debug_port:
            return True

        # If debug port is not active, we cannot connect. Return False.
        if not self._state.has_debug_port:
            if self._state.is_running:
                logger.warning("Chrome is running but debug port is not active. Cannot connect.")
            else:
                logger.warning("Chrome is not running. Cannot connect.")
            self._connected = False  # Ensure disconnected status
            return False

        # If debug port IS active, attempt connection
        logger.debug("Chrome running with debug port. Attempting to connect...")
        try:
            chrome_info = await get_chrome_info()
            if chrome_info["connected"]:
                self._connected = True
                logger.info(
                    f"Successfully connected to Chrome {chrome_info['version']} via debug port"
                )
                return True
            else:
                # Connection failed even though port seemed active
                self._connected = False
                logger.warning("Connection failed despite active debug port detected.")
                return False
        except Exception as e:
            self._connected = False
            logger.error(f"Error during connection attempt: {e}")
            return False

    async def get_all_tabs(self) -> List[dict]:
        """
        Get information about all open tabs in Chrome using CDP HTTP API:
        - Title, URL, ID, window_id, webSocketDebuggerUrl, devtoolsFrontendUrl
        """
        await self._ensure_initialized()
        # Directly use async function
        tabs_data = await get_tabs()

        # Convert the Pydantic models to dictionaries for backward compatibility
        tabs = []
        for tab in tabs_data:
            tab_dict = tab.model_dump()

            # If window_id exists but not part of the dict, add it
            if tab.window_id and "window_id" not in tab_dict:
                tab_dict["window_id"] = tab.window_id

            tabs.append(tab_dict)

        return tabs

    async def get_tab_html(
        self, ws_url: Optional[str], initial_url: Optional[str], title: Optional[str]
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Get the HTML content, final URL, and title from a specific tab using its WebSocket URL.

        Args:
            ws_url: The WebSocket debugger URL for the tab.
            initial_url: The URL known for the tab before attempting fetch.
            title: The title known for the tab before attempting fetch.

        Returns:
            Tuple (html_content | None, final_url | None, final_title | None)
        """
        await self._ensure_initialized()
        if not self._state.has_debug_port:
            logger.error("Chrome debug port is not active. Cannot attempt CDP for tab HTML.")
            return None, initial_url, title  # Return initial values on error

        final_url: Optional[str] = initial_url  # Keep track of the best URL
        final_title: Optional[str] = title  # Keep track of the best title
        html: Optional[str] = None

        # Try CDP only if WebSocket URL is available
        if ws_url:
            html, cdp_url = await get_tab_html_content(ws_url)
            if cdp_url:  # Update URL if CDP returned one
                # logger.debug(f"CDP provided updated URL: {cdp_url}")
                final_url = cdp_url
            # NOTE: get_tab_html_content doesn't return title, so we keep the input title.
            # If title changes significantly *during* interaction/fetch, this might be slightly stale.
            # But it avoids an extra CDP call.
            if html:
                return html, final_url, final_title  # Success with CDP
            else:
                pass
                # logger.warning(f"CDP failed to get HTML content (initial URL: {initial_url}).")
        else:
            logger.warning(
                f"Tab (initial URL: {initial_url}) has no WebSocket URL. Cannot use CDP."
            )

        # If we reach here, CDP failed or wasn't attempted
        # logger.error(f"Failed to get HTML for tab (initial URL: {initial_url}) using CDP.")
        return None, final_url, final_title  # Return None for HTML, but best URL/title we found

    async def get_html_for_tabs(
        self, tabs: List[dict]
    ) -> List[Tuple[dict, Optional[str], Optional[str], Optional[str]]]:  # Added Title
        """
        Get HTML content, final URLs, and titles from multiple tabs via CDP.

        Args:
            tabs: List of tab dictionaries containing id, url, title, webSocketDebuggerUrl

        Returns:
            List of (tab_dict, html | None, final_url | None, final_title | None) tuples
        """
        await self._ensure_initialized()
        results: List[Tuple[dict, Optional[str], Optional[str], Optional[str]]] = []

        if not tabs:
            return []

        semaphore = asyncio.Semaphore(5)

        async def process_tab_with_cdp_async(tab):
            async with semaphore:
                initial_title = tab.get("title", "Untitled")
                initial_url = tab.get("url")
                ws_url = tab.get("webSocketDebuggerUrl")
                short_title = (
                    (initial_title[:30] + "...") if len(initial_title) > 30 else initial_title
                )
                html: Optional[str] = None
                final_url: Optional[str] = initial_url
                final_title: Optional[str] = initial_title
                try:
                    # Call the updated get_tab_html method
                    html, final_url, final_title = await self.get_tab_html(
                        ws_url, initial_url, initial_title
                    )
                except asyncio.TimeoutError:
                    logger.warning(f"get_html_for_tabs: {short_title} timed out")
                except Exception as e:
                    logger.error(f"get_html_for_tabs: {short_title}: {e}")
                if not html:
                    logger.warning(f"get_html_for_tabs: {short_title} failed to get HTML")
                return tab, html, final_url, final_title  # Return all four values

        cdp_results = await asyncio.gather(
            *[process_tab_with_cdp_async(tab) for tab in tabs], return_exceptions=True
        )

        successful_results = []
        exceptions_caught = []
        for result in cdp_results:
            if isinstance(result, Exception):
                exceptions_caught.append(result)
            else:
                # Expecting (tab_dict, html | None, final_url | None, final_title | None)
                successful_results.append(result)

        for tab, html, url, title in successful_results:
            # Update the original tab dict with potentially updated URL/title if needed?
            # For now, just return them alongside. The caller can decide.
            results.append((tab, html, url, title))

        for exc in exceptions_caught:
            logger.error(f"Error during gather for tab processing: {exc}", exc_info=False)
        return results

    async def shutdown(self):
        logger.debug("Shutting down ChromeManager...")
        # Add any other Chrome cleanup if needed here
        self._connected = False
        self._initialized = False
        logger.debug("ChromeManager shutdown complete.")
