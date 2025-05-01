from typing import NamedTuple, Optional


class TabReference(NamedTuple):
    """Minimal reference to identify a tab and its relevant state."""

    id: str
    url: str
    html: Optional[str] = None
    title: Optional[str] = None
    ws_url: Optional[str] = None
