import asyncio
import time
from datetime import timedelta
from typing import Annotated, Any, Dict, List, Optional, cast

import lancedb
import pyarrow as pa
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from lancedb.db import LanceDBConnection
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session

from starfruit.db.const import DIMENSIONS, LANCEDB_PATH
from starfruit.db.lance_connection import get_or_create_table
from starfruit.db.lance_schema import ITEM_SCHEMA
from starfruit.db.search import (
    hybrid_search,
)
from starfruit.db.sqlite_manager import sqlite_manager
from starfruit.db.sqlite_models import Item
from starfruit.internal.logger import get_logger
from starfruit.server.models import (
    CommonQueryParams,
    PaginatedResponse,
    PostResponse,
)

logger = get_logger(__name__)


router = APIRouter(
    prefix="/data",
)


class UpsertVectorRequest(BaseModel):
    sqlite_id: int
    text_content: Optional[str] = None
    embedding: Optional[List[float]] = None


OPTIMIZE_COOLDOWN_SECONDS = 60
_last_optimize_time = 0.0
_optimize_lock = asyncio.Lock()


@router.post("/batch_upsert_vector", status_code=202)
async def internal_batch_upsert_vector_req(payload: List[UpsertVectorRequest]):
    """Internal endpoint called by Huey tasks to save batches of vectors to LanceDB.

    Also triggers debounced table optimization.
    """
    if not payload:
        logger.info("Received empty payload for batch upsert.")
        return {"message": "Batch upsert accepted (empty payload)"}

    current_db: Optional[LanceDBConnection] = None
    current_table: Optional[lancedb.table.Table] = None
    try:
        # Establish connection and get table per request
        conn = await asyncio.to_thread(lancedb.connect, LANCEDB_PATH)
        current_db = cast(LanceDBConnection, conn)
        current_table = await asyncio.to_thread(get_or_create_table, current_db)

        if current_table is None:
            raise RuntimeError("Failed to get or create LanceDB table handle for batch upsert.")

        # Prepare data for batch
        data_list = []
        ids_in_batch = [item.sqlite_id for item in payload]
        for item in payload:
            vector = item.embedding if item.embedding is not None else [0.0] * DIMENSIONS
            data_dict = {
                "id": item.sqlite_id,
                "text": item.text_content,
                "vector": vector,
            }
            data_list.append(data_dict)

        arrow_table = pa.Table.from_pylist(data_list, schema=ITEM_SCHEMA)

        # Perform batch upsert
        current_table.merge_insert(
            "id"
        ).when_matched_update_all().when_not_matched_insert_all().execute(arrow_table)

        # --- Trigger Debounced Optimize --- #
        await _maybe_optimize_table(current_table)

        return {"message": f"Batch upsert accepted for {len(payload)} items"}

    except Exception as e:
        table_name_log = current_table.name if current_table else "<unavailable>"
        ids_str = ", ".join(map(str, ids_in_batch[:5])) + ("..." if len(ids_in_batch) > 5 else "")
        logger.error(
            f"Error in internal_batch_upsert_vector for IDs starting with {ids_str} (table: {table_name_log}): {e}",
            exc_info=True,
        )
        # Raise HTTPException so the calling task knows it failed
        raise HTTPException(
            status_code=500, detail=f"Internal LanceDB batch upsert failed for IDs: {ids_str}"
        ) from e


async def _maybe_optimize_table(table: lancedb.table.Table):
    """Checks cooldown and runs optimize in a thread if needed."""
    global _last_optimize_time
    async with _optimize_lock:
        current_time = time.monotonic()
        if current_time - _last_optimize_time >= OPTIMIZE_COOLDOWN_SECONDS:
            optimize_start_time = time.monotonic()
            try:
                # Run blocking optimize in a separate thread
                await asyncio.to_thread(table.optimize, cleanup_older_than=timedelta(days=0))
                optimization_duration = time.monotonic() - optimize_start_time
                logger.info(
                    f"table.optimize for '{table.name}' finished in {optimization_duration:.2f}s."
                )
                _last_optimize_time = time.monotonic()  # Update time only on success
            except Exception as e:
                logger.error(
                    f"Error during table optimization for '{table.name}': {e}", exc_info=True
                )
                # Do not update _last_optimize_time on error
        else:
            # logger.debug(
            #     f"Skipping optimize, last run {current_time - _last_optimize_time:.0f}s ago."
            # )
            pass


