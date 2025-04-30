from typing import Optional

import mlx.nn as nn
from mlx_lm.tokenizer_utils import TokenizerWrapper
from sentence_transformers import SentenceTransformer

# Global for embedding model, loaded by huey startup hook
huey_embed_model: Optional[SentenceTransformer] = None

# Global for language model and tokenizer, loaded by huey startup hook
huey_lm_model: Optional[nn.Module] = None
huey_tokenizer: Optional[TokenizerWrapper] = None

# TODO: mlx
