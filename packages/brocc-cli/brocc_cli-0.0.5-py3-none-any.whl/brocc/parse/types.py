import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# Define a structure similar to CoreItemModel fields needed by parsers/TabMonitor
class ParsedMetadata(BaseModel):
    title: Optional[str] = None
    author_name: Optional[str] = None
    author_url: Optional[str] = None  # If available from parser
    source_url: Optional[str] = None  # If different from main URL (e.g., feed page)
    created_at: Optional[datetime.datetime] = None
    media: Optional[List[str]] = None  # Simplified media representation
    metrics: Optional[Dict[str, Any]] = None
    additional_metadata: Optional[Dict[str, Any]] = None


class ParsedContent(BaseModel):
    id: str = Field(..., description="Consistent ID derived from URL")
    url: str
    content_to_embed: str
    content_to_store: Optional[str] = Field(
        description="Text to store in LanceDB (summary or original)"
    )
    metadata: ParsedMetadata
    is_summary_required: bool
    raw_content_hash: str = Field(..., description="Hash of content_to_embed")
