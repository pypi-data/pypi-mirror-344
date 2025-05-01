import asyncio
import time
from typing import Dict, List, Optional, Tuple

import httpx
from pydantic import BaseModel
from sqlalchemy.orm import Session

from brocc.browser.chrome_cdp import ChromeTab, get_tabs
from brocc.browser.chrome_manager import ChromeManager
from brocc.browser.chrome_watcher import (
    ChromeWatcher,
    TabChangeEvent,
    TabReference,
)
from brocc.browser.determine_item_action import (
    ItemAction,
    ItemProcessingState,
    determine_item_action,
)
from brocc.browser.next_monitor_status import next_monitor_status
from brocc.db.sqlite_manager import sqlite_manager
from brocc.db.sqlite_models import Item
from brocc.internal.logger import get_logger
from brocc.internal.normalize_url import normalize_url
from brocc.parse.parser_registry import get_parser_for_url
from brocc.parse.types import ParsedContent
from brocc.server.debouncer import AsyncDebouncer
from brocc.server.types import MonitorStatus
from brocc.tasks.consumer import (
    batch_embed_raw_text,
    generate_summary_and_notify,
    upsert_to_db,
)

logger = get_logger(__name__)

SAVE_DEBOUNCE_DELAY_SECONDS = 2.0
EMBEDDING_BATCH_MAX_SIZE = 16
EMBEDDING_BATCH_MAX_WAIT_SECONDS = 15.0


class TabMonitorStatusRes(BaseModel):
    status: MonitorStatus
    details: Optional[str] = None
    is_chrome_connected: bool = False
    tabs_count: int = 0


class EmbeddingResultPayload(BaseModel):
    item_id: int
    url: str
    embedding: List[float]


class SummaryResultPayload(BaseModel):
    item_id: int
    url: str
    summary_text: str


