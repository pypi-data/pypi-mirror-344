import webbrowser

import httpx
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from starfruit.internal.auth_data import (
    is_logged_in,
    load_auth_data,
    save_auth_data,
)
from starfruit.internal.auth_data import (
    logout as clear_local_auth_data,
)
from starfruit.internal.logger import get_logger
from starfruit.internal.site_api_client import req_get_noauth

logger = get_logger(__name__)

router = APIRouter(prefix="/auth")


class AuthStatusResponse(BaseModel):
    is_logged_in: bool = Field(..., description="Indicates if the user is currently logged in.")
    email: str | None = Field(None, description="The email of the logged-in user, if available.")


class LoginStartResponse(BaseModel):
    auth_url: str = Field(..., description="The URL to open in the browser for authentication.")
    session_id: str = Field(..., description="The session ID to use for polling.")


class LoginPollResponse(BaseModel):
    status: str = Field(..., description="Polling status (e.g., 'pending', 'complete', 'error').")
    email: str | None = Field(None, description="User email if login is complete.")
    message: str | None = Field(None, description="Optional message, e.g., for errors.")


@router.get("/status", response_model=AuthStatusResponse)
async def get_auth_status():
    """
    Check the current authentication status based on saved credentials.
    """
    auth_data: dict | None = load_auth_data()
    logged_in = is_logged_in(auth_data)
    email = auth_data.get("email") if auth_data and logged_in else None

    return AuthStatusResponse(is_logged_in=logged_in, email=email)


@router.get("/login/start", response_model=LoginStartResponse)
async def start_login():
    # Use endpoint path instead of full URL
    start_endpoint = "/auth/cli/start"
    logger.debug(f"Initiating login via endpoint: {start_endpoint}")
    try:
        # Use the imported helper, passing the logger
        response = await req_get_noauth(start_endpoint, caller_logger=logger)
        data = response.json()
        auth_url = data.get("authUrl")
        session_id = data.get("sessionId")

        # Explicitly check for None or empty strings
        if not auth_url or not session_id:
            logger.error(
                f"Invalid response from site API {start_endpoint}. Missing 'authUrl' or 'sessionId'. Response data: {data}"
            )
            raise Exception(f"Invalid response from site API {start_endpoint}")

        logger.debug(f"Opening auth URL in browser: {auth_url}")
        try:
            # Run webbrowser.open in a separate thread to avoid blocking? (Consider if this causes issues)
            # For now, keep it simple.
            webbrowser.open(auth_url)
        except Exception as wb_err:
            # Log the error but don't fail the whole request, just inform the user
            logger.warning(
                f"Failed to open browser automatically: {wb_err}. User may need to copy the URL."
            )
            pass  # Continue execution, the URL is still returned

        return LoginStartResponse(auth_url=auth_url, session_id=session_id)
    except Exception:
        # Log the specific exception before re-raising
        logger.error(
            f"Login start failed during request to {start_endpoint} or processing response.",
            exc_info=True,  # Include stack trace
        )
        # Re-raise the exception so FastAPI can handle it (usually results in 500)
        raise


@router.get("/login/poll", response_model=LoginPollResponse)
async def poll_login_status(session_id: str):
    # Use endpoint path
    token_endpoint = f"/auth/cli/token?sessionId={session_id}"
    logger.debug(f"Polling login status via endpoint: {token_endpoint}")
    try:
        # Use the imported helper, passing the logger
        response = await req_get_noauth(token_endpoint, caller_logger=logger)
        data = response.json()

        if data.get("status") == "complete":
            logger.info(
                f"Authentication complete via polling. API key received: {bool(data.get('apiKey'))}"
            )
            auth_data = {
                "accessToken": data["accessToken"],
                "userId": data["userId"],
                "email": data.get("email"),
                "apiKey": data.get("apiKey"),
                "_source": "fastapi-poll",
            }
            save_auth_data(auth_data)  # Save on the server side
            return LoginPollResponse(status="complete", email=auth_data.get("email"), message=None)
        else:
            # Still pending or other status from main API
            logger.debug(f"Polling status: {data.get('status', 'unknown')}")
            return LoginPollResponse(status=data.get("status", "pending"), email=None, message=None)

    except httpx.HTTPStatusError as e:
        # Handle specific errors if needed, e.g., 404 might mean session expired
        logger.warning(f"Polling error: {e.response.status_code}")
        return LoginPollResponse(
            status="error", email=None, message=f"Polling failed: {e.response.status_code}"
        )
    except Exception as e:
        logger.error(f"Polling failed: {e}")
        return LoginPollResponse(status="error", email=None, message=f"Polling failed: {e}")


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user():
    """
    Logs the user out by clearing locally stored authentication data.
    """
    success = clear_local_auth_data()
    if success:
        return {"message": "Logged out successfully."}
    else:
        # Logged in logger.error already
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear authentication data.",
        )
