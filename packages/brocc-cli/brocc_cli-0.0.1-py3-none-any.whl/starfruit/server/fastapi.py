import asyncio
import logging
import threading
import webbrowser
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, HttpUrl
from starlette.middleware.cors import CORSMiddleware

from starfruit.internal.const import API_HOST, API_PORT
from starfruit.internal.get_version import get_version
from starfruit.internal.logger import get_logger
from starfruit.server.router_auth import router as auth_router
from starfruit.server.router_chrome import (
    router as chrome_router,
)
from starfruit.server.router_chrome import (
    tab_monitor,
    try_initial_connect,
)
from starfruit.server.router_data import router as data_router
from starfruit.server.router_websockets import router as websockets_router
from starfruit.server.router_webview import router as webview_router

logger = get_logger(__name__)

STATIC_DIR = Path(__file__).parent.parent / "static"


# --- Lifespan Management ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Attempt initial Chrome connection in the background
    asyncio.create_task(try_initial_connect(quiet=False))
    # Attempt to start monitoring after ensuring Chrome connection attempt
    asyncio.create_task(tab_monitor.start_monitoring())
    # Load models
    # await _load_models_on_startup(app)

    yield  # Application runs here

    try:
        await tab_monitor.shutdown()
    except Exception as e:
        logger.error(f"Error shutting down tab monitor service: {e}", exc_info=True)

    logger.info("FastAPI app shutdown complete (lifespan).")


app = FastAPI(
    title="starfruit server",
    description="internal eternals",
    version="unknown",  # TODO: This might be better sourced dynamically
    lifespan=lifespan,  # Use the lifespan context manager
)
# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(webview_router)
app.include_router(auth_router)
app.include_router(chrome_router)
app.include_router(websockets_router)
app.include_router(data_router)

# Mount static assets directory (where Vite puts assets, js, css files)
assets_dir = STATIC_DIR / "assets"
if assets_dir.exists() and assets_dir.is_dir():
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    logger.debug(f"Mounted static assets from {assets_dir}")
else:
    logger.warning(f"Static assets directory not found at {assets_dir}. Frontend failed to load.")


# --- ROUTES ---
@app.get("/")
async def root():
    """Serve the index.html as the default page"""
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        logger.error(f"index.html not found at {index_file}")
        # Return a simple message or a more informative JSON response
        return JSONResponse(
            {
                "error": "Frontend not built. Run 'make build' in 'webapp' directory.",
                "detail": f"Expected index.html at {index_file}",
            },
            status_code=500,
        )
    return FileResponse(index_file)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "version": get_version(),
    }


class OpenUrlRequest(BaseModel):
    url: HttpUrl  # Use HttpUrl for basic validation


@app.post("/open_url")
async def open_url_in_browser(request: OpenUrlRequest):
    try:
        opened = webbrowser.open(str(request.url))  # Convert HttpUrl to string for webbrowser
        if opened:
            logger.info(f"Successfully requested to open URL: {request.url}")
            return {"message": f"Attempted to open URL: {request.url}"}
        else:
            logger.warning(
                f"webbrowser.open returned False for URL: {request.url}. It might not have opened."
            )
            return {
                "message": f"Attempted to open URL: {request.url}, but browser might not have opened."
            }
    except Exception as e:
        logger.error(f"Failed to open URL {request.url}: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"message": f"Error opening URL: {e}"})


# --- Logging Endpoint ---
class LogRequest(BaseModel):
    level: str = Field(
        ..., pattern="^(debug|info|warning|error|critical)$|^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
    )
    message: str
    logger_name: str = "webview_remote"  # Default logger name if not provided


@app.post("/log", status_code=204)
async def receive_log(request: LogRequest):
    """Receives log messages from other processes (like webview)."""
    remote_logger = get_logger(request.logger_name)
    log_level = getattr(logging, request.level.upper(), None)

    if log_level:
        remote_logger.log(log_level, request.message)
    else:
        # Fallback or error if level is somehow invalid despite Pydantic validation
        logger.error(f"Invalid log level received: {request.level} for message: {request.message}")
    # No response body needed, status 204 indicates success with no content


# --- LIFECYCLE ---


def start_server(host=API_HOST, port=API_PORT):
    try:
        logger.debug(f"starting FastAPI server, docs: http://{host}:{port}/docs")
        uvicorn.run(app, host=host, port=port, log_level="info")
    except OSError as e:
        # Catch specific error for address in use
        if (
            e.errno == 48 or "address already in use" in str(e).lower()
        ):  # Check errno 48 for macOS/Linux
            logger.error(f"FATAL: Port {port} is already in use! Cannot start server.")
            # Optionally, re-raise or exit differently if needed
        else:
            logger.error(f"Network error starting FastAPI server: {e}")
    except Exception as e:
        logger.error(f"Error starting FastAPI server: {e}")


def run_server_in_thread(host=API_HOST, port=API_PORT):
    server_thread = threading.Thread(
        target=run_uvicorn,
        args=(app, host, port, False),
        daemon=True,  # make sure thread closes when main app closes
        name=f"FastAPI-{host}-{port}",
    )
    server_thread.start()
    return server_thread


def run_uvicorn(app, host: str, port: int, reload: bool):
    try:
        uvicorn.run(app, host=host, port=port, reload=reload, log_config=None)
        logger.debug(
            f"uvicorn.run({host}, {port}) completed (should not happen unless server stops)."
        )
    except Exception as e:
        logger.error(f"uvicorn.run({host}, {port}) CRASHED: {e}", exc_info=True)
    finally:
        logger.debug(f"exiting target function for {host}:{port}")


# serve index.html for all other paths (SPA routing pattern)
# NOTE: this MUST be the LAST route defined
@app.get("/{full_path:path}")
async def serve_static_or_index(request: Request, full_path: str):
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        logger.error(f"index.html not found at {index_file} (requested path: /{full_path})")
        return JSONResponse(
            {
                "error": "Frontend assets not found. Run 'make build' in 'webapp' directory.",
                "detail": f"Expected index.html at {index_file}",
            },
            status_code=500,
        )
    # Check if the requested path looks like a file extension we shouldn't serve index.html for
    # This prevents backend API paths potentially clashing if not defined before this route
    # A more robust solution might involve checking if full_path matches known API prefixes
    if "." in Path(full_path).name and not full_path.endswith(".html"):
        logger.debug(f"path /{full_path} looks like a file, returning 404 for SPA catch-all")
        return JSONResponse({"detail": "Not Found"}, status_code=404)

    logger.debug(f"serving index.html for path: /{full_path}")
    return FileResponse(index_file)


# NOTE: DO NOT ADD ADDITIONAL ROUTES BELOW ROUTING CATCH-ALL