class TabMonitor:
    def __init__(self, chrome_manager: ChromeManager):
        self.chrome_manager = chrome_manager
        self.http_client = httpx.AsyncClient()
        self.chrome_watcher: Optional[ChromeWatcher] = None
        self._monitoring_task: Optional[asyncio.Task] = None
        self._embedding_batcher_task: Optional[asyncio.Task] = None
        self._status = MonitorStatus.INACTIVE
        self._status_details: Optional[str] = None
        self._last_interacted_tab_id: Optional[str] = None
        self._save_debouncer = AsyncDebouncer(
            delay=SAVE_DEBOUNCE_DELAY_SECONDS, callback=self._save_tab_data
        )
        self._pending_items: Dict[str, ParsedContent] = {}
        self._completed_embeddings: Dict[str, List[float]] = {}
        self._completed_summaries: Dict[str, str] = {}
        self._processing_locks: Dict[str, asyncio.Lock] = {}
        self._embedding_batch_queue: List[Tuple[int, str, str]] = []
        self._embedding_queue_lock = asyncio.Lock()
        self._last_embedding_batch_time = time.monotonic()

    async def start_monitoring(self) -> bool:
        """Start the tab monitoring service and its background check loop."""
        if self._monitoring_task and not self._monitoring_task.done():
            logger.warning("TabMonitor background task already running.")
            if self.chrome_watcher and not self.chrome_watcher._monitoring:
                logger.info(
                    "Service loop running, but ChromeWatcher monitor stopped. Attempting to restart ChromeWatcher monitor..."
                )
                try:
                    await self._ensure_tabs_monitor_started()
                except Exception as e:
                    logger.error(f"Error restarting ChromeWatcher monitor: {e}", exc_info=True)
                    self._status = MonitorStatus.ERROR
                    self._status_details = f"Failed to restart ChromeWatcher: {e}"
            return True

        if self.chrome_watcher is None:
            self.chrome_watcher = ChromeWatcher(self.chrome_manager)

        self._monitoring_task = asyncio.create_task(self._run_monitoring_loop())
        self._embedding_batcher_task = asyncio.create_task(self._schedule_embedding_batcher())

        await self._run_initial_check()

        if self._status == MonitorStatus.ERROR:
            logger.error("Tab monitoring failed to start due to errors during initial check.")
            if self._monitoring_task and not self._monitoring_task.done():
                self._monitoring_task.cancel()
            if self._embedding_batcher_task and not self._embedding_batcher_task.done():
                self._embedding_batcher_task.cancel()
            return False

        return True

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
                                await self._save_debouncer.trigger(
                                    key=initial_ref.id, value=initial_ref.id
                                )
                    else:
                        logger.warning(
                            "Cannot save initial refs: chrome_watcher is None after start attempt."
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
            if self._monitoring_task and not self._monitoring_task.done():
                self._monitoring_task.cancel()
                try:
                    await self._monitoring_task
                except asyncio.CancelledError:
                    pass
                self._monitoring_task = None

            if self._embedding_batcher_task and not self._embedding_batcher_task.done():
                self._embedding_batcher_task.cancel()
                try:
                    await self._embedding_batcher_task
                except asyncio.CancelledError:
                    pass
                self._embedding_batcher_task = None

            await self._save_debouncer.shutdown()

            self._pending_items.clear()
            self._completed_embeddings.clear()
            self._completed_summaries.clear()
            async with self._embedding_queue_lock:
                self._embedding_batch_queue.clear()
            logger.info("Cleared in-memory state.")

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
        if new_status == self._status:
            return

        old_status = self._status
        self._status = new_status
        if new_status == MonitorStatus.PAUSED_CHROME_DISCONNECTED:
            self._status_details = "Chrome is disconnected"
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
        try:
            while True:
                await self.chrome_manager.refresh_state()
                chrome_connected = self.chrome_manager.connected

                next_status = next_monitor_status(
                    current_status=self._status,
                    chrome_connected=chrome_connected,
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
        tabs_to_trigger_save = set()
        for tab_info in event.new_tabs + event.navigated_tabs:
            tab_id = tab_info.get("id")
            url = tab_info.get("url")
            html_content = tab_info.get("html")

            if not tab_id or not url or url.startswith("chrome://") or url.startswith("about:"):
                continue

            if html_content:
                tabs_to_trigger_save.add(tab_id)
            else:
                if self.chrome_watcher:
                    try:
                        current_tabs: List[ChromeTab] = await get_tabs()
                        target_tab_obj = next((t for t in current_tabs if t.id == tab_id), None)
                        if target_tab_obj and target_tab_obj.webSocketDebuggerUrl:
                            fetched_html, _, _ = await self.chrome_manager.get_tab_html(
                                ws_url=target_tab_obj.webSocketDebuggerUrl,
                                initial_url=target_tab_obj.url,
                                title=target_tab_obj.title,
                            )
                            if fetched_html:
                                tabs_to_trigger_save.add(tab_id)
                    except Exception as fetch_err:
                        logger.error(
                            f"Polling update: Error fetching HTML for tab ID {tab_id}: {fetch_err}"
                        )
                else:
                    logger.warning("Chrome watcher is None, cannot fetch missing HTML.")

        for tid in tabs_to_trigger_save:
            await self._save_debouncer.trigger(key=tid, value=tid)

    async def _handle_interaction_update(self, tab_ref: TabReference):
        if not self._status == MonitorStatus.ACTIVE:
            return
        self._last_interacted_tab_id = tab_ref.id

    async def _handle_content_fetched(self, tab_ref: TabReference):
        if self._status != MonitorStatus.ACTIVE:
            return
        await self._save_debouncer.trigger(key=tab_ref.id, value=tab_ref.id)

    async def _fetch_and_parse_tab(self, tab_id: str) -> Optional[Tuple[str, List[ParsedContent]]]:
        """Fetches tab HTML, finds parser, and parses content.

        Returns:
            A tuple of (normalized_url, parsed_content_list) or None if fetching,
            parsing fails, or no suitable parser is found.
        """
        html_content: Optional[str] = None
        current_url: Optional[str] = None
        try:
            current_tabs: List[ChromeTab] = await get_tabs()
            target_tab_obj = next((t for t in current_tabs if t.id == tab_id), None)
            if not target_tab_obj:
                logger.warning(f"Could not find tab info for {tab_id}.")
                return None
            if not target_tab_obj.webSocketDebuggerUrl:
                logger.warning(f"Tab {tab_id} has no websocket URL. Cannot fetch HTML.")
                return None

            html_content, current_url, _ = await self.chrome_manager.get_tab_html(
                ws_url=target_tab_obj.webSocketDebuggerUrl,
                initial_url=target_tab_obj.url,
                title=target_tab_obj.title,
            )
            if html_content is None or not current_url:
                logger.warning(f"Failed to fetch HTML or URL for tab {tab_id}.")
                return None

        except Exception as fetch_err:
            logger.error(
                f"Error fetching data for tab {tab_id}: {fetch_err}",
                exc_info=True,
            )
            return None

        normalized_url = normalize_url(current_url)
        parser = get_parser_for_url(normalized_url)
        if not parser:
            logger.debug(f"No parser found for URL: {normalized_url}.")
            return None

        # Double check html_content, though should be caught above
        if not html_content:
            logger.error(f"html_content became None unexpectedly for {normalized_url}.")
            return None

        try:
            parsed_list: List[ParsedContent] = parser.parse(html_content, url=normalized_url)
            if not parsed_list:
                logger.debug(f"Parser yielded no items for {normalized_url}.")
                # Return the URL but an empty list, let caller decide if that's an error
                return normalized_url, []

            return normalized_url, parsed_list

        except Exception as parse_err:
            logger.error(f"Error parsing {normalized_url}: {parse_err}", exc_info=True)
            return None

    async def _process_parsed_items(self, normalized_url: str, parsed_items: List[ParsedContent]):
        """Processes parsed items: check/upsert metadata, update state, queue for embedding."""
        if not parsed_items:
            logger.debug(f"No items to process for {normalized_url}.")
            return

        logger.info(
            f"Processing {len(parsed_items)} parsed items from {normalized_url}. Checking DB..."
        )

        session: Optional[Session] = None
        try:
            session = sqlite_manager.get_session()
            if not session:
                logger.error(f"Failed to get DB session for {normalized_url}.")
                return  # Cannot proceed without session

            items_queued_count = 0
            for parsed_item in parsed_items:
                item_id = Item.check_and_upsert_metadata(session, parsed_item)
                if item_id is not None:
                    # Item is new or updated, needs embedding/summary check
                    lock = self._processing_locks.setdefault(parsed_item.url, asyncio.Lock())
                    async with lock:
                        # Check if another thread processed this already while waiting for lock
                        if parsed_item.url not in self._pending_items:
                            self._pending_items[parsed_item.url] = parsed_item

                            async with self._embedding_queue_lock:
                                self._embedding_batch_queue.append(
                                    (item_id, parsed_item.url, parsed_item.content_to_embed)
                                )
                                items_queued_count += 1
                                logger.debug(
                                    f"Added item {item_id} ({parsed_item.url}) to embedding queue."
                                )

                            # Trigger status check immediately after adding
                            await self._check_item_processing_status(item_id, parsed_item.url)
                        else:
                            logger.debug(
                                f"Item {item_id} ({parsed_item.url}) was already pending, skipping queue add."
                            )

            if items_queued_count == 0:
                logger.debug(
                    f"All parsed items from {normalized_url} were already up-to-date or pending."
                )

        except Exception as db_err:
            logger.error(
                f"Error during DB check/upsert for {normalized_url}: {db_err}",
                exc_info=True,
            )
        finally:
            if session:
                session.close()

    async def _save_tab_data(self, tab_id: str):
        """Orchestrates fetching, parsing, and processing tab data after debounce."""
        if self._status != MonitorStatus.ACTIVE:
            logger.debug(f"Status is {self._status}, skipping save for {tab_id}.")
            return

        try:
            # Step 1: Fetch and Parse
            parsed_data = await self._fetch_and_parse_tab(tab_id)

            # Step 2: Process if successful
            if parsed_data:
                normalized_url, parsed_list = parsed_data
                await self._process_parsed_items(normalized_url, parsed_list)
            # else: _fetch_and_parse_tab already logged the reason for None

        except Exception as e:
            # Catch unexpected errors during the orchestration steps
            logger.error(
                f"Unexpected error in _save_tab_data orchestration for tab {tab_id}: {e}",
                exc_info=True,
            )

    async def _schedule_embedding_batcher(self):
        while True:
            await asyncio.sleep(5)

            batch_to_process: List[Tuple[int, str, str]] = []
            now = time.monotonic()
            should_schedule = False

            async with self._embedding_queue_lock:
                queue_size = len(self._embedding_batch_queue)
                time_since_last = now - self._last_embedding_batch_time

                if queue_size >= EMBEDDING_BATCH_MAX_SIZE:
                    logger.info(
                        f"Embedding batch triggered by size ({queue_size} >= {EMBEDDING_BATCH_MAX_SIZE})."
                    )
                    should_schedule = True
                elif queue_size > 0 and time_since_last >= EMBEDDING_BATCH_MAX_WAIT_SECONDS:
                    logger.info(
                        f"Embedding batch triggered by time ({time_since_last:.1f}s >= {EMBEDDING_BATCH_MAX_WAIT_SECONDS}s). Size: {queue_size}."
                    )
                    should_schedule = True

                if should_schedule:
                    batch_to_process = list(self._embedding_batch_queue)
                    self._embedding_batch_queue.clear()
                    self._last_embedding_batch_time = now

            if batch_to_process:
                try:
                    batch_data_serializable = [list(item) for item in batch_to_process]
                    batch_embed_raw_text.schedule(args=(batch_data_serializable,), delay=0.1)
                    logger.info(
                        f"Scheduled batch_embed_raw_text task for {len(batch_to_process)} items."
                    )
                except Exception as schedule_err:
                    logger.error(
                        f"Error scheduling batch_embed_raw_text: {schedule_err}", exc_info=True
                    )
                    async with self._embedding_queue_lock:
                        logger.error("Failed batch will be dropped.")

    async def _check_item_processing_status(self, item_id: int, url: str):
        # Check if item is still pending (might have been processed/cleaned up by another path)
        parsed_item = self._pending_items.get(url)
        if not parsed_item:
            logger.debug(
                f"_check_item_processing_status: Item {item_id} ({url}) no longer pending. Likely processed or failed."
            )
            return

        # Gather current state for the item
        embedding = self._completed_embeddings.get(url)
        summary = self._completed_summaries.get(url)

        # Determine the correct content to potentially store
        content_to_store: Optional[str]
        if parsed_item.is_summary_required:
            content_to_store = (
                summary  # Use summary if required, even if None (checked by determine action)
            )
        else:
            content_to_store = (
                parsed_item.content_to_store
            )  # Use original content if summary not required

        current_state = ItemProcessingState(
            url=url,
            item_id=item_id,
            is_summary_required=parsed_item.is_summary_required,
            has_embedding=embedding is not None,
            has_summary=summary is not None,
            content_to_store=content_to_store,
            content_to_embed=parsed_item.content_to_embed,
            embedding=embedding,
        )

        # Determine the next action using the pure function
        action = determine_item_action(current_state)

        logger.debug(f"Action determined for item {item_id} ({url}): {action}")

        # Execute side effects based on the determined action
        if action == ItemAction.UPSERT_TO_DB:
            # Pre-conditions (content_to_store and embedding) are checked inside determine_item_action
            # If it returns UPSERT_TO_DB, we assume they are valid.
            if current_state.content_to_store is not None and current_state.embedding is not None:
                logger.info(f"Item {item_id} ({url}) ready for DB. Scheduling upsert task.")
                try:
                    # Schedule the task with validated state
                    upsert_to_db.schedule(
                        args=(item_id, current_state.content_to_store, current_state.embedding),
                        delay=0.1,
                    )
                    # Clean up state only after successful scheduling
                    self._cleanup_item_state(url)
                except Exception as schedule_err:
                    logger.error(
                        f"Failed to schedule upsert for {item_id} ({url}): {schedule_err}",
                        exc_info=True,
                    )
            else:
                # This should ideally not be reached due to checks in determine_item_action
                logger.error(
                    f"Internal Error: UPSERT action decided for {url}, but content_to_store or embedding is unexpectedly None. Cleaning up."
                )
                self._cleanup_item_state(url)

        elif action == ItemAction.GENERATE_SUMMARY:
            # Pre-condition (content_to_embed exists) checked inside determine_item_action
            logger.debug(
                f"Item {item_id} ({url}) needs summary. Scheduling generate_summary_and_notify task."
            )
            try:
                generate_summary_and_notify.schedule(
                    args=(item_id, url, current_state.content_to_embed), delay=0.1
                )
                # Do NOT clean up state here - waiting for summary result
            except Exception as schedule_err:
                logger.error(
                    f"Failed to schedule generate_summary_and_notify for {item_id} ({url}): {schedule_err}",
                    exc_info=True,
                )
                # If scheduling fails, clean up the state to prevent getting stuck.
                self._cleanup_item_state(url)

        elif action == ItemAction.WAIT:
            logger.debug(f"Item {item_id} ({url}) waiting for dependencies (embedding/summary).")
            # No state change, no cleanup needed. Waiting for next event.
            pass

        elif action == ItemAction.ERROR:
            logger.error(f"Error state determined for item {item_id} ({url}). Cleaning up.")
            self._cleanup_item_state(url)  # Clean up inconsistent state

    def _cleanup_item_state(self, url: str):
        _removed_pending = self._pending_items.pop(url, None)
        _removed_embed = self._completed_embeddings.pop(url, None)
        _removed_summary = self._completed_summaries.pop(url, None)
        _removed_lock = self._processing_locks.pop(url, None)
        if _removed_pending:
            logger.debug(f"Cleaned up in-memory state for {url}.")

    async def handle_embedding_result(self, data: EmbeddingResultPayload):
        logger.debug(f"Received embedding result for item {data.item_id} ({data.url})")
        lock = self._processing_locks.get(data.url)
        if lock:
            async with lock:
                if data.url not in self._pending_items:
                    logger.warning(
                        f"Received embedding for {data.url}, but item no longer pending. Discarding."
                    )
                    return
                self._completed_embeddings[data.url] = data.embedding
                await self._check_item_processing_status(data.item_id, data.url)
        else:
            logger.warning(
                f"Received embedding for {data.url}, but no processing lock found. Discarding."
            )

    async def handle_summary_result(self, data: SummaryResultPayload):
        logger.debug(f"Received summary result for item {data.item_id} ({data.url})")
        lock = self._processing_locks.get(data.url)
        if lock:
            async with lock:
                if data.url not in self._pending_items:
                    logger.warning(
                        f"Received summary for {data.url}, but item no longer pending. Discarding."
                    )
                    return
                self._completed_summaries[data.url] = data.summary_text
                await self._check_item_processing_status(data.item_id, data.url)
        else:
            logger.warning(
                f"Received summary for {data.url}, but no processing lock found. Discarding."
            )

    async def shutdown(self) -> None:
        logger.info("Shutting down TabMonitor...")
        await self.stop_monitoring()
        logger.info("TabMonitor shutdown complete.")
        try:
            await self.http_client.aclose()
            logger.info("HTTP client closed successfully.")
        except Exception as e:
            logger.error(f"Error closing HTTP client: {e}", exc_info=True)


chrome_manager = ChromeManager()
tab_monitor = TabMonitor(chrome_manager)
