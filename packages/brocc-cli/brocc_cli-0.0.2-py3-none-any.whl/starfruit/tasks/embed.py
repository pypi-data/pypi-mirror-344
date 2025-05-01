import time
from typing import List, Optional

import mlx.core as mx
import numpy as np
from sentence_transformers import SentenceTransformer

import starfruit.tasks.state as task_state
from starfruit.db.const import DIMENSIONS
from starfruit.internal.logger import get_logger
from starfruit.tasks.model_loader import load_embed_model

logger = get_logger(__name__)


def embed_texts(
    texts: List[str],
    prefix: str,
    model: Optional[SentenceTransformer] = None,
) -> Optional[List[List[float]]]:
    """Embeds a list of texts using the SentenceTransformer model.

    Loads the model on first use if not already loaded in task_state.

    Args:
        texts: The list of strings to embed.
        prefix: The prefix to prepend to each text (e.g., 'query:', 'passage:').
        model: An optional pre-loaded SentenceTransformer model instance.
               If provided, it overrides the lazy loading logic.

    Returns:
        A list of embeddings (each as a list of floats), or None if embedding fails.
    """
    if not texts:
        logger.debug("Received empty text list.")
        return []  # Return empty list for empty input

    task_start_time = time.monotonic()
    try:
        # Determine which model to use
        model_to_use = model

        if model_to_use is None:
            # Check task state
            if task_state.huey_embed_model is None:
                logger.info("Embedding model not loaded in task state. Attempting lazy load...")
                # --- Lazy Load --- #
                try:
                    loaded_model = load_embed_model()
                    if loaded_model:
                        task_state.huey_embed_model = loaded_model
                        model_to_use = task_state.huey_embed_model
                        logger.info("Successfully lazy-loaded embedding model.")
                    else:
                        logger.error("Lazy load failed: load_embed_model() returned None.")
                        return None  # Indicate failure
                except Exception as load_err:
                    logger.error(
                        f"Exception during lazy load of embedding model: {load_err}", exc_info=True
                    )
                    return None  # Indicate failure
            else:
                # Use already loaded model from state
                model_to_use = task_state.huey_embed_model

        # If after all checks, model_to_use is still None, we cannot proceed.
        if model_to_use is None:
            logger.error(
                "Could not obtain embedding model (lazy load failed or state inconsistent). Failing task."
            )
            return None

        # --- Proceed with embedding --- #
        prefixed_texts = [f"{prefix}{text}" for text in texts]
        embeddings = model_to_use.encode(prefixed_texts, normalize_embeddings=True)

        if isinstance(embeddings, (np.ndarray, mx.array)):
            embeddings_list = embeddings.tolist()
        else:
            embeddings_list = embeddings
        # Truncate embeddings to the expected dimension
        truncated_embeddings = [embedding[:DIMENSIONS] for embedding in embeddings_list]

        duration = time.monotonic() - task_start_time
        logger.debug(
            f"Embedding successful for {len(truncated_embeddings)} items in {duration:.2f}s (incl. load if first run)."
        )
        return truncated_embeddings

    except Exception as e:
        logger.error(f"Failed to embed text batch: {e}", exc_info=True)
        return None
