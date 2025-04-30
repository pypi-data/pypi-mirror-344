import json
import threading
import time
from functools import wraps
from typing import Dict, List, Optional, cast

import httpx
from huey import SqliteHuey
from pydantic import ValidationError
from sqlalchemy.orm import Session

import starfruit.tasks.state as task_state
from starfruit.db.const import DOCUMENT_PREFIX, QUERY_PREFIX
from starfruit.db.sqlite_manager import sqlite_manager
from starfruit.db.sqlite_models import Item
from starfruit.internal.const import INTERNAL_API_URL
from starfruit.internal.get_app_dir import get_app_dir
from starfruit.internal.logger import enable_console_logging, get_logger
from starfruit.tasks.embed import embed_texts
from starfruit.tasks.exceptions import ModelNotReadyError
from starfruit.tasks.hash_content import hash_content
from starfruit.tasks.model_loader import load_lm
from starfruit.tasks.notify_frontend import notify_frontend
from starfruit.tasks.summarize import summarize
from starfruit.tasks.task_item import ProcessingItem, SummaryItem

logger = get_logger(__name__)
enable_console_logging()  # must enable in consumer process
task_stats = {}
task_stats_lock = threading.Lock()


def log_task_runtime(retryable_exceptions: tuple):
    """Decorator to log task runtime and handle exceptions intelligently.

    Logs success duration/average.
    Logs errors for non-retryable exceptions.
    Silently re-raises retryable exceptions for Huey to handle.

    Args:
        retryable_exceptions: A tuple of exception types that Huey is expected
                              to retry (matching the task's `retry_on`).
                              Pass an empty tuple `()` if none.
    """
    # Directly use the provided tuple
    if not isinstance(retryable_exceptions, tuple):
        # Add a fallback warning if it's not a tuple, but proceed
        logger.warning("log_task_runtime expects a tuple for retryable_exceptions.")
        # Attempt to use it anyway, or default to empty if problematic
        retry_exceptions_tuple = (
            retryable_exceptions if isinstance(retryable_exceptions, type) else ()
        )
    else:
        retry_exceptions_tuple = retryable_exceptions

    def decorator(task_func):
        @wraps(task_func)
        def wrapper(*args, **kwargs):
            start_time = time.monotonic()
            task_name = task_func.__name__
            try:
                result = task_func(*args, **kwargs)
                end_time = time.monotonic()
                duration = end_time - start_time
                with task_stats_lock:
                    if task_name not in task_stats:
                        task_stats[task_name] = {"total_time": 0.0, "count": 0}
                    task_stats[task_name]["total_time"] += duration
                    task_stats[task_name]["count"] += 1
                    avg_time = task_stats[task_name]["total_time"] / task_stats[task_name]["count"]
                logger.info(f"'{task_name}' succeeded in {duration:.3f}s (avg {avg_time:.3f}s)")
                return result
            except Exception as e:
                # Check if this exception type is in the configured retryable list
                is_retryable_exception = isinstance(e, retry_exceptions_tuple)
                if not is_retryable_exception:
                    # Only log errors for non-retryable exceptions
                    end_time = time.monotonic()
                    duration = end_time - start_time
                    logger.error(
                        f"'{task_name}' failed after {duration:.3f}s with unhandled error: {e}",
                        exc_info=True,
                    )
                # else: If retryable, do nothing here, let Huey handle logging/requeue

                # Always re-raise the exception for huey to handle
                raise

        return wrapper

    return decorator


app_dir = get_app_dir()
huey_db_path = app_dir / "tasks.db"

huey = SqliteHuey(
    filename=str(huey_db_path),
    # Rely on default use_wal=True and timeout=5.0 in SqliteStorage
)


@huey.on_startup()
def startup_load_model():
    """Enqueues tasks to load the language and embedding models when the consumer starts."""
    _load_lm_task.schedule(args=(), delay=0)  # Load LM first
    # _load_embed_task.schedule(args=(), delay=0.5) # Removed embed model pre-loading


@huey.on_shutdown()
def shutdown_cleanup_db():
    """Attempts to delete the Huey task database file on shutdown."""
    if huey_db_path.exists():
        try:
            huey_db_path.unlink()
            logger.info(f"Successfully removed Huey DB file on shutdown: {huey_db_path}")
        except OSError as e:
            logger.error(
                f"Failed to remove Huey DB file {huey_db_path} on shutdown: {e}", exc_info=True
            )
    else:
        logger.info(f"Huey DB file not found on shutdown, skipping removal: {huey_db_path}")


