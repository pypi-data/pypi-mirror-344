import hashlib
import os
import re
import urllib.parse
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import List, Optional

from markdownify import markdownify

from brocc.browser.extract_metadata import extract_metadata
from brocc.internal.logger import get_logger
from brocc.parse.base_parser import BaseParser
from brocc.parse.id_from_url import id_from_url
from brocc.parse.types import ParsedContent, ParsedMetadata
from brocc.tasks.hash_content import hash_content

logger = get_logger(__name__)

DEBUG = True

# --- Constants ---
LLM_INPUT_MAX_CHARS = 100_000  # Max characters of markdown to feed the LLM

# Common non-HTML file extensions we want to explicitly avoid parsing as HTML.
# Focus on types that might be served raw.
# fmt: off
NON_HTML_EXTENSIONS = {
    # Documents (often linked directly)
    ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".rtf",
    # Images (browsers render directly, but not as HTML)
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico",
    # Audio (browsers might play, not HTML)
    ".mp3", ".wav", ".ogg",
    # Video (browsers might play, not HTML)
    ".mp4", ".mov", ".avi", ".webm",
    # Data formats sometimes served raw
    ".json", ".xml", ".csv",
    # Explicitly exclude JS/CSS often linked in pages but not primary content
    ".js", ".css",
}
# fmt: on


class HtmlPageParser(BaseParser):
    """
    Generic parser for standard HTML pages using docling for content extraction and BeautifulSoup/metadata tags for structured data.
    """

    # Match any http or https URL.
    # Specificity is handled by registry order and file extension check in can_parse.
    FALLBACK_URL_PATTERNS: List[str] = [r"https?://.*"]

    def __init__(self):
        super().__init__(url_patterns=self.FALLBACK_URL_PATTERNS)

    def can_parse(self, url: str) -> bool:
        """
        Checks if the URL matches the basic pattern and doesn't have a common non-HTML file extension.
        """
        # First, check if it matches the basic http/https pattern
        if not super().can_parse(url):
            return False

        # Second, check the file extension
        try:
            parsed_url = urllib.parse.urlparse(url)
            # Extract path, ignoring query parameters and fragment
            path = parsed_url.path
            # Check if path ends with a common non-html extension
            # Use os.path.splitext for robustness
            _, extension = os.path.splitext(path)
            if extension and extension.lower() in NON_HTML_EXTENSIONS:
                logger.debug(f"Skipping URL {url} due to non-HTML extension: {extension}")
                return False
        except Exception as e:
            # If URL parsing fails, probably best not to handle it.
            logger.warning(f"Could not parse URL path for extension check: {url} - {e}")
            return False

        # If it passes both checks, it's potentially parsable by this parser.
        return True

    def _parse_page(self, html: str, url: str) -> List[ParsedContent]:
        """
        Parses the HTML using markdownify for markdown and extract_metadata for details.
        Returns a list containing zero or one ParsedContent object.
        """
        # --- Debugging ---
        if url.startswith("https://www.linkedin.com/posts/"):
            try:
                html_hash = hashlib.sha256(html.encode("utf-8")).hexdigest()
                script_dir = Path(__file__).parent
                debug_dir = script_dir.parent.parent.parent / "tests" / "parse" / "html" / "debug"
                logger.debug(f"DEBUG: Attempting to create directory: {debug_dir}")
                debug_dir.mkdir(parents=True, exist_ok=True)
                debug_file_path = debug_dir / f"{html_hash}.html"
                logger.debug(f"DEBUG: Attempting to write to file: {debug_file_path}")
                with open(debug_file_path, "w", encoding="utf-8") as f:
                    f.write(html)
                    logger.debug(f"DEBUG: Successfully wrote to {debug_file_path}")
                logger.debug(f"DEBUG: Completed HTML save for {url} to {debug_file_path}")
            except Exception as e_debug:
                logger.error(f"DEBUG: Failed to save HTML for {url}: {e_debug}", exc_info=True)
        # --- End Debugging ---

        try:
            # 1. Extract structured metadata and additional IDs
            metadata_obj = extract_metadata(html, url)

            # 2. Convert HTML to Markdown using markdownify
            raw_markdown_text = ""
            try:
                raw_markdown_text = markdownify(html).strip()
                if not raw_markdown_text:
                    logger.warning(f"markdownify produced empty markdown for {url}")
            except Exception as e_markdownify:
                logger.error(
                    f"markdownify failed for {url}: {e_markdownify}",
                    exc_info=True,
                )
                # Ensure raw_markdown_text remains empty on failure
                raw_markdown_text = ""

            # Check if markdown content exists before proceeding
            if not raw_markdown_text:
                logger.debug(f"No markdown content extracted for URL {url}. Skipping.")
                return []  # Return empty list if no content

            # --- Create ParsedMetadata --- #
            # Ensure created_at is timezone-aware (UTC)
            created_at_dt: Optional[datetime] = None
            if metadata_obj.published_at:
                if metadata_obj.published_at.tzinfo is None:
                    created_at_dt = metadata_obj.published_at.replace(tzinfo=timezone.utc)
                else:
                    created_at_dt = metadata_obj.published_at.astimezone(timezone.utc)

            media_list: Optional[List[str]] = None
            if metadata_obj.og_image:
                media_list = [str(metadata_obj.og_image)]

            additional_meta_dict = {}
            if metadata_obj.favicon:
                additional_meta_dict["favicon"] = str(metadata_obj.favicon)
            # Add other potential metadata here if needed

            parsed_metadata = ParsedMetadata(
                title=metadata_obj.title,
                author_name=metadata_obj.author,
                author_url=None,  # Html parser doesn't reliably get this
                source_url=None,  # Typically same as url for direct pages
                created_at=created_at_dt,
                media=media_list,
                metrics=None,  # No standard metrics from generic HTML
                additional_metadata=additional_meta_dict if additional_meta_dict else None,
            )
            # --- End ParsedMetadata Creation --- #

            # --- Create ParsedContent --- #
            # Use URL from metadata if available (handles redirects), else use input url
            final_url = str(metadata_obj.url) if metadata_obj.url else url
            content_hash = hash_content(raw_markdown_text)  # Calculate hash of markdown

            if not content_hash:
                logger.error(f"Failed to calculate content hash for {url}. Skipping.")
                return []  # Cannot proceed without hash

            parsed_content_item = ParsedContent(
                id=id_from_url(final_url),
                url=final_url,
                content_to_embed=raw_markdown_text,
                content_to_store=None,  # Needs summary
                metadata=parsed_metadata,
                is_summary_required=True,
                raw_content_hash=content_hash,
            )
            # --- End ParsedContent Creation --- #

            # Return list containing one item
            return [parsed_content_item]

        except Exception as e:
            logger.error(f"Error parsing generic HTML page at {url}: {e}", exc_info=True)
            # Return empty list on error
            return []
