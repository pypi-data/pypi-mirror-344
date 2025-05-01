import datetime
import threading
import time
from functools import wraps
from typing import List, Optional, Tuple

import httpx
from huey import SqliteHuey
from mlx_lm.generate import generate
from mlx_lm.models.cache import make_prompt_cache
from mlx_lm.sample_utils import make_sampler
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import brocc.tasks.state as task_state
from brocc.db.const import DOCUMENT_PREFIX, QUERY_PREFIX
from brocc.db.sqlite_manager import sqlite_manager
from brocc.db.sqlite_models import Item
from brocc.internal.const import INTERNAL_API_URL
from brocc.internal.get_app_dir import get_app_dir
from brocc.internal.logger import enable_console_logging, get_logger
from brocc.tasks.embed import embed_texts
from brocc.tasks.exceptions import ModelNotReadyError
from brocc.tasks.model_loader import load_lm
from brocc.tasks.notify_frontend import notify_frontend
from brocc.tasks.summarize import SYSTEM_PROMPT, summarize

logger = get_logger(__name__)
enable_console_logging()  # must enable in consumer process
task_stats = {}
task_stats_lock = threading.Lock()


def _notify_tab_monitor(endpoint_path: str, payload: dict, context_log_msg: str) -> bool:
    """
    Args:
        endpoint_path: The specific API path (e.g., '/chrome/monitoring/summary_result').
        payload: The JSON data to send.
        context_log_msg: A descriptive string for logging (e.g., 'summary for item 123').
    """
    callback_url = f"{INTERNAL_API_URL}{endpoint_path}"
    try:
        with httpx.Client() as client:
            response = client.post(callback_url, json=payload, timeout=10.0)
            response.raise_for_status()
        logger.debug(f"Successfully sent TabMonitor callback for {context_log_msg}.")
        return True
    except httpx.RequestError as req_err:
        logger.error(
            f"Failed callback ({req_err.__class__.__name__}) to TabMonitor for {context_log_msg}: {req_err}"
        )
        return False
    except httpx.HTTPStatusError as status_err:
        logger.error(
            f"Failed callback (HTTP {status_err.response.status_code}) to TabMonitor for {context_log_msg}: {status_err.response.text[:200]}"
        )
        # Consider if this should re-raise or just return False. Returning False for now.
        return False
    except Exception as e:
        logger.error(
            f"Unexpected error during callback for {context_log_msg}: {e}",
            exc_info=True,
        )
        return False


def log_task_runtime(retryable_exceptions: tuple):
    """Decorator to log task runtime and handle exceptions intelligently."""
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
        logger.info("Loading LM...")
        try:
            load_start_time = time.monotonic()
            lm_result = load_lm()
            load_duration = time.monotonic() - load_start_time
            if lm_result:
                task_state.huey_lm_model, task_state.huey_tokenizer = lm_result
                logger.info(f"LM loaded successfully in {load_duration:.3f}s.")
                if task_state.huey_lm_model and task_state.huey_tokenizer:
                    logger.info("Generating prompt cache...")
                    cache_start_time = time.monotonic()
                    try:
                        system_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                        tokenizer = task_state.huey_tokenizer
                        system_prompt_formatted = tokenizer.apply_chat_template(  # type: ignore[attr-defined]
                            system_messages, tokenize=False, add_generation_prompt=True
                        )
                        model = task_state.huey_lm_model
                        initial_cache = make_prompt_cache(model)
                        cache_sampler = make_sampler(temp=0.0)
                        _ = generate(
                            model=model,
                            tokenizer=tokenizer,
                            prompt=system_prompt_formatted,
                            max_tokens=1,  # Minimal generation
                            prompt_cache=initial_cache,
                            sampler=cache_sampler,
                        )
                        task_state.huey_prompt_cache = initial_cache
                        cache_duration = time.monotonic() - cache_start_time
                        logger.info(f"Prompt cache generated in {cache_duration:.3f}s.")
                    except Exception as cache_err:
                        cache_duration = time.monotonic() - cache_start_time
                        logger.error(
                            f"Failed to pre-populate prompt cache after {cache_duration:.3f}s: {cache_err}",
                            exc_info=True,
                        )
                        task_state.huey_prompt_cache = None  # Ensure it's None on failure
                else:
                    logger.warning("Model or tokenizer became unavailable before cache population.")
            else:  # lm_result was False
                logger.warning(f"load_lm() failed after {load_duration:.3f}s.")

        except Exception as e:
            logger.error(
                f"Unexpected error loading language model: {e}",
                exc_info=True,
            )
            # Raise error to trigger retry for unexpected errors too
            raise ModelNotReadyError(f"Unexpected error during LM load: {e}") from e
    else:
        logger.info("Language model already loaded. Skipping load.")


@huey.task(priority=7, retries=2, retry_delay=4)
@log_task_runtime(retryable_exceptions=())
def batch_embed_raw_text(batch_data: List[Tuple[int, str, str]]):
    """Embeds raw text for a batch of items and calls back to TabMonitor API."""
    if not batch_data:
        logger.info("batch_embed_raw_text received empty batch.")
        return

    logger.info(f"Embedding batch of {len(batch_data)} items.")
    item_ids = [item[0] for item in batch_data]
    texts_to_embed = [item[2] for item in batch_data]

    # Call embed_texts (handles lazy loading of embed model)
    embeddings_result = embed_texts(texts_to_embed, DOCUMENT_PREFIX)

    if embeddings_result is None or len(embeddings_result) != len(batch_data):
        logger.error(
            f"Embedding failed or returned unexpected number of results for batch starting with item ID {item_ids[0]}. Expected {len(batch_data)}, got {len(embeddings_result) if embeddings_result else 'None'}."
        )
        # Consider how to notify failure? Maybe callback with error? For now, log and drop.
        return

    # Call back to TabMonitor API for each successful embedding
    success_count = 0
    fail_count = 0
    for i, item_tuple in enumerate(batch_data):
        item_id, url, _ = item_tuple
        embedding = embeddings_result[i]
        payload = {"item_id": item_id, "url": url, "embedding": embedding}
        log_context = f"embedding result for item {item_id}"
        if _notify_tab_monitor("/chrome/monitoring/embedding_result", payload, log_context):
            success_count += 1
        else:
            fail_count += 1
            # Continue processing other items in the batch even if one callback fails

    logger.info(
        f"Embedding batch processed. Callbacks: {success_count} succeeded, {fail_count} failed."
    )