@huey.task(priority=10, retries=3, retry_delay=2)
@log_task_runtime(retryable_exceptions=())
def _load_lm_task():
    """Loads the language model and tokenizer if not already loaded."""
    if task_state.huey_lm_model is None or task_state.huey_tokenizer is None:
        logger.info("Attempting to load language model...")
        try:
            logger.debug("Calling load_lm()...")
            lm_result = load_lm()
            logger.debug(f"load_lm() returned: {'success' if lm_result else 'failure'}")
            if lm_result:
                task_state.huey_lm_model, task_state.huey_tokenizer = lm_result
                logger.info("Language model and tokenizer loaded successfully by task.")
        except Exception as e:
            logger.error(
                f"Unexpected error loading language model: {e}",
                exc_info=True,
            )
            # Raise error to trigger retry for unexpected errors too
            raise ModelNotReadyError(f"Unexpected error during LM load: {e}") from e
    else:
        logger.info("Language model already loaded. Skipping load.")


# @huey.task(priority=9, retries=3, retry_delay=2)
# @log_task_runtime
# def _load_embed_task():
#     """Loads the embedding model if not already loaded."""
#     # This task is removed in favor of lazy loading within embed_texts
#     pass


@huey.task(priority=2, retries=2, retry_delay=8, retry_on=(ModelNotReadyError,))
@log_task_runtime(retryable_exceptions=(ModelNotReadyError,))
def batch_summarize_items(items_json_list: str):
    """NOTE: currently NEVER called with multiple items (this is for single html pages)"""
    # --- Check if LM is loaded --- #
    if task_state.huey_lm_model is None or task_state.huey_tokenizer is None:
        raise ModelNotReadyError("Language model not loaded yet. Task will be retried.")

    # 1. Deserialize items_json_list -> List[SummaryItem]
    try:
        original_items_jsons = json.loads(items_json_list)
        original_items: List[SummaryItem] = [
            SummaryItem.model_validate_json(item_json) for item_json in original_items_jsons
        ]
    except (json.JSONDecodeError, ValidationError, TypeError) as e:
        logger.error(f"Failed to deserialize/validate batch in batch_summarize_items: {e}")
        return  # Cannot proceed if batch is invalid

    if not original_items:
        logger.info("batch_summarize_items received empty list after deserialization.")
        return

    processed_items: List[ProcessingItem] = []
    processed_count = 0
    failed_count = 0

    # 2. Loop and Summarize
    for original_item in original_items:
        if not original_item.raw_markdown_text:
            logger.warning(
                f"Item {original_item.id or original_item.url} lacks 'raw_markdown_text'. Skipping summary."
            )
            failed_count += 1
            continue

        try:
            summary_text = summarize(
                markdown_text=original_item.raw_markdown_text, source_identifier=original_item.url
            )
            processing_data = original_item.model_dump(exclude={"raw_markdown_text"})
            processing_data["text"] = summary_text  # Use summary_text (can be None)
            try:
                processing_item = ProcessingItem.model_validate(processing_data)
                processed_items.append(processing_item)
                processed_count += 1
            except (ValidationError, json.JSONDecodeError) as e_val:
                logger.error(
                    f"Failed to validate/create ProcessingItem for {original_item.id} after summary: {e_val}",
                    exc_info=True,
                )
                failed_count += 1
        except Exception as summary_err:
            logger.error(
                f"Error during summarization for item {original_item.id}: {summary_err}",
                exc_info=True,
            )
            failed_count += 1
            # If summarization fails for one, continue with others

    # 3 & 4: Schedule next batch task if there are results
    if processed_items:
        try:
            processed_items_json = json.dumps([item.model_dump_json() for item in processed_items])
            batch_save_to_sqlite.schedule(args=(processed_items_json,), delay=0.1)
        except Exception as schedule_err:
            logger.error(f"Failed to schedule batch_save_to_sqlite: {schedule_err}", exc_info=True)
    else:
        logger.warning(
            f"No items successfully summarized in batch (original size: {len(original_items)}, failed: {failed_count}). Skipping batch_save_to_sqlite."
        )


