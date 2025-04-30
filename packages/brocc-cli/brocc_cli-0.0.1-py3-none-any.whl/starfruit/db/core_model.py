from typing import Optional

from pydantic import BaseModel


class CoreItemModel(BaseModel):
    """Core fields shared across different item representations."""

    url: str
    title: Optional[str] = None
    author_name: Optional[str] = None
    author_url: Optional[str] = None
    source_url: Optional[str] = None
    content_hash: Optional[str] = None
    text: Optional[str] = None  # Final text content (summary or original)

    class Config:
        from_attributes = True  # Useful for ORM integration downstream
