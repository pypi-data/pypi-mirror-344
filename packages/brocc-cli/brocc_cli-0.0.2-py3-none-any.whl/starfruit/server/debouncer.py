import asyncio
from typing import Any, Awaitable, Callable, Dict

from starfruit.internal.logger import get_logger

logger = get_logger(__name__)


class AsyncDebouncer:
    """Debounces asynchronous calls based on a key."""

    def __init__(self, delay: float, callback: Callable[[Any], Awaitable[None]]):
        """
        Args:
            delay: The debounce delay in seconds.
            callback: The async function to call after the delay.
                      It will be called with the last value provided for the key.
        """
        self.delay = delay
        self.callback = callback
        self._timers: Dict[Any, asyncio.TimerHandle] = {}
        self._values: Dict[Any, Any] = {}
        self._lock = asyncio.Lock()  # Use asyncio.Lock for async context

    async def trigger(self, key: Any, value: Any):
        """Triggers the debounce mechanism for a given key."""
        async with self._lock:
            # Cancel existing timer for this key, if any
            if key in self._timers:
                self._timers[key].cancel()

            # Store the latest value
            self._values[key] = value

            # Schedule the callback execution
            loop = asyncio.get_running_loop()
            self._timers[key] = loop.call_later(self.delay, self._schedule_callback, key)

    def _schedule_callback(self, key: Any):
        # This method runs synchronously via call_later,
        # so we need to schedule the async callback execution in the loop
        loop = asyncio.get_running_loop()
        loop.create_task(self._execute_callback(key))

    async def _execute_callback(self, key: Any):
        value_to_process = None
        async with self._lock:
            # Check if the timer still exists (could have been cancelled right before lock acquisition)
            if key not in self._timers:
                return

            # Retrieve value and clean up
            value_to_process = self._values.pop(key, None)
            self._timers.pop(key, None)

        # Execute the callback outside the lock
        if value_to_process is not None:
            try:
                await self.callback(value_to_process)
            except Exception as e:
                logger.error(
                    f"Debouncer: Error executing callback for key '{key}': {e}",
                    exc_info=True,
                )
        else:
            logger.warning(
                f"Debouncer: Value for key '{key}' was missing during callback execution."
            )

    async def shutdown(self):
        """Cancels all pending debounce tasks."""
        async with self._lock:
            logger.info(f"Debouncer: Shutting down. Cancelling {len(self._timers)} pending timers.")
            for _key, timer in list(
                self._timers.items()
            ):  # Use list to avoid modification during iteration
                timer.cancel()
            self._timers.clear()
            self._values.clear()
