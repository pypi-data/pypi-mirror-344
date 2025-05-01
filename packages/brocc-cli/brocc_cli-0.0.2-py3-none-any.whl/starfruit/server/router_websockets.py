from typing import Any, Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from pydantic import BaseModel, Field

from starfruit.internal.logger import get_logger
from starfruit.server.frontend_ws_manager import frontend_manager

logger = get_logger(__name__)
router = APIRouter(prefix="/ws")


# Pydantic model for the notification payload
class NotifyUpdatePayload(BaseModel):
    item_count: Optional[int] = Field(None, description="Total number of items in the table")
    db_size_mb: Optional[float] = Field(None, description="Total size of the database in MB")


@router.websocket("/frontend/updates")
async def websocket_frontend_endpoint(websocket: WebSocket):
    """Handles websocket connections from the frontend app."""
    await frontend_manager.connect(websocket)
    try:
        while True:
            # Listen for messages (primarily to detect disconnects)
            # Frontend doesn't currently send messages, but we keep the loop
            # to maintain the connection state.
            data = await websocket.receive_text()  # Or receive_json if expecting json
            logger.debug(
                f"Received unexpected message from frontend client {websocket.client}: {data}"
            )
    except WebSocketDisconnect:
        logger.info(f"Frontend client {websocket.client} initiated disconnect.")
        # No need to call disconnect explicitly here, the finally block handles it.
    except Exception as e:
        logger.error(
            f"Error in frontend websocket connection {websocket.client}: {e}", exc_info=True
        )
        # The finally block will ensure disconnection on errors.
    finally:
        # Ensure disconnection happens regardless of how the loop exits
        frontend_manager.disconnect(websocket)


# Internal endpoint for tasks to trigger frontend updates
@router.post("/frontend/internal/notify_update", status_code=status.HTTP_202_ACCEPTED)
async def notify_frontend_update(payload: NotifyUpdatePayload):
    """Internal endpoint triggered by background tasks to notify frontend of data changes."""
    # Log the received payload
    try:
        # Construct base broadcast message with explicit Any type for values
        broadcast_message: dict[str, Any] = {"type": "data_updated", "source": "task_completion"}

        # Add stats to the message if they exist in the payload
        if payload.item_count is not None:
            broadcast_message["item_count"] = payload.item_count
        if payload.db_size_mb is not None:
            broadcast_message["db_size_mb"] = payload.db_size_mb

        # Use send_json for frontend clients
        logger.info(f"Broadcasting WS message to frontend: {broadcast_message}")
        await frontend_manager.broadcast(broadcast_message)
        return {"status": "notification_sent", "details": payload.model_dump(exclude_none=True)}
    except Exception as e:
        logger.error(f"Failed to broadcast frontend update: {e}", exc_info=True)
        # Don't raise HTTPException here, as the task itself succeeded.
        # The endpoint should still return 202 Accepted.
        return {"status": "broadcast_failed", "details": payload.model_dump(exclude_none=True)}
