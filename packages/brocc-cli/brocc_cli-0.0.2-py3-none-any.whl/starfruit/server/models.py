from datetime import datetime, timezone  # Add timezone
from typing import Any, Generic, List, Optional, TypeVar  # Add Any

from fastapi import HTTPException, status
from pydantic import (
    BaseModel,
    field_validator,
)  # Add field_serializer and field_validator

from starfruit.db.core_model import CoreItemModel  # Add import
from starfruit.internal.logger import get_logger  # Import our logger

logger = get_logger(__name__)  # Initialize logger


class PostResponse(CoreItemModel):
    id: str

    # not defined in CoreItemModel
    created_at: Optional[str] = None
    ingested_at: str
    updated_at: str
    media: Optional[dict | list] = None
    metrics: Optional[dict | list] = None
    additional_metadata: Optional[dict | list] = None

    # search score
    score: Optional[float] = None

    # Use 'before' validators to coerce types from the input source (ORM object)
    @field_validator("id", mode="before")
    @classmethod
    def validate_id_to_str(cls, v: Any) -> str:
        # Handles int from DB or potentially already string
        if isinstance(v, (int, float)):  # Handle potential floats just in case
            return str(int(v))
        return str(v)  # Ensure it's a string

    # Re-add validator with explicit +00:00 for UTC
    @field_validator("created_at", "ingested_at", "updated_at", mode="before")
    @classmethod
    def validate_dt_to_str(cls, v: Any) -> Optional[str]:
        # logger.debug(...) # Removed debug log

        if isinstance(v, datetime):
            # If datetime is naive (tzinfo is None), assume it's UTC and make it aware
            if v.tzinfo is None:
                v = v.replace(tzinfo=timezone.utc)

            # Now format the (guaranteed timezone-aware) datetime
            # isoformat() on aware objects includes the offset
            return v.isoformat(timespec="milliseconds")

        return str(v) if v is not None else None


T = TypeVar("T")


# Generic paginated response structure
class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    limit: int
    offset: int


# Model for query parameters common to list/search
class CommonQueryParams:
    def __init__(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ):
        self.skip = skip
        self.limit = max(1, min(limit, 1000))  # Enforce reasonable limits
        self.sort_by = sort_by
        # Use lower() for case-insensitive check
        normalized_sort_order = sort_order.lower()
        if normalized_sort_order not in ["asc", "desc"]:
            # Use HTTPException for consistency with FastAPI validation
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="sort_order must be 'asc' or 'desc'"
            )
        self.sort_order = normalized_sort_order