@router.get("/list", response_model=PaginatedResponse[PostResponse])
async def list_req(
    common: Annotated[CommonQueryParams, Depends()],
):
    """Lists posts from SQLite (sorted by ingested_at desc)."""

    session: Optional[Session] = None
    page_items: List[Item] = []
    total_count: int = 0

    # 1 & 2: Query metadata DB for total count and page data
    try:
        if not sqlite_manager.initialize_db():
            raise HTTPException(status_code=503, detail="Metadata database unavailable")
        session = sqlite_manager.get_session()
        if not session:
            raise HTTPException(status_code=503, detail="Metadata database session unavailable")

        # Define blocking query functions
        def _get_total_count(s: Session):
            from sqlalchemy import func

            return s.query(func.count(Item.id)).scalar()

        def _get_page_data(s: Session, limit: int, skip: int):
            # Fetch all necessary columns directly from Item
            return s.query(Item).order_by(Item.ingested_at.desc()).limit(limit).offset(skip).all()

        # Run queries in threads
        total_count_task = asyncio.to_thread(_get_total_count, session)
        page_data_task = asyncio.to_thread(_get_page_data, session, common.limit, common.skip)

        # Await results and ensure total_count is an integer
        db_total_count = await total_count_task
        total_count = db_total_count if db_total_count is not None else 0
        page_items = await page_data_task

    except Exception as db_err:
        logger.error(f"/list: Error querying metadata database: {db_err}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error querying metadata database") from db_err
    finally:
        if session:
            session.close()

    # Handle case where no items are returned for the page
    if not page_items:
        return PaginatedResponse(
            items=[],
            total=total_count,
            limit=common.limit,
            offset=common.skip,
        )

    # 6. Convert Item objects to PostResponse models
    validated_items: List[PostResponse] = []
    for item in page_items:
        try:
            # Let Pydantic create the model directly from the ORM object
            # This relies on Config.from_attributes = True in CoreItemModel
            response_item = PostResponse.model_validate(item)
            validated_items.append(response_item)
        except ValidationError as e:
            logger.warning(
                f"Skipping item due to validation error: {e}. Item ID: {getattr(item, 'id', 'N/A')}"
            )
            continue
        except Exception as model_err:
            logger.error(
                f"Unexpected error converting Item to PostResponse for item ID {getattr(item, 'id', 'N/A')}: {model_err}",
                exc_info=True,
            )
            continue

    # 7. Format response
    return PaginatedResponse(
        items=validated_items,
        total=total_count,
        limit=common.limit,
        offset=common.skip,
    )


