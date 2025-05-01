import asyncio
import time
from typing import (
    Awaitable,
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Set,
    Union,
)

from starfruit.browser.chrome_cdp import ChromeTab, get_tabs
from starfruit.browser.chrome_manager import ChromeManager
from starfruit.browser.diff_tab_state import diff_tab_state
from starfruit.browser.tab_interaction_handler import (
    ContentFetchedCallback,
    InteractionTabUpdateCallback,
    TabInteractionHandler,
)
from starfruit.browser.types import TabReference
from starfruit.internal.logger import get_logger

logger = get_logger(__name__)

INITIAL_FETCH_DELAY_SECONDS = 3.0  # Configurable delay before initial fetch
# DEBOUNCE_DELAY_SECONDS = 0.75  # Time to wait after last interaction before fetching - moved to handler


class TabChangeEvent(NamedTuple):
    new_tabs: List[dict]
    closed_tabs: List[dict]
    navigated_tabs: List[dict]
    current_tabs: List[dict]


TabChangeCallback = Union[
    Callable[[TabChangeEvent], None],  # Sync callback
    Callable[[TabChangeEvent], Awaitable[None]],  # Async callback
]

PollingTabChangeCallback = Union[
    Callable[[TabChangeEvent], None],
    Callable[[TabChangeEvent], Awaitable[None]],
]