@huey.task(priority=5, retries=2, retry_delay=4)
@log_task_runtime(retryable_exceptions=())
def batch_save_to_sqlite(items_json_list: str):
    """Saves a batch of ProcessingItems to SQLite and schedules batch embedding.

    Handles transaction, content hash check, and schedules batch_embed_items.
    """
    # 1. Deserialize items_json_list -> List[ProcessingItem]
    try:
        proc_items_jsons = json.loads(items_json_list)
        proc_items: List[ProcessingItem] = [
            ProcessingItem.model_validate_json(item_json) for item_json in proc_items_jsons
        ]
    except (json.JSONDecodeError, ValidationError, TypeError) as e:
        logger.error(f"Failed to deserialize/validate batch in batch_save_to_sqlite: {e}")
        return  # Cannot proceed if batch is invalid

    if not proc_items:
        logger.info("batch_save_to_sqlite received empty list after deserialization.")
        return

    items_to_embed: List[tuple[int, Optional[str], str]] = []
    saved_ids: List[int] = []
    failed_count = 0
    skipped_duplicates = 0
    session: Optional[Session] = None

    try:
        session = sqlite_manager.get_session()
        if not session:
            logger.error("batch_save_to_sqlite: Failed to get DB session.")
            raise ConnectionError("Failed to get DB session for batch save")

        # --- Step 1: Pre-calculate Hashes and Check for Global Duplicates (Read Only) --- #
        items_to_process_dict: Dict[str, ProcessingItem] = {}
        hashes_to_check = set()
        items_without_hash = []

        for item in proc_items:
            content_hash = hash_content(item.text)
            if content_hash:
                item.content_hash = content_hash
                hashes_to_check.add(content_hash)
                items_to_process_dict[content_hash] = item  # Map hash to item
            else:
                logger.warning(
                    f"Could not calculate content hash for {item.url or item.id}. Will process without dupe check."
                )
                item.content_hash = None
                items_without_hash.append(item)  # Process these separately

        existing_hashes = set()
        if hashes_to_check:
            try:
                query = session.query(Item.content_hash).filter(
                    Item.content_hash.in_(hashes_to_check)
                )
                existing_hashes.update(result[0] for result in query.all() if result[0])
                logger.debug(
                    f"Hash check: Found {len(existing_hashes)} existing hashes out of {len(hashes_to_check)} checked."
                )
            except Exception as hash_check_err:
                logger.error(
                    f"Error checking existing content hashes: {hash_check_err}. Skipping check."
                )
                existing_hashes.clear()  # Don't filter if check fails

        # Prepare final list of items for the write transaction
        items_for_transaction: List[ProcessingItem] = []
        if existing_hashes:
            for content_hash, item in items_to_process_dict.items():
                if content_hash in existing_hashes:
                    skipped_duplicates += 1
                    logger.debug(
                        f"Skipping save (dupe hash): {content_hash[:8]} for {item.url or item.id}."
                    )
                else:
                    items_for_transaction.append(item)
        else:
            # If no existing hashes found or check failed, add all hashable items
            items_for_transaction.extend(items_to_process_dict.values())

        # Add items that couldn't be hashed
        items_for_transaction.extend(items_without_hash)

        # --- Explicitly commit session after read query (hash check) --- #
        try:
            session.commit()  # Commit to end the implicit transaction started by the query
            logger.debug("Committed session after hash check query.")
        except Exception as commit_err:
            # If commit fails here, something is very wrong. Log and potentially abort.
            logger.error(f"Error committing session after hash check: {commit_err}. Aborting task.")
            return  # Abort if we can't clear the transaction state
        # ------------------------------------------------------------------

        if not items_for_transaction:
            logger.info(
                f"All {len(proc_items)} items were duplicates based on content hash. Nothing to save."
            )
            return
        # --- End Duplicate Check --- #

        # --- Step 2: Perform Writes within a Single Transaction --- #
        try:
            with session.begin():  # Start the main transaction here
                for proc_item in items_for_transaction:
                    try:
                        # Hash already calculated and added above
                        db_item, needs_lance_update = Item.create_or_update(session, proc_item)
                        sqlite_id = db_item.id
                        if sqlite_id is None:
                            raise ValueError(
                                f"Failed to obtain sqlite_id for {proc_item.url or proc_item.id}"
                            )

                        saved_ids.append(cast(int, sqlite_id))

                        if needs_lance_update:
                            text_for_embedding = proc_item.build_embedding_text()
                            items_to_embed.append(
                                (cast(int, sqlite_id), proc_item.text, text_for_embedding)
                            )
                    except Exception as item_save_err:
                        failed_count += 1
                        logger.error(
                            f"Error saving item {proc_item.url or proc_item.id} within batch transaction: {item_save_err}",
                            exc_info=True,
                        )
                        # Let the outer exception handler catch this if we want rollback
                        # Or potentially add specific handling here if we want partial commits (more complex)
                        # For now, assume any error within the loop should potentially roll back the whole batch
                        raise  # Re-raise to trigger rollback by session.begin() context manager

            # If loop completes without error, transaction is committed here
            logger.info(
                f"Successfully saved/updated {len(saved_ids)} items to SQLite (skipped: {skipped_duplicates}, transaction failed items: {failed_count})."
            )

        except (
            Exception
        ) as transaction_err:  # Catch errors leaking from session.begin() or re-raised inner errors
            failed_count = len(items_for_transaction)  # Mark all items in transaction as failed
            logger.error(
                f"Batch save transaction failed (rolled back): {transaction_err}", exc_info=True
            )
            # Clear potentially partially populated lists from the failed transaction attempt
            saved_ids.clear()
            items_to_embed.clear()
            # Don't proceed to notify/schedule embed if transaction failed
            return
        # --- End Transaction --- #

        # --- Step 3: Notify Frontend and Schedule Next Task (only if transaction succeeded) --- #
        if saved_ids:
            notify_frontend("batch_save_to_sqlite", len(saved_ids))

        if items_to_embed:
            try:
                items_data_json = json.dumps(items_to_embed)
                batch_embed_items.schedule(args=(items_data_json,), delay=0.1)
            except Exception as schedule_err:
                logger.error(f"Failed to schedule batch_embed_items: {schedule_err}", exc_info=True)
        elif saved_ids:  # Log only if we saved something but didn't need embedding
            logger.info("No items needed embedding from this batch.")

    except Exception as e:
        # Catch outer errors like DB connection
        logger.error(f"Outer error during batch_save_to_sqlite: {e}", exc_info=True)
        # Let Huey handle retry based on task config
        raise
    finally:
        if session:
            session.close()