async def _enrich_lance_results(
    results: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Fetches metadata from SQLite for the given LanceDB result IDs and merges them."""
    if not results:
        return []

    # Extract unique IDs (assuming LanceDB 'id' corresponds to SQLite primary key)
    ids_to_fetch = list({item["id"] for item in results if item.get("id") is not None})

    if not ids_to_fetch:
        logger.warning(
            "_enrich_lance_results_with_metadata: No valid IDs found in LanceDB results."
        )
        return []

    session: Optional[Session] = None
    sqlite_items_map: Dict[int, Item] = {}
    try:
        # Get metadata session (ensure initialized)
        if not sqlite_manager.initialize_db():
            logger.error(
                "_enrich_lance_results_with_metadata: Failed to initialize metadata database."
            )
            return []  # Cannot proceed without DB
        session = sqlite_manager.get_session()
        if not session:
            logger.error(
                "_enrich_lance_results_with_metadata: Failed to get metadata database session."
            )
            return []  # Cannot proceed

        # Define the blocking DB query function
        def _query_sqlite(s: Session, ids: List[int]):
            return s.query(Item).filter(Item.id.in_(ids)).all()

        # Run the query in a thread
        # Ensure IDs are integers for the query
        int_ids_to_fetch = [
            int(id_val)
            for id_val in ids_to_fetch
            if isinstance(id_val, (int, str)) and str(id_val).isdigit()
        ]
        if not int_ids_to_fetch:
            logger.warning(
                "_enrich_lance_results_with_metadata: No integer IDs to fetch after conversion."
            )
            return []

        sqlite_results = await asyncio.to_thread(_query_sqlite, session, int_ids_to_fetch)
        # Ignore linter error on key type
        sqlite_items_map = {item.id: item for item in sqlite_results}  # type: ignore

    except Exception as e:
        logger.error(
            f"_enrich_lance_results_with_metadata: Error querying metadata database: {e}",
            exc_info=True,
        )
        # Depending on desired behavior, could return partial results or empty
        return []  # Return empty on DB error for safety
    finally:
        if session:
            session.close()

    # Merge results
    enriched_results: List[Dict[str, Any]] = []
    for lance_result in results:
        lance_id = lance_result.get("id")
        # Ensure lance_id is int for lookup
        try:
            lookup_id = int(lance_id) if lance_id is not None else None
        except (ValueError, TypeError):
            lookup_id = None

        if lookup_id is None:
            logger.warning(
                f"Skipping enrichment for LanceDB result with invalid/missing ID: {lance_result}"
            )
            continue

        sqlite_item = sqlite_items_map.get(lookup_id)

        if sqlite_item:
            # Convert SQLite Item model to dict, EXCLUDE manual formatting
            merged_data = {
                c.name: getattr(sqlite_item, c.name) for c in sqlite_item.__table__.columns
            }

            # Override/add fields from LanceDB result
            if "text" in lance_result:
                merged_data["text"] = lance_result["text"]
            if "score" in lance_result:
                merged_data["score"] = lance_result["score"]

            # DO NOT pre-format dates here, let Pydantic handle it
            enriched_results.append(merged_data)
        else:
            logger.warning(
                f"_enrich_lance_results_with_metadata: Metadata not found for LanceDB ID {lookup_id}. Lance Result: {lance_result}"
            )
            # Optionally append the unenriched lance_result? Or skip?
            # enriched_results.append(lance_result) # If we want to return partial data

    return enriched_results


@router.get("/search", response_model=PaginatedResponse[PostResponse])
async def search_req(
    request: Request,
    common: Annotated[CommonQueryParams, Depends()],
    query: Annotated[str, Query(...)],
):
    """Performs hybrid search on LanceDB, enriches with SQLite metadata, and returns results."""
    # --- Per-Request Handle Opening --- #
    current_db: Optional[LanceDBConnection] = None
    current_table: Optional[lancedb.table.Table] = None
    try:
        conn = await asyncio.to_thread(lancedb.connect, LANCEDB_PATH)
        current_db = cast(LanceDBConnection, conn)

        # Use the utility function to get/create the table
        current_table = await asyncio.to_thread(get_or_create_table, current_db)

    except RuntimeError as table_err:  # Catch error from get_or_create_table
        logger.error(
            f"/lance/search: Failed to get or create table during request: {table_err}",
            exc_info=True,
        )
        raise HTTPException(status_code=503, detail="LanceDB table unavailable") from table_err
    except Exception as e:
        logger.error(f"/lance/search: Failed to connect to DB during request: {e}", exc_info=True)
        raise HTTPException(status_code=503, detail="LanceDB connection failed") from e
    # If table is still None after check/attempt, something went wrong
    if current_table is None:
        logger.error("/lance/search: LanceDB table is unexpectedly None.")
        raise HTTPException(status_code=503, detail="LanceDB table unavailable")

    try:
        # 2a. Asynchronously embed the query text using Huey task
        from starfruit.tasks.consumer import embed_query_text  # Import the task

        query_result_handle = embed_query_text.schedule(args=(query,), delay=0)

        # 2b. Wait for the embedding result from Huey (with timeout)
        try:
            task_result = await asyncio.wait_for(
                asyncio.to_thread(query_result_handle, blocking=True),
                timeout=30.0,  # Increased timeout slightly -> Increased to 30s
            )
            if not task_result or not task_result[0]:
                raise ValueError("Query embedding task failed or returned empty result.")
            query_vector = task_result[0]
        except asyncio.TimeoutError:
            logger.error(
                f"Timeout waiting for embedding result from Huey task {query_result_handle.id} for query '{query[:20]}...'"
            )
            return PaginatedResponse(
                items=[], total=-1, limit=common.limit, offset=common.skip
            )  # Return empty response
        except Exception as e:
            # Catch potential Huey/task errors during result retrieval
            logger.error(
                f"Error retrieving result from Huey task {query_result_handle.id} for query '{query[:20]}...': {e}",
                exc_info=True,  # Include traceback for debugging
            )
            # Raise HTTPException so frontend knows it failed
            raise HTTPException(status_code=500, detail="Failed to retrieve query embedding") from e

        # 2c. Perform hybrid search using the retrieved vector
        fetch_limit = common.limit + common.skip
        if common.sort_by and common.sort_by not in [
            "score",
            "_relevance_score",
            "_score",
            "_distance",
        ]:
            logger.warning(
                f"Ignoring sort_by='{common.sort_by}' for hybrid search. Results ordered by relevance."
            )

        # Pass the (potentially newly created) table handle to hybrid_search
        # Pass query_vector instead of query_text for embedding part
        search_results_raw = await hybrid_search(
            table=current_table,
            query_text=query,
            query_vector=query_vector,
            limit=fetch_limit,
        )

        # 3. Apply pagination (slicing) in Python
        paginated_lance_items_raw = search_results_raw[common.skip : common.skip + common.limit]

        # 4. Enrich with metadata database
        enriched_items_dict_list = await _enrich_lance_results(paginated_lance_items_raw)

        # 5. Convert enriched results to PostResponse models
        validated_items: List[PostResponse] = []
        for item_dict in enriched_items_dict_list:
            try:
                # Ensure ID is string before validation (as it comes from dict)
                item_dict["id"] = str(item_dict.get("id"))
                # Let Pydantic validate the dictionary containing datetimes
                validated_items.append(PostResponse.model_validate(item_dict))
            except ValidationError as e:
                logger.warning(
                    f"Skipping search result due to validation error: {e}. Item data: {item_dict}"
                )
                continue
            except Exception as model_err:
                logger.error(
                    f"Unexpected error validating PostResponse for search item ID {item_dict.get('id')}: {model_err}",
                    exc_info=True,
                )
                continue

        # 6. Format response
        return PaginatedResponse(
            items=validated_items,
            total=-1,  # Total is typically unknown/expensive for search
            limit=common.limit,
            offset=common.skip,
        )

    except Exception as e:
        logger.error(
            f"Error searching posts from LanceDB table '{current_table.name}': {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail="Error searching LanceDB") from e
