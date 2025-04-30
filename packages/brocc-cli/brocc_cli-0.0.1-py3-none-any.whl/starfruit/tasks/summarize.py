import re
import time
from typing import Optional

import mlx.core as mx
from mlx_lm.generate import generate
from mlx_lm.sample_utils import make_sampler
from mlx_lm.tokenizer_utils import TokenizerWrapper

import starfruit.tasks.state as task_state
from starfruit.internal.logger import get_logger
from starfruit.tasks.exceptions import ModelNotReadyError
from starfruit.tasks.model_const import DEFAULT_LM_MAX_TOKENS

logger = get_logger(__name__)

MAX_TOKENS = 1024  # Max *output* tokens for the summary itself
TEMPERATURE = 0.1
# Heuristic: Estimate characters based on max tokens (e.g., ~3 chars/token)
# We also subtract a buffer for the prompt template itself.

SYSTEM_PROMPT = """You are a highly skilled analyst specializing in summarizing content concisely and comprehensively.
For the following content, your task is to:
1.  Identify ALL key details in the content.
2.  Filter out ANY extraneous material and write a concise, coherent summary.
3.  Review your response to ensure it does not include:
  a. UI elements: DO NOT mention images, navigation menus, footers, headers, etc.
  b. Legal text: DO NOT mention cookie policies, legal terms, copyright notices, privacy policies, data policies, etc.
  c. Promotional text: DO NOT mention ads, promotional content, etc.
  d. Code snippets: DO NOT include raw code, instead summarize the code.
4.  Do not feel obligated to pad your response with extra text. The more concise the better.
5.  Respond ONLY with the final condensed summary following these guidelines:
  a. DO NOT begin your response with preamble: "Summary...", "Summary of...", "The content...", "This article...", etc.
  b. DO NOT end your response explaining that it's a summary: "This summary...", "The summary...", etc.
"""
USER_PROMPT_TEMPLATE = """Summarize the following:

```markdown
{}
```"""

# Calculate actual prompt overhead
USER_PROMPT_STRUCTURE_LEN = len(USER_PROMPT_TEMPLATE)
CHAT_TEMPLATE_OVERHEAD = 1000  # over-estimate
PROMPT_BUFFER_CHARS = len(SYSTEM_PROMPT) + USER_PROMPT_STRUCTURE_LEN + CHAT_TEMPLATE_OVERHEAD
CHARS_PER_TOKEN_ESTIMATE = 4  # over-estimate
MAX_MARKDOWN_CHARS = (DEFAULT_LM_MAX_TOKENS * CHARS_PER_TOKEN_ESTIMATE) - PROMPT_BUFFER_CHARS


def summarize(markdown_text: str, source_identifier: Optional[str] = None) -> Optional[str]:
    """Generates a concise summary using the loaded MLX language model."""
    log_ref = f" for {source_identifier}" if source_identifier else ""
    if not task_state.huey_lm_model or not task_state.huey_tokenizer:
        logger.warning(
            f"Language model or tokenizer not loaded. Task will retry. Summary{log_ref}."
        )
        raise ModelNotReadyError("Language model or tokenizer not available.")
    if not markdown_text:
        logger.debug(f"Received empty markdown text{log_ref}. Skipping summary.")
        return None

    original_length = len(markdown_text)
    if original_length > MAX_MARKDOWN_CHARS:
        logger.warning(
            f"Input markdown length ({original_length} chars) exceeds limit ({MAX_MARKDOWN_CHARS}). Truncating input for summary{log_ref}."
        )
        # Truncate by word
        trunc_index = markdown_text.rfind(" ", 0, MAX_MARKDOWN_CHARS)
        if trunc_index == -1:  # If no space found, fallback to hard cutoff (unlikely)
            trunc_index = MAX_MARKDOWN_CHARS
        markdown_text = markdown_text[:trunc_index] + "..."

    model = task_state.huey_lm_model
    tokenizer: TokenizerWrapper = task_state.huey_tokenizer
    formatted_prompt = tokenizer.apply_chat_template(  # type: ignore[attr-defined]
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": USER_PROMPT_TEMPLATE.format(markdown_text),
            },
        ],
        tokenize=False,
        add_generation_prompt=True,
    )
    start_time = time.monotonic()
    try:
        # Ensure model and prompt are on the same device
        mx.eval(model.parameters())  # Ensure model params are loaded if lazy=True was used
        # Create sampler with the desired temperature
        sampler = make_sampler(TEMPERATURE)
        response = generate(
            model=model,
            tokenizer=tokenizer,
            prompt=formatted_prompt,
            max_tokens=MAX_TOKENS,
            sampler=sampler,
            verbose=False,
        )
        duration = time.monotonic() - start_time
        # Strip out any <think> blocks
        response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

        # Filter out potential preamble lines
        if response:
            lines = response.splitlines()
            if lines:
                first_line = lines[0]
                # Match optional markdown around "summary", optional colon, and whitespace
                preamble_pattern = r"^\s*(\*\*|\*|_)?summary(\*\*|\*|_)?[:]?\s*"
                match_result = re.match(preamble_pattern, first_line, re.IGNORECASE)
                logger.debug(
                    f"Checking preamble: first_line='{first_line}', "
                    f"pattern='{preamble_pattern}', match={bool(match_result)}, len={len(first_line)}"
                )
                # Check length *after* stripping potential markdown for a more accurate comparison
                test_line = re.sub(
                    r"(^\s*(\*\*|\*|_)?|(\*\*|\*|_)?[:]?\s*$)", "", first_line
                ).strip()
                if match_result and len(test_line) < 60:
                    logger.debug(f"Removing potential preamble line: '{first_line}'")
                    response = "\n".join(lines[1:]).strip()

            # Filter out potential concluding sentences like "The summary..."
            lines = response.splitlines()  # Re-split in case preamble was removed
            if len(lines) > 1:  # Only check if there's more than one line
                last_line = lines[-1].strip()
                # Match optional markdown at the start, then "the summary"
                concluding_pattern = r"^\s*(\*\*|\*|_)the\s+summary"
                if re.match(concluding_pattern, last_line, re.IGNORECASE):
                    logger.debug(f"Removing potential concluding line: '{lines[-1]}'")
                    response = "\n".join(lines[:-1]).strip()

        return response

    except Exception as e:
        duration = time.monotonic() - start_time
        logger.error(
            f"Failed to generate summary{log_ref} after {duration:.2f}s: {e}",
            exc_info=True,
        )
        return None
