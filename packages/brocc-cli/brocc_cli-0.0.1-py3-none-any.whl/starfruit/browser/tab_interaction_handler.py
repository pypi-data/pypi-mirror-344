import asyncio
from typing import Awaitable, Callable, List, Optional

import websockets

from starfruit.browser.chrome_cdp import ChromeTab, get_tabs, monitor_user_interactions
from starfruit.browser.chrome_manager import ChromeManager
from starfruit.browser.types import TabReference
from starfruit.internal.logger import get_logger

InteractionTabUpdateCallback = Callable[
    [TabReference], Awaitable[None]
]  # Called immediately on interaction (no fresh HTML)
ContentFetchedCallback = Callable[
    [TabReference], Awaitable[None]
]  # Called after interaction + fetch (with fresh HTML)

logger = get_logger(__name__)

DEBOUNCE_DELAY_SECONDS = 0.75  # Time to wait after last interaction before fetching


class TabInteractionHandler:
    """Handles interaction monitoring, debouncing, and fetching for a single tab."""

    def __init__(
        self,
        tab: ChromeTab,
        chrome_manager: ChromeManager,
        interaction_callback: InteractionTabUpdateCallback,
        content_fetched_callback: ContentFetchedCallback,
    ):
        self.tab = tab
        self.tab_id = tab.id
        self.ws_url = tab.webSocketDebuggerUrl
        self.chrome_manager = chrome_manager
        self.interaction_callback = interaction_callback
        self.content_fetched_callback = content_fetched_callback

        self._monitor_task: Optional[asyncio.Task] = None
        self._debounce_timer: Optional[asyncio.TimerHandle] = None
        self._fetch_task: Optional[asyncio.Task] = None
        self._is_running = False

    async def start(self):
        """Starts the interaction monitoring loop for the tab."""
        if self._is_running or not self.ws_url:
            if not self.ws_url:
                logger.warning(
                    f"Cannot start interaction monitor for tab {self.tab_id}: missing WebSocket URL."
                )
            return  # Already running or cannot run

        self._is_running = True
        self._monitor_task = asyncio.create_task(self._run_interaction_monitor_loop())
        # Add a callback to clean up if the task finishes unexpectedly
        self._monitor_task.add_done_callback(self._handle_monitor_completion)

    async def stop(self):
        """Stops the interaction monitoring loop and cleans up resources."""
        if not self._is_running:
            return  # Already stopped
        self._is_running = False
        # Cancel monitor task
        if self._monitor_task and not self._monitor_task.done():
            self._monitor_task.cancel()
            # Optionally await cancellation with timeout
            try:
                await asyncio.wait_for(self._monitor_task, timeout=1.0)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass  # Expected exceptions
            except Exception as e:
                logger.error(f"Error waiting for monitor task cancellation for {self.tab_id}: {e}")
        self._monitor_task = None

        # Cancel debounce timer
        if self._debounce_timer:
            self._debounce_timer.cancel()
            self._debounce_timer = None

        # Cancel fetch task
        if self._fetch_task and not self._fetch_task.done():
            self._fetch_task.cancel()
            try:
                await asyncio.wait_for(self._fetch_task, timeout=1.0)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass  # Expected exceptions
            except Exception as e:
                logger.error(f"Error waiting for fetch task cancellation for {self.tab_id}: {e}")
        self._fetch_task = None
        # logger.debug(f"Interaction monitor stopped for tab {self.tab_id}") # Reduced noise

    def _handle_monitor_completion(self, task: asyncio.Task):
        """Callback executed when the monitor task finishes (normally or abnormally)."""
        if self._is_running:  # If it stopped unexpectedly while we thought it was running
            logger.warning(f"Interaction monitor task for {self.tab_id} completed unexpectedly.")
            try:
                # Log exception if task failed
                exc = task.exception()
                if exc:
                    logger.error(
                        f"Interaction monitor task for {self.tab_id} failed: {exc}", exc_info=exc
                    )
            except asyncio.CancelledError:
                logger.debug(
                    f"Interaction monitor task for {self.tab_id} was cancelled."
                )  # Normal stop
            except asyncio.InvalidStateError:
                logger.debug(
                    f"Interaction monitor task for {self.tab_id} completion state invalid."
                )  # Shouldn't happen

            # Ensure cleanup happens even if task dies
            asyncio.create_task(self.stop())  # Schedule stop if it wasn't initiated

    async def _run_interaction_monitor_loop(self):
        """The actual monitoring loop for the tab's interactions via WebSocket."""
        if not self.ws_url:
            return  # Guard

        try:
            async for _event in monitor_user_interactions(self.ws_url):
                if not self._is_running:
                    logger.debug(
                        f"Interaction monitoring stopped for tab {self.tab_id}, exiting loop."
                    )
                    break

                # Create a TabReference for the callback using the initially known tab info
                interaction_tab_ref = TabReference(
                    id=self.tab.id,
                    url=self.tab.url,
                    title=self.tab.title,
                    html=None,  # HTML is not relevant for the interaction *trigger* callback
                )
                # Call the originally provided callback (e.g., to immediately indicate activity)
                # Schedule the callback correctly, handling both sync and async cases
                if asyncio.iscoroutinefunction(self.interaction_callback):
                    # Use create_task for the immediate interaction signal
                    asyncio.create_task(self.interaction_callback(interaction_tab_ref))
                else:
                    # Run sync callback directly (might block loop briefly if slow)
                    try:
                        # Although InteractionTabUpdateCallback is async, handle potential sync case defensively
                        result = self.interaction_callback(interaction_tab_ref)
                        if asyncio.iscoroutine(result):
                            asyncio.create_task(result)  # If it returns a coroutine, run it
                    except Exception as sync_cb_exc:
                        logger.error(
                            f"Error executing sync interaction callback for tab {self.tab_id}: {sync_cb_exc}",
                            exc_info=True,
                        )

                # Also, handle debouncing to fetch content later
                self._handle_interaction_event()  # No event_type needed here

        except websockets.exceptions.ConnectionClosedOK:
            logger.debug(f"ws connection closed normally for tab {self.tab_id}.")
        except websockets.exceptions.ConnectionClosedError as e:
            logger.warning(f"ws connection closed with error for tab {self.tab_id}: {e}")
        except websockets.exceptions.InvalidStatus as e:
            # Handle cases where the tab vanished
            # Use getattr for safety, although status_code should exist
            status_code = getattr(e, "status_code", None)
            if status_code == 500 and "No such target id" in str(e):
                logger.warning(
                    f"Interaction monitor for {self.tab_id} ({self.ws_url}) failed: Target ID disappeared (HTTP 500). Stopping handler."
                )
                # Task completion callback will handle stop()
            else:
                logger.error(
                    f"Unexpected InvalidStatus in interaction monitor for tab {self.tab_id}: {e}",
                    exc_info=True,
                )
        except Exception as e:
            logger.error(
                f"Error in interaction monitor loop for tab {self.tab_id}: {e}", exc_info=True
            )
        finally:
            pass
            # logger.debug(f"Interaction monitor loop finished for tab {self.tab_id}")
            # Let the done callback handle cleanup

    def _handle_interaction_event(self):
        """Handles a detected interaction event by resetting the debounce timer."""
        # Cancel existing timer, if any
        if self._debounce_timer:
            self._debounce_timer.cancel()

        # Schedule the debounced fetch function
        loop = asyncio.get_running_loop()
        self._debounce_timer = loop.call_later(
            DEBOUNCE_DELAY_SECONDS,
            lambda: asyncio.create_task(self._trigger_debounced_fetch()),
        )

    async def _trigger_debounced_fetch(self):
        """Callback executed after the debounce delay. Starts the HTML fetch task."""
        self._debounce_timer = None  # Timer has fired

        # Prevent concurrent fetches for the same tab initiated by interactions
        if self._fetch_task and not self._fetch_task.done():
            logger.debug(
                f"Fetch already in progress for tab {self.tab_id}, skipping debounced trigger."
            )
            return

        # Run the fetch in the background
        self._fetch_task = asyncio.create_task(self._fetch_and_process_tab_content())

        # Ensure the task reference is cleared once it completes
        self._fetch_task.add_done_callback(lambda _task: setattr(self, "_fetch_task", None))

    async def _fetch_and_process_tab_content(self):
        """Fetches HTML for the tab and calls the content_fetched_callback, only if URL is parsable."""
        """Fetches HTML for the tab and calls the content_fetched_callback."""  # Updated docstring
        try:
            # Get the current tab info first
            current_tabs: List[ChromeTab] = await get_tabs()
            target_tab_obj = next((t for t in current_tabs if t.id == self.tab_id), None)

            if not target_tab_obj:
                logger.warning(
                    f"Could not find tab {self.tab_id} info for fetching. Aborting update."
                )
                return
            if not target_tab_obj.webSocketDebuggerUrl:
                logger.warning(
                    f"Tab {self.tab_id} has no websocket URL. Cannot fetch HTML. Aborting update."
                )
                return

            html_content, current_url, latest_title = await self.chrome_manager.get_tab_html(
                ws_url=target_tab_obj.webSocketDebuggerUrl,
                initial_url=target_tab_obj.url,
                title=target_tab_obj.title,
            )

            if not current_url or html_content is None:  # Check html_content too
                logger.warning(
                    f"Could not determine URL or fetch HTML for tab {self.tab_id} during fetch. Aborting update."
                )
                return

            fetched_tab_ref = TabReference(
                id=self.tab_id, url=current_url, html=html_content, title=latest_title
            )

            # Call the dedicated callback with the *complete* TabReference
            if asyncio.iscoroutinefunction(self.content_fetched_callback):
                asyncio.create_task(self.content_fetched_callback(fetched_tab_ref))
            else:
                # Handle potential sync callback defensively
                try:
                    result = self.content_fetched_callback(fetched_tab_ref)
                    if asyncio.iscoroutine(result):
                        asyncio.create_task(result)
                except Exception as sync_cb_exc:
                    logger.error(
                        f"Error executing sync content_fetched_callback for tab {self.tab_id}: {sync_cb_exc}",
                        exc_info=True,
                    )

        except Exception as e:
            logger.error(
                f"Error fetching/processing tab {self.tab_id} after interaction: {e}", exc_info=True
            )