@huey.task(priority=5, retries=2, retry_delay=8, retry_on=(ModelNotReadyError,))
@log_task_runtime(retryable_exceptions=(ModelNotReadyError,))
def generate_summary_and_notify(item_id: int, url: str, content_to_embed: str):
    """Generates summary for a single item and calls back to TabMonitor API."""
    if task_state.huey_lm_model is None or task_state.huey_tokenizer is None:
        raise ModelNotReadyError(
            "Language model not loaded yet for summarization. Task will be retried."
        )

    logger.info(f"Generating summary for item {item_id} ({url}).")
    try:
        summary_text = summarize(
            markdown_text=content_to_embed,
            source_identifier=url,
            # Uses models/cache from task_state internally
        )
        if summary_text is None:
            # Summarization might return None on failure/empty content
            raise ValueError("Summarization returned None")

        logger.info(
            f"Summary generated successfully for item {item_id} ({url}). Length: {len(summary_text)}"
        )

        # Call back to TabMonitor API using the helper
        payload = {"item_id": item_id, "url": url, "summary_text": summary_text}
        log_context = f"summary result for item {item_id} ({url})"
        if not _notify_tab_monitor("/chrome/monitoring/summary_result", payload, log_context):
            # If the callback fails, log it but don't fail the task.
            # Losing the notification is not ideal, but avoids re-summarizing on retry.
            logger.warning(
                f"TabMonitor notification failed for {log_context}. Summary was generated but monitor wasn't notified immediately."
            )

    except ModelNotReadyError as mnre:
        logger.warning(f"generate_summary_and_notify: {mnre}. Task will retry.")
        raise  # Re-raise specifically for Huey retry logic
    except Exception as e:
        logger.error(
            f"Error during summarization or callback for item {item_id} ({url}): {e}", exc_info=True
        )
        # Re-raise general errors to potentially trigger Huey retry
        raise


@huey.task(priority=9, retries=3, retry_delay=5)
@log_task_runtime(retryable_exceptions=())
def upsert_to_db(item_id: int, text_content: str, embedding: List[float]):
    """Upserts the final data (summary + embedding) to LanceDB via internal API and updates DB."""
    logger.info(f"Upserting item {item_id} to LanceDB via batch endpoint.")
    upsert_url = f"{INTERNAL_API_URL}/data/batch_upsert_vector"
    payload = [{"sqlite_id": item_id, "text_content": text_content, "embedding": embedding}]
    processed_successfully = False
    try:
        with httpx.Client() as client:
            response = client.post(upsert_url, json=payload, timeout=60.0)
            response.raise_for_status()
        logger.info(f"Successfully upserted item {item_id} via internal API.")
        processed_successfully = True
    except httpx.RequestError as req_err:
        logger.error(
            f"upsert_to_lancedb: HTTP request error calling internal API for item {item_id}: {req_err}"
        )
        raise  # Re-raise to trigger Huey retry
    except httpx.HTTPStatusError as status_err:
        logger.error(
            f"upsert_to_lancedb: HTTP status error {status_err.response.status_code} from internal API for item {item_id}: {status_err.response.text[:200]}"
        )
        # Decide if this is retryable? 4xx probably not, 5xx maybe.
        # For now, let's retry on status errors too.
        raise
    except Exception as api_err:
        logger.error(
            f"upsert_to_lancedb: Unexpected error calling internal API for item {item_id}: {api_err}",
            exc_info=True,
        )
        raise  # Re-raise to trigger Huey retry

    # Update SQLite only if API call was successful
    if processed_successfully:
        session: Optional[Session] = None
        try:
            session = sqlite_manager.get_session()
            if not session:
                logger.error(f"Failed to get DB session to update processed_at for item {item_id}")
                return  # Cannot update status

            db_item = session.query(Item).filter(Item.id == item_id).first()
            if db_item:
                db_item.processed_at = datetime.datetime.now(datetime.timezone.utc)  # type: ignore[assignment]
                session.commit()
                logger.info(f"Updated processed_at timestamp for item {item_id}.")
                # Notify frontend about successful processing
                notify_frontend("item_processed", item_id)
            else:
                logger.warning(f"Could not find item {item_id} in DB to update processed_at.")

        except SQLAlchemyError as db_err:
            logger.error(
                f"Database error updating processed_at for item {item_id}: {db_err}", exc_info=True
            )
            if session:
                session.rollback()
        except Exception as e:
            logger.error(
                f"Unexpected error updating processed_at for item {item_id}: {e}", exc_info=True
            )
            if session:
                session.rollback()
        finally:
            if session:
                session.close()


@huey.task(priority=10, retries=2, retry_delay=4)
@log_task_runtime(retryable_exceptions=())
def embed_query_text(text: str) -> Optional[List[List[float]]]:
    """Embeds search queries."""
    # Model loading handled by embed_texts
    logger.debug(f"Embedding query text (length: {len(text)})...")
    result = embed_texts([text], QUERY_PREFIX)
    logger.debug(f"Query embedding done. Result shape: {len(result) if result else 0} vectors.")
    return result
