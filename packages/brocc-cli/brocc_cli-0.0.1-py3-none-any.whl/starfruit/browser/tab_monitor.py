import asyncio
import json
from typing import List, Optional, cast

import httpx
from pydantic import BaseModel
from sqlalchemy.orm import Session

from starfruit.browser.chrome_cdp import ChromeTab, get_tabs
from starfruit.browser.chrome_manager import ChromeManager
from starfruit.browser.chrome_watcher import (
    ChromeWatcher,
    TabChangeEvent,
    TabReference,
)
from starfruit.browser.next_monitor_status import next_monitor_status
from starfruit.db.sqlite_manager import sqlite_manager
from starfruit.db.sqlite_models import Item
from starfruit.internal.auth_data import is_logged_in, load_auth_data
from starfruit.internal.logger import get_logger
from starfruit.internal.normalize_url import normalize_url
from starfruit.parse.parser_registry import get_parser_for_url
from starfruit.server.debouncer import AsyncDebouncer
from starfruit.server.types import MonitorStatus
from starfruit.tasks.should_save import should_save_content
from starfruit.tasks.task_item import ParseResult, ProcessingItem, SummaryItem

logger = get_logger(__name__)

SAVE_DEBOUNCE_DELAY_SECONDS = 2.0


class TabMonitorStatusRes(BaseModel):
    status: MonitorStatus
    details: Optional[str] = None
    is_chrome_connected: bool = False
    tabs_count: int = 0


