import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console

from brocc.app import BroccApp
from brocc.internal.logger import disable_console_logging, enable_console_logging, get_logger
from brocc.lifecycle import run_headless

# Go up two levels: src/brocc -> src -> cli
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
    parser = argparse.ArgumentParser(description="Run Brocc App.")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode without launching the webview.",
    )
    args = parser.parse_args()

    # Decide execution path based on headless flag
    if args.headless:
        try:
            # Run headless version (manages its own logging/errors)
            run_headless()
        except SystemExit as e:
            # Logged within run_headless, just exit cleanly
            sys.exit(e.code)
        except Exception as e:
            logger.critical(f"unexpected error during headless startup: {e}", exc_info=True)
            sys.exit(1)
    else:
        # Run TUI version
        try:
            enable_console_logging()
            app = BroccApp()  # No headless arg needed
            disable_console_logging()  # Disable before running app
            app.run()
        except Exception as e:
            logger.error(f"failed to start TUI: {e}", exc_info=True)
            # Re-enable console logging to show the final error if TUI failed
            enable_console_logging()
            console.print_exception(show_locals=True)
            raise  # Or sys.exit(1) if we don't want the full traceback always
