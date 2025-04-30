from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console

from starfruit.app import StarfruitApp
from starfruit.internal.logger import disable_console_logging, enable_console_logging, get_logger

# Determine the project root directory (assuming entry_points.py is in src/starfruit)
# Go up two levels: src/starfruit -> src -> cli
project_root = Path(__file__).parent.parent.parent

# Construct the path to the .env file in the cli directory
dotenv_path = project_root / ".env"

# Load the .env file if it exists
if dotenv_path.exists():
    load_dotenv(
        dotenv_path=dotenv_path, override=True
    )  # override=True ensures .env takes precedence
else:
    pass


logger = get_logger(__name__)
console = Console()


def start():
    try:
        enable_console_logging()
        # TODO: can add startup logic here, before TUI launches
        # e.g. pre-downloading small local models
        app = StarfruitApp()
        disable_console_logging()
        app.run()
    except Exception as e:
        logger.error(f"failed to start: {e}")
        raise