class TabMonitor:
    def __init__(self, chrome_manager: ChromeManager):
        self.chrome_manager = chrome_manager
        self.http_client = httpx.AsyncClient()
        self.chrome_watcher: Optional[ChromeWatcher] = None
        self._monitoring_task: Optional[asyncio.Task] = None
        self._status = MonitorStatus.INACTIVE
        self._status_details: Optional[str] = None
        self._last_interacted_tab_id: Optional[str] = None
        self._save_debouncer = AsyncDebouncer(
            delay=SAVE_DEBOUNCE_DELAY_SECONDS, callback=self._actual_save_tab_data
        )

    async def start_monitoring(self) -> bool:
        """Start the tab monitoring service and its background check loop."""
        if self._monitoring_task and not self._monitoring_task.done():
            logger.warning("TabMonitor background task already running.")
            if self.chrome_watcher and not self.chrome_watcher._monitoring:
                logger.info(
                    "Service loop running, but ChromeWatcher monitor stopped. Attempting to restart ChromeWatcher monitor..."
                )
                try:
                    # Re-use the existing start logic, assuming it's correct
                    await self._ensure_tabs_monitor_started()
                except Exception as e:
                    logger.error(f"Error restarting ChromeWatcher monitor: {e}", exc_info=True)
                    self._status = MonitorStatus.ERROR
                    self._status_details = f"Failed to restart ChromeWatcher: {e}"
            return True  # Indicate it's already running or restart attempted

        if self.chrome_watcher is None:
            self.chrome_watcher = ChromeWatcher(self.chrome_manager)

        self._monitoring_task = asyncio.create_task(self._run_monitoring_loop())

        # Initial state check and start
        await self._run_initial_check()

        # Check if the initial check resulted in an error state
        if self._status == MonitorStatus.ERROR:
            logger.error("Tab monitoring failed to start due to errors during initial check.")
            if self._monitoring_task and not self._monitoring_task.done():
                self._monitoring_task.cancel()  # Cancel the loop if init failed
            return False

        return True  # Started successfully or is already running

    async def _run_initial_check(self):
        """Performs the initial check for Chrome connection and starts monitoring if possible."""
        try:
            chrome_connected = await self.chrome_manager.ensure_connection()
            if chrome_connected:
                logger.info("Initial check: Chrome connected. Starting ChromeTabs monitoring...")
                await self._ensure_tabs_monitor_started()
                if self._status == MonitorStatus.ACTIVE:
                    if self.chrome_watcher:
                        initial_refs_to_save = list(self.chrome_watcher.previous_tab_refs)
                        if initial_refs_to_save:
                            logger.info(
                                f"Queueing save for {len(initial_refs_to_save)} initial tabs..."
                            )
                            for initial_ref in initial_refs_to_save:
                                # Trigger debouncer using tab_id
                                await self._save_debouncer.trigger(
                                    key=initial_ref.id, value=initial_ref.id
                                )
                    else:
                        logger.warning(
                            "Cannot save initial refs: tabs_monitor is None after start attempt."
                        )
            else:
                logger.warning(
                    "Initial check: Chrome disconnected. Monitoring loop started, status set to PAUSED."
                )
                self._status = MonitorStatus.PAUSED_CHROME_DISCONNECTED
                self._status_details = "Chrome is disconnected"
        except Exception as e:
            logger.error(f"Error during TabMonitor initial check: {e}", exc_info=True)
            self._status = MonitorStatus.ERROR
            self._status_details = f"Error initializing monitoring: {str(e)}"

    async def stop_monitoring(self) -> bool:
        """Stop the tab monitoring service and its background loop."""
        try:
            # Cancel the monitoring task if it exists
            if self._monitoring_task and not self._monitoring_task.done():
                self._monitoring_task.cancel()
                try:
                    await self._monitoring_task
                except asyncio.CancelledError:
                    pass
                self._monitoring_task = None

            # Shutdown debouncer
            await self._save_debouncer.shutdown()

            # Stop the tabs monitor if it exists
            if self.chrome_watcher:
                await self.chrome_watcher.stop_monitoring()

            self._status = MonitorStatus.INACTIVE
            logger.info("Tab monitoring stopped successfully")
            return True

        except Exception as e:
            self._status = MonitorStatus.ERROR
            self._status_details = f"Error stopping monitoring: {str(e)}"
            logger.error(f"Error stopping tab monitoring: {e}", exc_info=True)
            return False

    def get_status(self) -> TabMonitorStatusRes:
        """Get the current status of the tab monitor"""
        tabs_count = 0
        is_chrome_connected = False
        try:
            is_chrome_connected = self.chrome_manager.connected
            if self.chrome_watcher:
                tabs_count = len(self.chrome_watcher.previous_tab_refs)
        except Exception as e:
            logger.error(f"Error getting monitoring status details: {e}")

        return TabMonitorStatusRes(
            status=self._status,
            details=self._status_details,
            is_chrome_connected=is_chrome_connected,
            tabs_count=tabs_count,
        )

    async def _ensure_tabs_monitor_started(self):
        """Checks and attempts to start the ChromeTabs monitor if not running."""
        if not self.chrome_watcher:
            logger.error("Cannot start ChromeTabs: instance is None!")
            self._status = MonitorStatus.ERROR
            self._status_details = "tabs_monitor instance missing on start attempt"
            return

        if not self.chrome_watcher._monitoring:
            try:
                monitor_started = await self.chrome_watcher.start_monitoring(
                    on_polling_change_callback=self._handle_tab_polling_update,
                    on_interaction_update_callback=self._handle_interaction_update,
                    on_content_fetched_callback=self._handle_content_fetched,
                )
                if not monitor_started:
                    logger.error("Failed to start ChromeTabs monitoring.")
                    self._status = MonitorStatus.ERROR
                    self._status_details = "Failed to start ChromeTabs component"
            except Exception as e:
                logger.error(f"Error starting ChromeTabs monitoring: {e}", exc_info=True)
                self._status = MonitorStatus.ERROR
                self._status_details = f"Error starting ChromeTabs: {e}"
        else:
            logger.debug("ChromeTabs monitor is already running.")

    async def _transition_to_state(self, new_status: MonitorStatus):
        """Handles the side effects of changing the monitoring state."""
        if new_status == self._status:
            return

        old_status = self._status
        self._status = new_status
        if new_status == MonitorStatus.PAUSED_CHROME_DISCONNECTED:
            self._status_details = "Chrome is disconnected"
        elif new_status == MonitorStatus.PAUSED_NEEDS_LOGIN:
            self._status_details = "User needs to log in"
        elif new_status == MonitorStatus.ERROR:
            if not self._status_details:
                self._status_details = "An unexpected error occurred"
        else:
            self._status_details = None

        monitor_should_be_running = new_status == MonitorStatus.ACTIVE
        if monitor_should_be_running and old_status != MonitorStatus.ACTIVE:
            await self._ensure_tabs_monitor_started()
            if self._status != new_status:
                logger.warning(
                    f"Transition to {new_status} failed, current status is now {self._status}"
                )
                return

    async def _run_monitoring_loop(self):
        """Background task to periodically check monitoring conditions and manage state."""
        try:
            while True:
                await self.chrome_manager.refresh_state()
                chrome_connected = self.chrome_manager.connected
                auth_data = load_auth_data()
                user_logged_in = is_logged_in(auth_data)

                next_status = next_monitor_status(
                    current_status=self._status,
                    chrome_connected=chrome_connected,
                    user_logged_in=user_logged_in,
                )

                if next_status != self._status:
                    await self._transition_to_state(next_status)

                await asyncio.sleep(5)
        except asyncio.CancelledError:
            logger.debug("Monitoring loop cancelled")
            raise
        except Exception as e:
            logger.error(f"Error in tab monitoring loop: {e}", exc_info=True)
            self._status = MonitorStatus.ERROR
            self._status_details = f"Error in monitoring loop: {str(e)}"

    async def _handle_tab_polling_update(self, event: TabChangeEvent):
        """Handle polling-based tab changes from ChromeTabs"""
        closed_tab_ids = {tab["id"] for tab in event.closed_tabs}
        if self._last_interacted_tab_id and self._last_interacted_tab_id in closed_tab_ids:
            logger.debug(
                f"Last interacted tab {self._last_interacted_tab_id} was closed. Clearing interaction state."
            )
            self._last_interacted_tab_id = None

        if self._status != MonitorStatus.ACTIVE:
            return

        # --- Process Tabs: Prioritize event data, fallback to watcher state --- #
        tabs_to_trigger_save = set()  # Use a set to avoid duplicate tab IDs
        for tab_info in event.new_tabs + event.navigated_tabs:
            tab_id = tab_info.get("id")
            url = tab_info.get("url")
            # title = tab_info.get("title")
            html_content = tab_info.get("html")  # HTML from event

            if not tab_id or not url:
                logger.warning(
                    f"Polling update: Skipping tab ID {tab_id} (URL: {url}) due to missing id or url in event data."
                )
                continue

            # Attempt 1: Use HTML directly from event if available
            if html_content:
                # If HTML is present, we can trigger save immediately based on this event
                # NOTE: We only need the tab_id to trigger the debouncer
                tabs_to_trigger_save.add(tab_id)
            else:
                # Attempt 2: HTML missing from event. Check if the ref exists in watcher.
                # Need to fetch HTML before triggering save if it was missing.
                if self.chrome_watcher:
                    # Fetch the LATEST tab info, including ws_url, to get HTML
                    try:
                        current_tabs: List[ChromeTab] = await get_tabs()
                        target_tab_obj = next((t for t in current_tabs if t.id == tab_id), None)

                        if target_tab_obj and target_tab_obj.webSocketDebuggerUrl:
                            # Fetch HTML explicitly
                            fetched_html, fetched_url, _ = await self.chrome_manager.get_tab_html(
                                ws_url=target_tab_obj.webSocketDebuggerUrl,
                                initial_url=target_tab_obj.url,
                                title=target_tab_obj.title,
                            )
                            if fetched_html and fetched_url:  # Check if fetch succeeded
                                tabs_to_trigger_save.add(tab_id)
                            else:
                                logger.warning(
                                    f"Polling update: Fetched HTML for tab ID {tab_id} but content or URL was empty. Skipping save trigger."
                                )
                        elif target_tab_obj:
                            logger.warning(
                                f"Polling update: Found tab {tab_id} but it lacks WebSocket URL. Cannot fetch HTML or trigger save."
                            )
                        else:
                            logger.warning(
                                f"Polling update: Could not find current tab info for ID {tab_id}. Cannot fetch HTML or trigger save."
                            )
                    except Exception as fetch_err:
                        logger.error(
                            f"Polling update: Error fetching HTML for tab ID {tab_id}: {fetch_err}",
                            exc_info=True,
                        )
                else:
                    logger.warning("Chrome watcher is None, cannot fetch missing HTML.")

        # Trigger debouncer for unique tab IDs that need saving
        for tid in tabs_to_trigger_save:
            await self._save_debouncer.trigger(key=tid, value=tid)

    async def _handle_interaction_update(self, tab_ref: TabReference):
        """Internal handler for interaction events from ChromeTabs monitor."""
        if not self._status == MonitorStatus.ACTIVE:
            return
        self._last_interacted_tab_id = tab_ref.id

    async def _handle_content_fetched(self, tab_ref: TabReference):
        """Handles the event when fresh content has been fetched after an interaction."""
        if self._status != MonitorStatus.ACTIVE:
            return
        # Trigger debouncer using tab_id
        await self._save_debouncer.trigger(key=tab_ref.id, value=tab_ref.id)

    async def _actual_save_tab_data(self, tab_id: str):
        """Process and save data for a given tab ID after debounce period."""
        if self._status != MonitorStatus.ACTIVE:
            logger.debug(
                f"_actual_save_tab_data: Status is {self._status}, skipping save for {tab_id}."
            )
            return

        # --- Fetch Latest Tab Reference (including HTML) --- #
        tab_ref: Optional[TabReference] = None
        try:
            # Get current tabs to find the websocket URL for the target tab ID
            current_tabs: List[ChromeTab] = await get_tabs()
            target_tab_obj = next((t for t in current_tabs if t.id == tab_id), None)

            if not target_tab_obj:
                logger.warning(
                    f"_actual_save_tab_data: Could not find tab info for {tab_id}. Cannot save."
                )
                return
            if not target_tab_obj.webSocketDebuggerUrl:
                logger.warning(
                    f"_actual_save_tab_data: Tab {tab_id} has no websocket URL. Cannot fetch HTML."
                )
                return

            # Fetch the latest HTML content, URL, and Title
            html_content, current_url, latest_title = await self.chrome_manager.get_tab_html(
                ws_url=target_tab_obj.webSocketDebuggerUrl,
                initial_url=target_tab_obj.url,  # Pass current known URL
                title=target_tab_obj.title,  # Pass current known title
            )

            if html_content is None or not current_url:
                logger.warning(
                    f"_actual_save_tab_data: Failed to fetch HTML or URL for tab {tab_id}. Skipping save."
                )
                return

            # Create the TabReference with the freshly fetched data
            tab_ref = TabReference(
                id=tab_id, url=current_url, html=html_content, title=latest_title
            )

        except Exception as fetch_err:
            logger.error(
                f"_actual_save_tab_data: Error fetching latest data for tab {tab_id}: {fetch_err}",
                exc_info=True,
            )
            return  # Don't proceed if fetching failed
        # --- End Fetch --- #

        # --- Proceed with existing logic using the fetched tab_ref --- #
        if not tab_ref:  # Should not happen if fetch succeeded, but check anyway
            logger.error(
                f"_actual_save_tab_data: tab_ref is None after fetch for {tab_id}. Aborting."
            )
            return

        normalized_url = normalize_url(tab_ref.url)
        html_content = tab_ref.html  # Use the fetched HTML

        # --- Check if content should be saved (uses markdown hash internally) --- #
        _save_flag, _reason, content_hash = should_save_content(normalized_url, html_content)
        if not _save_flag:
            return

        # --- Pre-enqueue Hash Check (using Normalized URL) --- #
        if content_hash:
            session: Optional[Session] = None
            try:
                session = sqlite_manager.get_session()
                if session:
                    existing_hash = (
                        session.query(Item.content_hash).filter(Item.url == normalized_url).scalar()
                    )
                    if existing_hash == content_hash:
                        logger.debug(
                            f"Skipping enqueue for {normalized_url}, content unchanged (DB hash match: {content_hash[:8]})."
                        )
                        return  # Skip enqueueing
                    # else: Hash differs or no existing hash, proceed.
                else:
                    logger.warning(
                        f"Could not get DB session to check hash for {normalized_url}. Proceeding to enqueue."
                    )
            except Exception as db_err:
                logger.error(
                    f"Error checking existing hash for {normalized_url}: {db_err}. Proceeding to enqueue.",
                    exc_info=True,
                )
            finally:
                if session:
                    session.close()
        elif _save_flag:
            # This case means should_save returned True but no hash (e.g., markdown failed?)
            # The should_save logic should prevent this, but log defensively.
            logger.warning(
                f"Proceeding to enqueue {normalized_url} but content_hash was None after should_save check returned True."
            )
        # --- End pre-enqueue hash check --- #

        # --- Parse Content and Schedule Next Task --- #
        # Only reach here if _save_flag is True and (no content_hash OR hash check passed/no existing item)
        parser = get_parser_for_url(normalized_url)
        if not parser:
            logger.debug(f"No parser found for URL: {normalized_url}. Skipping further processing.")
            return

        if not html_content:
            logger.error(
                f"Cannot parse {normalized_url}: html_content became None unexpectedly after should_save check."
            )
            return

        try:
            parse_results: List[ParseResult] = parser.parse(html_content, url=normalized_url)
            if not parse_results:
                logger.debug(f"No items parsed from {normalized_url}.")
                return

            logger.info(
                f"Parsing {normalized_url} yielded {len(parse_results)} items. Collecting for batch processing..."
            )

            items_to_summarize: List[SummaryItem] = []
            items_ready_to_save: List[ProcessingItem] = []

            for result in parse_results:
                if result.status == "needs_summary":
                    summary_item = cast(SummaryItem, result.data)
                    if summary_item:
                        # Ensure URL is set before adding
                        summary_item.url = normalized_url
                        items_to_summarize.append(summary_item)
                    else:
                        logger.error(
                            f"ParseResult status is 'needs_summary' but data is missing for {normalized_url}"
                        )
                elif result.status == "ready_to_embed":
                    processing_item = cast(ProcessingItem, result.data)
                    if processing_item:
                        items_ready_to_save.append(processing_item)
                    else:
                        logger.error(
                            f"ParseResult status is 'ready_to_embed' but data is missing for {normalized_url}"
                        )
                elif result.status == "failed":
                    logger.warning(
                        f"Skipping failed parse result for {normalized_url}: {result.error}"
                    )
                else:
                    logger.error(
                        f"Unknown ParseResult status '{result.status}' for {normalized_url}"
                    )

            # --- Schedule Batch Tasks --- #
            if items_to_summarize:
                try:
                    summarize_list_json = json.dumps(
                        [item.model_dump_json() for item in items_to_summarize]
                    )
                    from starfruit.tasks.consumer import batch_summarize_items

                    # logger.debug(
                    #     f"Scheduling batch_summarize_items with payload: {summarize_list_json[:200]}..."
                    # )  # Log payload
                    batch_summarize_items.schedule(args=(summarize_list_json,), delay=0.1)
                    logger.debug(
                        f"Enqueued batch_summarize_items for {len(items_to_summarize)} items from {normalized_url}"
                    )
                except Exception as schedule_err:
                    logger.error(
                        f"Error scheduling batch_summarize_items for {normalized_url}: {schedule_err}",
                        exc_info=True,
                    )

            if items_ready_to_save:
                try:
                    save_list_json = json.dumps(
                        [item.model_dump_json() for item in items_ready_to_save]
                    )
                    # TODO: Replace with actual import when batch task exists
                    from starfruit.tasks.consumer import batch_save_to_sqlite

                    logger.debug(
                        f"Scheduling batch_save_to_sqlite with payload: {save_list_json[:200]}..."
                    )  # Log payload
                    batch_save_to_sqlite.schedule(args=(save_list_json,), delay=0.1)
                    logger.debug(
                        f"Enqueued batch_save_to_sqlite for {len(items_ready_to_save)} items from {normalized_url}"
                    )
                except Exception as schedule_err:
                    logger.error(
                        f"Error scheduling batch_save_to_sqlite for {normalized_url}: {schedule_err}",
                        exc_info=True,
                    )

        except Exception as parse_err:
            logger.error(f"Error during parsing for {normalized_url}: {parse_err}", exc_info=True)

    async def shutdown(self) -> None:
        """Gracefully shuts down the tab monitoring service."""
        logger.info("Shutting down TabMonitor...")
        await self.stop_monitoring()
        logger.info("TabMonitor shutdown complete.")
        try:
            await self.http_client.aclose()
            logger.info("HTTP client closed successfully.")
        except Exception as e:
            logger.error(f"Error closing HTTP client: {e}", exc_info=True)


# Instantiate singletons
chrome_manager = ChromeManager()
tab_monitor = TabMonitor(chrome_manager)
