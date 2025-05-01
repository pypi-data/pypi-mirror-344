import logging
from typing import Any, Dict, Optional

import httpx

from starfruit.internal.auth_data import load_auth_data
from starfruit.internal.env import starfruit_api_url
from starfruit.internal.logger import get_logger

logger = get_logger(__name__)


async def _make_request(
    method: str,
    endpoint: str,
    headers: Optional[Dict[str, str]] = None,
    json_data: Optional[Any] = None,
    timeout: float = 10.0,
    caller_logger: Optional[logging.Logger] = None,
) -> httpx.Response:
    """internal helper to make HTTP requests to the site API."""
    request_logger = caller_logger or logger
    base_url = starfruit_api_url()
    url = f"{base_url}{endpoint}" if endpoint.startswith("/") else f"{base_url}/{endpoint}"
    async with httpx.AsyncClient() as client:
        try:
            request_kwargs = {"headers": headers, "timeout": timeout}
            if json_data is not None:
                request_kwargs["json"] = json_data
            if method.upper() == "GET":
                response = await client.get(url, **request_kwargs)
            elif method.upper() == "POST":
                response = await client.post(url, **request_kwargs)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()  # Raise exception for 4xx/5xx errors
            return response
        except httpx.RequestError as e:
            request_logger.error(f"Error requesting {url} ({method}): {e}")
            raise  # Re-raise to allow caller-specific handling
        except httpx.HTTPStatusError as e:
            # Log potentially sensitive info carefully
            response_text_preview = e.response.text[:200] if hasattr(e, "response") else "N/A"
            request_logger.error(
                f"API returned error for {url} ({method}): {e.response.status_code} - {response_text_preview}"
            )
            raise  # Re-raise to allow caller-specific handling
        except ValueError as e:  # Catch the unsupported method error
            request_logger.error(f"Configuration error for {url} ({method}): {e}")
            raise  # Re-raise configuration errors
        except Exception as e:
            request_logger.error(
                f"Unexpected error during API request to {url} ({method}): {e}", exc_info=True
            )
            raise  # Re-raise unexpected errors


async def req_get_noauth(
    endpoint: str, method: str = "GET", caller_logger: Optional[logging.Logger] = None
) -> httpx.Response:
    """make unauthenticated requests to the site API as part of the auth flow"""
    return await _make_request(method=method, endpoint=endpoint, caller_logger=caller_logger)


async def req_get(
    endpoint: str, timeout: float = 10.0, caller_logger: Optional[logging.Logger] = None
) -> Optional[httpx.Response]:
    """make an authenticated GET request to the site API"""
    request_logger = caller_logger or logger
    auth_data = load_auth_data()
    api_key = auth_data.get("apiKey") if auth_data else None
    if not api_key:
        request_logger.error("Cannot make authenticated request: API key not found in auth data.")
        return None

    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        # Use the helper function for the actual request
        response = await _make_request(
            method="GET",
            endpoint=endpoint,
            headers=headers,
            timeout=timeout,
            caller_logger=request_logger,  # Pass the specific logger
        )
        return response
    except (httpx.RequestError, httpx.HTTPStatusError, ValueError, Exception) as e:
        request_logger.debug(
            f"Caught exception in req_get wrapper for {endpoint}, returning None: {type(e).__name__}"
        )
        # TODO: maybe clear auth data if 401 (consider moving this logic here if needed)
        # if isinstance(e, httpx.HTTPStatusError) and e.response.status_code == 401:
        #     logger.warning("API key rejected (401), consider clearing auth data.")
        #     # clear_auth_data() # Be careful with automatic clearing
        return None
