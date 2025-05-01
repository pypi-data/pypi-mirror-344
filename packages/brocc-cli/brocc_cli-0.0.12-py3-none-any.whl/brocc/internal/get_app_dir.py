from pathlib import Path

from platformdirs import user_config_dir

from brocc.internal.const import APP_DIR_NAME
from brocc.internal.logger import get_logger

logger = get_logger(__name__)


def get_app_dir() -> Path:
    app_dir = Path(user_config_dir(APP_DIR_NAME))
    logger.info(f"[get_app_dir] Calculated app_dir: {app_dir}")
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir
