import os
import shutil
from pathlib import Path
from typing import Optional, Tuple

import mlx.nn as nn
from mlx_lm.tokenizer_utils import TokenizerWrapper
from mlx_lm.utils import ModelNotFoundError
from mlx_lm.utils import load as mlx_lm_load
from sentence_transformers import SentenceTransformer

from starfruit.internal.logger import get_logger
from starfruit.tasks.model_const import DEFAULT_LM, NOMIC_EMBED_TEXT_V2

logger = get_logger(__name__)
HF_CACHE_DIR = Path(os.getenv("HF_HOME", Path.home() / ".cache" / "huggingface")) / "hub"


def load_embed_model() -> Optional[SentenceTransformer]:
    model = NOMIC_EMBED_TEXT_V2
    try:
        st_model = SentenceTransformer(model, trust_remote_code=True)
        logger.info(f"SentenceTransformer model '{model}' loaded successfully.")
        return st_model
    except Exception as model_load_e:
        logger.error(
            f"Failed to load SentenceTransformer model '{model}': {model_load_e}",
            exc_info=True,
        )
        return None


def _get_expected_model_path(model_name: str) -> Path:
    """Calculates the expected model directory path in the cache."""
    model_dir_name = f"models--{model_name.replace('/', '--')}"
    return HF_CACHE_DIR / model_dir_name


def clear_model(model_name: str = DEFAULT_LM) -> None:
    """removes the specified model from the hugging face cache."""
    try:
        # allow passing without arg
        cache_dir = Path(os.getenv("HF_HOME", Path.home() / ".cache" / "huggingface")) / "hub"
        # model name format is like "org/model", cache dir is "models--org--model"
        model_dir_name = f"models--{model_name.replace('/', '--')}"
        model_path = cache_dir / model_dir_name

        if model_path.is_dir():
            shutil.rmtree(model_path)
            logger.info(f"removed cache directory for {model_name} at {model_path}")
        else:
            # use info level since this might not strictly be an error if user expects it not to exist
            logger.info(f"cache directory not found or not a directory: {model_path}")

    except OSError as e:
        logger.error(f"failed to remove cache directory for {model_name} at {model_path}: {e}")
    except Exception as e:
        logger.error(f"an unexpected error occurred while clearing cache for {model_name}: {e}")


def has_model(model_name: str = DEFAULT_LM) -> bool:
    """checks if the specified model exists in the hugging face cache."""
    try:
        model_path = _get_expected_model_path(model_name)
        exists = model_path.is_dir()
        logger.debug(
            f"Checking cache for model '{model_name}' at '{model_path}': {'Found' if exists else 'Not found'}"
        )
        return exists
    except Exception as e:
        # if any error occurs during path checking, assume it doesn't exist or isn't accessible
        logger.error(f"Error checking for model cache {model_name}: {e}")
        return False


def load_lm(
    model_name: str = DEFAULT_LM,
    tokenizer_config: dict | None = None,
    lazy: bool = False,
) -> Optional[Tuple[nn.Module, TokenizerWrapper]]:
    """Loads the specified language model and tokenizer from HF Hub (or cache) using mlx-lm.
    mlx-lm will handle downloading from the Hub if the model is not cached.
    """
    if tokenizer_config is None:
        tokenizer_config = {"eos_token": "<|im_end|>"}
    try:
        model, tokenizer = mlx_lm_load(
            model_name,  # Pass the model identifier directly
            tokenizer_config=tokenizer_config,
            lazy=lazy,
        )
        return model, tokenizer
    except (FileNotFoundError, ModelNotFoundError) as e:
        # This could happen if the repo ID is invalid or network fails
        logger.error(
            f"Failed to find or download model '{model_name}': {e}",
            exc_info=True,  # Keep exc_info for these errors
        )
        return None
    except Exception as e:
        logger.error(
            f"An unexpected error occurred loading language model '{model_name}': {e}",
            exc_info=True,
        )
        return None