@huey.task(priority=7, retries=2, retry_delay=4)
@log_task_runtime(retryable_exceptions=())
def batch_embed_items(items_data_json: str):
    """Embeds a batch of texts and upserts them via the internal API.

    Calls embed_texts (which handles lazy loading) and the new batch upsert endpoint.
    """
    # 1. Deserialize items_data_json -> List[Tuple[int, str | None, str]] (id, content, embed_text)
    try:
        items_data: List[tuple[int, Optional[str], str]] = json.loads(items_data_json)
    except (json.JSONDecodeError, TypeError) as e:
        logger.error(f"Failed to deserialize batch data in batch_embed_items: {e}")
        return  # Cannot proceed

    if not items_data:
        logger.info("batch_embed_items received empty list after deserialization.")
        return

    # 2. Extract list of embed_text
    texts_to_embed = [item[2] for item in items_data]
    if not texts_to_embed:
        logger.warning("No texts found to embed in the batch data.")
        return

    # 3. Call embed_texts()
    embeddings_result = embed_texts(texts_to_embed, DOCUMENT_PREFIX)

    if embeddings_result is None or len(embeddings_result) != len(items_data):
        logger.error(
            f"Embedding failed or returned unexpected number of results. Expected {len(items_data)}, got {len(embeddings_result) if embeddings_result else 0}."
        )
        # Decide how to handle partial failure? For now, fail the batch.
        # Re-raising might trigger retry depending on Huey config
        raise RuntimeError("Embedding failed for batch")

    # 4. Combine (id, content, embedding) into list of dicts/objects for API
    upsert_payload = []
    for i, item_tuple in enumerate(items_data):
        sqlite_id = item_tuple[0]
        text_content = item_tuple[1]
        embedding = embeddings_result[i]
        upsert_payload.append(
            {"sqlite_id": sqlite_id, "text_content": text_content, "embedding": embedding}
        )

    # 5. Call new internal API /data/batch_upsert_vector
    if upsert_payload:
        upsert_url = f"{INTERNAL_API_URL}/data/batch_upsert_vector"
        try:
            # Use a synchronous HTTP client within the sync Huey task
            with httpx.Client() as client:
                response = client.post(
                    upsert_url, json=upsert_payload, timeout=60.0
                )  # Increased timeout for batch
                response.raise_for_status()  # Raise exception for 4xx/5xx responses
        except httpx.RequestError as req_err:
            logger.error(
                f"batch_embed_items: HTTP request error calling internal batch upsert API: {req_err}",
                exc_info=False,
            )
            # Re-raise to potentially trigger Huey retry
            raise
        except httpx.HTTPStatusError as status_err:
            logger.error(
                f"batch_embed_items: HTTP status error from internal batch upsert API: {status_err.response.status_code} - {status_err.response.text[:200]}",
                exc_info=False,
            )
            # Re-raise to potentially trigger Huey retry
            raise
        except Exception as api_err:
            logger.error(
                f"batch_embed_items: Unexpected error calling internal batch upsert API: {api_err}",
                exc_info=True,
            )
            # Re-raise to potentially trigger Huey retry
            raise
    else:
        logger.info("No items to upsert after embedding batch.")


@huey.task(priority=10, retries=2, retry_delay=4)
@log_task_runtime(retryable_exceptions=())
def embed_query_text(text: str) -> Optional[List[List[float]]]:
    """Embeds search queries."""
    # Model loading handled by embed_texts
    # Call embed_texts (which uses task_state.huey_embed_model by default)
    result = embed_texts([text], QUERY_PREFIX)
    return result
