import os


def webview_url() -> str | None:
    return os.environ.get("STARFRUIT_WEBVIEW_URL")


def starfruit_api_url() -> str:
    return os.environ.get("STARFRUIT_API_URL", "https://www.starfruit.sh/api")


def starfruit_api_key() -> str | None:
    return os.environ.get("STARFRUIT_API_KEY")


def openrouter_api_key() -> str | None:
    return os.environ.get("OPENROUTER_API_KEY")
