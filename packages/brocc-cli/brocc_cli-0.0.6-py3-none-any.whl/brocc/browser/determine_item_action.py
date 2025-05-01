from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional

from brocc.internal.logger import get_logger

logger = get_logger(__name__)


class ItemAction(Enum):
    UPSERT_TO_DB = auto()
    GENERATE_SUMMARY = auto()
    WAIT = auto()
    ERROR = auto()


# Using dataclass for clarity and potential future expansion
@dataclass(frozen=True)  # Frozen makes instances immutable, good for representing state
class ItemProcessingState:
    url: str
    item_id: int
    is_summary_required: bool
    has_embedding: bool
    has_summary: bool
    content_to_store: Optional[str]
    content_to_embed: str
    embedding: Optional[List[float]]


def determine_item_action(state: ItemProcessingState) -> ItemAction:
    """Determines the next action based on the item's state."""

    summary_needed_but_missing = state.is_summary_required and not state.has_summary

    # Condition 1: Ready for Upsert?
    # Requires embedding AND (summary isn't needed OR summary is present)
    if state.has_embedding and not summary_needed_but_missing:
        # Further checks before declaring UPSERT_TO_DB
        if state.is_summary_required:
            # If summary was required, it must be the content_to_store
            if state.content_to_store is None or not state.has_summary:
                logger.error(
                    f"State inconsistency for {state.url}: Summary required, but content_to_store ({state.content_to_store is None=}) or has_summary ({state.has_summary=}) is invalid."
                )
                return ItemAction.ERROR
        else:
            # If summary wasn't required, original content_to_store must exist
            if state.content_to_store is None:
                logger.error(
                    f"State inconsistency for {state.url}: Summary not required, but content_to_store is None."
                )
                return ItemAction.ERROR

        # Embedding must also exist if has_embedding is True (redundant check, but safe)
        if state.embedding is None:
            logger.error(
                f"State inconsistency for {state.url}: has_embedding is True, but embedding is None."
            )
            return ItemAction.ERROR

        # All checks passed for upsert
        return ItemAction.UPSERT_TO_DB

    # Condition 2: Need to Generate Summary?
    # Requires summary AND summary is missing (checked in summary_needed_but_missing)
    elif summary_needed_but_missing:
        # We need the content to embed to generate the summary
        if not state.content_to_embed:
            logger.error(
                f"State inconsistency for {state.url}: Cannot generate summary because content_to_embed is missing."
            )
            return ItemAction.ERROR
        return ItemAction.GENERATE_SUMMARY

    # Condition 3: Must Wait?
    # Default case if not ready for upsert and summary generation isn't needed/possible yet
    else:
        return ItemAction.WAIT
