from typing import Any, Dict, List, Union

import lancedb
from lancedb.rerankers import RRFReranker

from starfruit.internal.logger import get_logger

logger = get_logger(__name__)


def dedup_search(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Deduplicates search results based on 'id', keeping the highest score
    and preserving the original relative order.
    Args:
        results: A list of dictionaries, where each dictionary represents a search result
                 and is expected to have an 'id' key and optionally a '_relevance_score' key.
    Returns:
        A list of deduplicated result dictionaries.
    """
    # Ensure IDs are strings for consistent dictionary keying and set storage
    if not results:
        return []

    best_scores: Dict[Union[str, int], float] = {}  # Allow int keys initially
    for result in results:
        result_id = result.get("id")
        # Use negative infinity for comparison if score is missing or not a number
        try:
            score = float(result.get("_relevance_score", -float("inf")))
        except (TypeError, ValueError):
            score = -float("inf")
            logger.warning(
                f"Result ID '{result_id}' has non-numeric score: {result.get('_relevance_score')}"
            )

        if result_id is not None:
            # Store best score, allowing int/str keys temporarily
            current_best = best_scores.get(result_id, -float("inf"))
            best_scores[result_id] = max(current_best, score)
        else:
            logger.warning(f"Found result with missing ID: {result}")

    unique_results: List[Dict[str, Any]] = []
    added_ids: set[Union[str, int]] = set()  # Allow int keys initially
    for result in results:
        result_id = result.get("id")
        if result_id is not None:
            try:
                # Use negative infinity for comparison if score is missing or not a number
                score = float(result.get("_relevance_score", -float("inf")))
            except (TypeError, ValueError):
                score = -float("inf")

            # Check if this ID has the best score recorded and hasn't been added yet
            # We access best_scores using the original id (could be int or str)
            if (
                result_id in best_scores
                and score == best_scores[result_id]
                and result_id not in added_ids
            ):
                # IMPORTANT: Convert id to string ONLY when adding to the final list
                # to match frontend expectations, but keep original type for checks.
                result["id"] = str(result_id)
                unique_results.append(result)
                added_ids.add(result_id)  # Add original id (int or str) to prevent re-adding
    return unique_results


# --- Define Reranker --- #
# If needed, initialize reranker here. Currently commented out.
# cross_encoder_model = "mixedbread-ai/mxbai-rerank-large-v1"
# reranker = CrossEncoderReranker(model_name=cross_encoder_model, device="mps")
# Instantiate RRFReranker by default
default_reranker = RRFReranker(return_score="all")


async def hybrid_search(
    table: lancedb.table.Table,
    query_text: str,
    query_vector: List[float],
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """Performs hybrid search (vector + FTS) on a LanceDB table.

    Args:
        table: The LanceDB table object to search (lancedb.table.Table).
        query_text: The user's search query string (for FTS).
        query_vector: The pre-computed embedding vector for the query_text.
        limit: The maximum number of results to return.

    Returns:
        A list of result dictionaries, ordered by relevance.
    """

    # 2. Perform the search using the computed vector
    try:
        search_query = (
            table.search(query_type="hybrid").vector(query_vector).text(query_text).limit(limit * 2)
        )

        # 3. Rerank (always)
        search_query = search_query.rerank(reranker=default_reranker)
        # Apply final limit *after* reranking
        search_query = search_query.limit(limit)

        # 4. Get results
        results = search_query.to_list()
        # Exclude vector for cleaner logs
    except Exception as search_err:
        logger.error(
            f"Error executing LanceDB search or converting results: {search_err}", exc_info=True
        )
        return []

    # 5. Deduplicate
    unique_results = dedup_search(results)
    return unique_results
