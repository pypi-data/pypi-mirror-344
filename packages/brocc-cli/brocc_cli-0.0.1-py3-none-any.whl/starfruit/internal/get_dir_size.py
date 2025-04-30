import os
from pathlib import Path

from starfruit.internal.logger import get_logger

logger = get_logger(__name__)


def get_dir_size(path: Path) -> int:
    """Recursively calculates the size of a directory."""
    total = 0
    # Check if path exists and is a directory before scanning
    if not path.exists() or not path.is_dir():
        logger.warning(f"Directory not found or not a directory: {path}")
        return 0
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat(follow_symlinks=False).st_size
                elif entry.is_dir(follow_symlinks=False):
                    total += get_dir_size(Path(entry.path))
            except OSError as e:
                # Log errors like permission denied but continue calculation
                logger.warning(f"Could not access {entry.path}: {e}")
    except OSError as e:
        logger.error(f"Error scanning directory {path}: {e}")
    return total