class ChromeWatcher:
    """watches Chrome for changes."""

    def __init__(self, chrome_manager: ChromeManager, check_interval: float = 2.0):
        """
        Args:
            chrome_manager: ChromeManager instance to use for Chrome interactions
            check_interval: How often to check for tab changes, in seconds
        """
        self.chrome_manager = chrome_manager
        self.check_interval = check_interval
        self.previous_tab_refs: Set[TabReference] = set()
        self.last_tabs_check = 0
        self._monitoring = False
        self._was_disconnected = False  # Flag to track connection state
        self._on_polling_change_callback: Optional[PollingTabChangeCallback] = None
        self._on_interaction_update_callback: Optional[InteractionTabUpdateCallback] = None
        self._on_content_fetched_callback: Optional[ContentFetchedCallback] = None
        self._monitor_task = None  # Task for the main polling loop

        # State for interaction monitoring and debouncing
        self._interaction_handlers: Dict[str, TabInteractionHandler] = {}

    async def start_monitoring(
        self,
        on_polling_change_callback: PollingTabChangeCallback,
        on_interaction_update_callback: InteractionTabUpdateCallback,
        on_content_fetched_callback: ContentFetchedCallback,
    ) -> bool:
        """
        Start monitoring tabs for changes asynchronously, including interaction events.
        This method initializes the monitoring process and should only be called once.
        To resume after a disconnection, the internal _monitor_loop handles it.

        Args:
            on_polling_change_callback: Callback for new/closed/navigated tabs detected by polling.
            on_interaction_update_callback: Callback for single tab content updates triggered by interaction.
            on_content_fetched_callback: Callback for content fetched for a tab

        Returns:
            bool: True if monitoring started successfully
        """
        if self._monitoring:
            logger.warning("Tab monitoring start requested, but already running.")
            return False

        # Store the callbacks
        self._on_polling_change_callback = on_polling_change_callback
        self._on_interaction_update_callback = on_interaction_update_callback
        self._on_content_fetched_callback = on_content_fetched_callback

        # Ensure connection (this might attempt connection but not launch based on recent changes)
        if not self.chrome_manager.connected:
            logger.info("Ensuring Chrome connection before starting tab monitoring...")
            connected = await self.chrome_manager.ensure_connection()
            if not connected:
                logger.error("Failed to ensure Chrome connection. Cannot start tab monitoring.")
                self._was_disconnected = True  # Mark as disconnected initially
                return False  # Cannot start if not connected

        # Perform initial setup (get tabs, start interaction monitors)
        await self._initialize_tabs_and_monitors()

        # Start the main polling monitoring task
        self._monitoring = True
        self._was_disconnected = False  # Mark as connected now
        self._monitor_task = asyncio.create_task(self._monitor_loop())
        return True

    async def _initialize_tabs_and_monitors(self):
        """Gets current tabs, fetches HTML, updates state, and starts interaction monitors."""
        try:
            # Stop any potentially lingering interaction handlers first
            await self._stop_all_interaction_monitors()

            # Get current tabs
            current_cdp_tabs: List[ChromeTab] = await get_tabs()
            filtered_tabs_with_ws = [tab for tab in current_cdp_tabs if tab.webSocketDebuggerUrl]

            # --- Lazy Initial Fetch: Create refs without fetching HTML --- #
            new_tab_refs = set()
            for tab in filtered_tabs_with_ws:
                if tab.id and tab.url:
                    tab_ref = TabReference(
                        id=tab.id,
                        url=tab.url,
                        title=tab.title,
                        html=None,  # Explicitly set HTML to None initially
                        ws_url=tab.webSocketDebuggerUrl,
                    )
                    new_tab_refs.add(tab_ref)
                else:
                    logger.warning(
                        f"Skipping initial ref for tab due to missing ID ({tab.id}) or URL ({tab.url})"
                    )

            # Update the main reference set
            self.previous_tab_refs = new_tab_refs

            # Start interaction monitors for the new set of tabs
            # Use the original filtered_tabs_with_ws list which contains ChromeTab objects
            tabs_map = {tab.id: tab for tab in filtered_tabs_with_ws}
            monitors_started_count = 0
            for tab_ref in self.previous_tab_refs:  # Iterate over the refs we just created
                tab_obj = tabs_map.get(tab_ref.id)
                if tab_obj:
                    # Ensure the tab object passed to the handler has the ws_url
                    if tab_obj.webSocketDebuggerUrl:
                        await self._start_interaction_monitor(tab_obj)
                        monitors_started_count += 1
                    else:
                        logger.warning(
                            f"Ref {tab_ref.id} exists but corresponding ChromeTab obj is missing WebSocket URL, cannot monitor interactions."
                        )

                else:
                    # This case should be less likely now, but handle defensively
                    logger.warning(
                        f"Could not find ChromeTab obj for ref {tab_ref.id} ({tab_ref.url}) during init, cannot monitor interactions."
                    )

        except Exception as e:
            logger.error(f"Error during tab/monitor initialization: {e}", exc_info=True)
            self.previous_tab_refs = set()
            await self._stop_all_interaction_monitors()

    async def stop_monitoring(self) -> None:
        """Stop monitoring tabs for changes (async version), including interaction monitors."""
        if not self._monitoring:
            logger.debug("Monitoring already stopped.")
            return

        self._monitoring = False  # Signal loops to stop

        # Stop interaction monitors first
        logger.debug(f"Stopping {len(self._interaction_handlers)} interaction handlers...")
        await self._stop_all_interaction_monitors()

        # Stop the main polling loop task
        if self._monitor_task and not self._monitor_task.done():
            logger.debug("Stopping main polling task...")
            self._monitor_task.cancel()
            try:
                await asyncio.wait_for(self._monitor_task, timeout=2.0)
                logger.debug("Main polling task cancelled successfully.")
            except asyncio.TimeoutError:
                logger.warning("Main polling task did not stop within timeout.")
            except asyncio.CancelledError:
                logger.debug("Main polling task cancelled as expected.")
            except Exception as e:
                logger.error(f"Error stopping main polling task: {e}")

        # Clear state
        self.previous_tab_refs = set()
        self._on_polling_change_callback = None
        self._on_interaction_update_callback = None
        self._on_content_fetched_callback = None
        self._monitor_task = None
        self._was_disconnected = False  # Reset disconnect flag

        logger.debug("Async tab monitoring stopped completely.")

    # --- Interaction Monitoring Logic (Delegated to Handler) ---

    async def _start_interaction_monitor(self, tab: ChromeTab):
        """Creates and starts a TabInteractionHandler for a single tab."""
        tab_id = tab.id
        ws_url = tab.webSocketDebuggerUrl
        if not ws_url:
            logger.warning(
                f"Cannot start interaction monitor for tab {tab_id}: missing WebSocket URL."
            )
            return

        if tab_id in self._interaction_handlers:
            # logger.debug(f"Interaction handler already running for tab {tab_id}, skipping start.")
            return

        if not self._on_interaction_update_callback:
            logger.error(
                f"Cannot start interaction handler for tab {tab_id}: interaction callback not set."
            )
            return

        if not self._on_content_fetched_callback:
            logger.error(
                f"Cannot start interaction handler for tab {tab_id}: content fetched callback not set."
            )
            return

        handler = TabInteractionHandler(
            tab=tab,
            chrome_manager=self.chrome_manager,
            interaction_callback=self._on_interaction_update_callback,
            content_fetched_callback=self._on_content_fetched_callback,
        )
        self._interaction_handlers[tab_id] = handler
        await handler.start()

    async def _stop_interaction_monitor(self, tab_id: str):
        """Stops the interaction handler and cleans up resources for a single tab."""
        handler = self._interaction_handlers.pop(tab_id, None)
        if handler:
            await handler.stop()

    async def _stop_all_interaction_monitors(self):
        """Stops all active TabInteractionHandler instances."""
        if not self._interaction_handlers:
            return

        logger.info(f"Stopping all {len(self._interaction_handlers)} interaction handlers...")

        # Create stop tasks for all handlers
        stop_tasks = [
            asyncio.create_task(handler.stop()) for handler in self._interaction_handlers.values()
        ]

        # Wait for all stop tasks to complete (with a timeout)
        if stop_tasks:
            logger.debug(f"Waiting for {len(stop_tasks)} interaction handlers to stop...")
            _, pending = await asyncio.wait(
                stop_tasks, timeout=2.0, return_when=asyncio.ALL_COMPLETED
            )
            if pending:
                logger.warning(f"{len(pending)} interaction handlers did not stop within timeout.")

        # Clear the dictionary
        self._interaction_handlers.clear()
        logger.debug("All interaction handlers stopped and cleared.")

    async def _monitor_loop(self) -> None:
        """(handles polling and connection state)."""
        while self._monitoring:
            current_time = time.time()
            try:
                is_connected = self.chrome_manager.connected
            except Exception as conn_e:
                logger.error(f"Error checking chrome_manager.connected: {conn_e}", exc_info=True)
                is_connected = False

            # --- Handle Connection State Change ---
            if not is_connected:
                if not self._was_disconnected:
                    logger.warning("Chrome connection lost detected in _monitor_loop. Pausing.")
                    self._was_disconnected = True
                    await self._stop_all_interaction_monitors()
                await asyncio.sleep(self.check_interval)
                continue
            elif self._was_disconnected:
                logger.info(
                    "Chrome connection re-established detected in _monitor_loop. Resuming..."
                )
                self._was_disconnected = False
                await self._initialize_tabs_and_monitors()
                self.last_tabs_check = 0

            # --- Perform Polling Check (Only if connected) ---
            if current_time - self.last_tabs_check >= self.check_interval:
                try:
                    current_cdp_tabs: List[ChromeTab] = await get_tabs()
                    changed_tabs_event = await self.process_tab_changes(current_cdp_tabs)

                    if self._on_polling_change_callback and changed_tabs_event:
                        # logger.info("Polling detected tab changes. Notifying callback.")
                        if asyncio.iscoroutinefunction(self._on_polling_change_callback):
                            await self._on_polling_change_callback(changed_tabs_event)
                        else:
                            self._on_polling_change_callback(changed_tabs_event)

                    self.last_tabs_check = current_time
                except Exception as e:
                    logger.error(f"Error during polling check in _monitor_loop: {e}", exc_info=True)
                    await asyncio.sleep(self.check_interval)

            await asyncio.sleep(0.5)
        logger.info("Exiting ChromeTabs _monitor_loop.")

    async def process_tab_changes(
        self, current_cdp_tabs: List[ChromeTab]
    ) -> Optional[TabChangeEvent]:
        """
        Process changes based on polled tabs, manage interaction monitors, and fetch HTML for polling-detected changes.
        NOTE: This method now primarily focuses on comparing tab lists and URLs from polling.
              Interaction monitor start/stop is handled by the main loop and initialization logic.
              Ignores tabs with 'chrome://' scheme URLs.

        Args:
            current_cdp_tabs: List of current ChromeTab objects from get_tabs()

        Returns:
            TabChangeEvent if polling detected new/closed/navigated tabs, None otherwise.
        """
        # Filter tabs based only on WebSocket URL existence AND http/https scheme
        filtered_tabs = [
            tab
            for tab in current_cdp_tabs
            if tab.webSocketDebuggerUrl
            and (tab.url.startswith("http://") or tab.url.startswith("https://"))
        ]

        # --- Identify Changes & Manage Interaction Monitors ---

        current_tab_refs_map: Dict[str, TabReference] = {
            ref.id: ref for ref in self.previous_tab_refs
        }
        current_polled_tabs_map: Dict[str, ChromeTab] = {tab.id: tab for tab in filtered_tabs}

        added_tabs, removed_refs, navigated_pairs = diff_tab_state(
            current_polled_tabs_map, current_tab_refs_map
        )

        newly_added_tab_dicts_for_fetch = []
        navigated_tab_dicts_for_fetch = []  # For the new URL if parsable
        navigated_tab_info_for_event = []  # Includes old_url
        closed_tab_dicts_for_event = []

        # --- Determine which refs to keep initially (start with all previous) ---
        tabs_to_keep_refs = set(self.previous_tab_refs)

        # Process Added Tabs
        for tab in added_tabs:
            newly_added_tab_dicts_for_fetch.append(tab.model_dump())  # Fetch all new tabs
            # Add ref with None HTML
            tabs_to_keep_refs.add(TabReference(id=tab.id, url=tab.url, html=None, title=tab.title))
            await self._start_interaction_monitor(tab)

        # Process Removed Tabs
        for ref in removed_refs:
            closed_tab_dicts_for_event.append({"id": ref.id, "url": ref.url})
            await self._stop_interaction_monitor(ref.id)
            # Remove from keep set
            tabs_to_keep_refs = {r for r in tabs_to_keep_refs if r.id != ref.id}

        # Process Existing Tabs (Check for Navigation or becoming parsable)
        for current_tab, previous_ref in navigated_pairs:
            tab_id = current_tab.id

            if current_tab.url != previous_ref.url:
                # Prepare info for the event callback (with old_url)
                nav_event_info = current_tab.model_dump()
                nav_event_info["old_url"] = previous_ref.url
                navigated_tab_info_for_event.append(nav_event_info)

                navigated_tab_dicts_for_fetch.append(
                    current_tab.model_dump()
                )  # Fetch all navigated tabs

                # 1. Stop interaction monitor for old context
                await self._stop_interaction_monitor(tab_id)

                # 2. Update internal state immediately (placeholder HTML)
                # logger.debug(f"Navigation detected for {tab_id}: updating internal ref URL immediately to {current_tab.url}") # Reduced noise
                # Remove old ref from keep set, add new placeholder (will be updated if fetched)
                tabs_to_keep_refs = {r for r in tabs_to_keep_refs if r.id != tab_id}
                tabs_to_keep_refs.add(
                    TabReference(
                        id=tab_id,
                        url=current_tab.url,
                        html=None,  # Mark HTML as stale / set to None
                        title=current_tab.title,
                    )
                )

                # 3. Start interaction monitor for new context (after delay)
                await asyncio.sleep(0.2)
                await self._start_interaction_monitor(current_tab)

            else:
                # URL didn't change. Check if it became parsable. - Removed check
                pass  # No longer need to check for becoming parsable

        # --- Fetch HTML for Polling-Detected Changes ---
        # Consolidate all lists of tab dicts that need fetching
        final_tabs_to_fetch = []
        final_tabs_to_fetch.extend(newly_added_tab_dicts_for_fetch)
        final_tabs_to_fetch.extend(navigated_tab_dicts_for_fetch)

        newly_fetched_tabs_with_html = []
        # Use the consolidated list for fetching
        if final_tabs_to_fetch:
            unique_tabs_to_fetch = {tuple(sorted(d.items())) for d in final_tabs_to_fetch}
            list_of_dicts_to_fetch = [dict(t) for t in unique_tabs_to_fetch]
            # Fetch HTML in parallel ONLY for tabs identified by the polling logic
            newly_fetched_tabs_with_html = await self.chrome_manager.get_html_for_tabs(
                list_of_dicts_to_fetch  # Pass the final list of dicts
            )

        # --- Update Internal State (previous_tab_refs) ---
        # Start with the refs we decided to keep (updated for navigation)
        updated_tab_refs = set(tabs_to_keep_refs)

        # Add/update refs for tabs where polling fetched new HTML
        for tab_dict, _html, fetched_url, fetched_title in newly_fetched_tabs_with_html:
            tab_id = tab_dict.get("id")
            tab_url = fetched_url or tab_dict.get("url")
            final_title = fetched_title or tab_dict.get("title")
            if tab_id and tab_url:
                # Remove any existing ref for this tab_id before adding the new one
                updated_tab_refs = {ref for ref in updated_tab_refs if ref.id != tab_id}
                updated_tab_refs.add(
                    TabReference(
                        id=tab_id,
                        url=tab_url,
                        html=None,  # Store None for HTML in the main set
                        title=final_title,
                    )
                )
            else:
                logger.warning(
                    f"Polling: Skipping tab update due to missing ID ({tab_id}) or URL ({tab_url}) in fetched data: {tab_dict}"
                )

        # Atomically update the main set of references
        self.previous_tab_refs = updated_tab_refs

        # --- Return Event for Polling Callback ---
        polling_detected_changes = bool(
            newly_added_tab_dicts_for_fetch
            or closed_tab_dicts_for_event
            or navigated_tab_info_for_event
        )

        if polling_detected_changes:
            current_tabs_for_event = [tab.model_dump() for tab in filtered_tabs]
            return TabChangeEvent(
                new_tabs=newly_added_tab_dicts_for_fetch,  # Report only newly added that need fetch
                closed_tabs=closed_tab_dicts_for_event,
                navigated_tabs=navigated_tab_info_for_event,  # Report all navigations
                current_tabs=current_tabs_for_event,
            )
        else:
            return None
