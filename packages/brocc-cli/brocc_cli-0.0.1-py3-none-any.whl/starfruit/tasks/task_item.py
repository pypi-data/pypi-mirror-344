from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel

from starfruit.db.core_model import CoreItemModel


class BaseTaskItem(CoreItemModel):
    """Base model for items stored in staging tables."""

    id: str

    # not defined in CoreItemModel
    created_at: Optional[datetime] = None
    media: Optional[List[str]] = None
    metrics: Optional[Dict[str, Any]] = None
    additional_metadata: Optional[Dict[str, Any]] = None

    # Staging specific
    attempt_count: int = 0


class SummaryItem(BaseTaskItem):
    """Item specifically staged for summarization."""

    raw_markdown_text: str  # Required for summary


class ProcessingItem(BaseTaskItem):
    """Item staged for final processing (embedding, saving)."""

    # This model should contain all fields needed by prepare_storage and save_prepared_data_to_lance
    # Inherits fields like id, url, title, text (summary), author_name, etc. from Base
    def build_embedding_text(self) -> str:
        """Combines title, author, and text content for embedding."""
        title = self.title or ""
        author = self.author_name or ""
        # Use 'text' field (which should be summary if available)
        primary_content = self.text or ""
        embedding_parts = [title.strip(), author.strip(), primary_content.strip()]
        return "\n".join(part for part in embedding_parts if part).strip()


class ParseResult(BaseModel):
    status: Literal["needs_summary", "ready_to_embed", "failed"]
    # Use specific item types. Data is optional only if status is 'failed'.
    data: Optional[Union[SummaryItem, ProcessingItem]] = None
    error: Optional[str] = None
