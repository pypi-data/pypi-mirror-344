from typing import Any, Dict, Set

from fastapi import WebSocket, WebSocketDisconnect

from starfruit.internal.logger import get_logger

logger = get_logger(__name__)


class FrontendWsManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Frontend WebSocket connected: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Frontend WebSocket disconnected: {websocket.client}")
        else:
            logger.debug(
                f"Attempted to disconnect already removed frontend websocket: {websocket.client}"
            )

    async def broadcast(self, message: Dict[str, Any]):
        if not self.active_connections:
            logger.debug("Frontend broadcast requested but no active connections.")
            return

        disconnected_clients = set()
        # Use list() to avoid modifying the set during iteration
        for connection in list(self.active_connections):
            try:
                # Use send_json for frontend clients
                await connection.send_json(message)
            except WebSocketDisconnect:
                logger.warning(
                    f"Frontend client {connection.client} disconnected during broadcast."
                )
                disconnected_clients.add(connection)
            except RuntimeError as e:
                # Catch specific error if connection closed unexpectedly during send
                if "Connection is closed" in str(e):
                    logger.warning(
                        f"Frontend client {connection.client} runtime error (closed) during broadcast."
                    )
                    disconnected_clients.add(connection)
                else:
                    logger.error(
                        f"Runtime error broadcasting to frontend client {connection.client}: {e}",
                        exc_info=False,  # Keep log less noisy for common runtime errors
                    )
                    disconnected_clients.add(connection)  # Also remove on unknown runtime errors
            except Exception as e:
                logger.error(
                    f"Unexpected error broadcasting to frontend client {connection.client}: {e}",
                    exc_info=True,
                )
                disconnected_clients.add(connection)  # Assume connection is broken

        # Remove disconnected clients
        for client in disconnected_clients:
            # Ensure disconnect wasn't already handled by another event
            if client in self.active_connections:
                self.disconnect(client)


# Singleton instance
frontend_manager = FrontendWsManager()
