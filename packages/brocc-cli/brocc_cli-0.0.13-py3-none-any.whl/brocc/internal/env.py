import os


def webview_url() -> str | None:
    return os.environ.get("BROCC_WEBVIEW_URL")


def brocc_api_url() -> str:
    return os.environ.get("BROCC_API_URL", "https://www.brocc.ai/api")


def brocc_api_key() -> str | None:
    return os.environ.get("BROCC_API_KEY")
