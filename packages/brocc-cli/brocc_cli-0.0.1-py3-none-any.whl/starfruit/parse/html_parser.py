import hashlib
import json
import os
import re
import urllib.parse
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
from typing import List, Literal, Optional

from docling.backend.html_backend import HTMLDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.datamodel.document import InputDocument
from markdownify import markdownify
from pydantic import ValidationError

from starfruit.browser.extract_metadata import extract_metadata
from starfruit.internal.logger import get_logger
from starfruit.parse.base_parser import BaseParser
from starfruit.parse.id_from_url import id_from_url
from starfruit.tasks.task_item import ParseResult, SummaryItem

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

    def _parse_page(self, html: str, url: str) -> List[ParseResult]:
        """
        Parses the HTML using docling for markdown and extract_metadata for details.
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

            # 2. Convert HTML to Markdown using docling (store temporarily)
            raw_markdown_text = ""
            try:
                # docling expects bytes
                html_bytes = html.encode("utf-8")
                # Create a filename placeholder (docling needs one)
                # Sanitize filename based on title or fallback to 'page'
                safe_title = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", metadata_obj.title or "page")
                filename = f"{safe_title[:100]}.html"  # Limit length
                in_doc = InputDocument(
                    path_or_stream=BytesIO(html_bytes),
                    format=InputFormat.HTML,
                    backend=HTMLDocumentBackend,
                    filename=filename,
                )
                # Initialize backend and convert
                backend = HTMLDocumentBackend(in_doc=in_doc, path_or_stream=BytesIO(html_bytes))
                dl_doc = backend.convert()
                raw_markdown_text = dl_doc.export_to_markdown().strip()
            except Exception as e_docling:
                logger.warning(
                    f"docling failed to convert HTML to Markdown for {url}: {e_docling}. Attempting markdownify fallback."
                )
                try:
                    # Default options seem reasonable for a fallback
                    raw_markdown_text = markdownify(html).strip()
                    if raw_markdown_text:
                        logger.info(
                            f"Successfully converted HTML to Markdown using markdownify fallback for {url}"
                        )
                    else:
                        logger.warning(f"markdownify fallback produced empty markdown for {url}")
                except Exception as e_markdownify:
                    logger.error(
                        f"markdownify fallback also failed for {url}: {e_markdownify}",
                        exc_info=True,  # Log traceback for markdownify failure
                    )
                    # Ensure raw_markdown_text remains empty
                    raw_markdown_text = ""
                # Proceeding without markdown text if both failed

            # 3. Prepare additional metadata (favicon, keywords, + IDs)
            additional_meta_dict = {}
            if metadata_obj.favicon:
                # Ensure favicon is string if it's HttpUrl
                additional_meta_dict["favicon"] = str(metadata_obj.favicon)
            additional_metadata_json: Optional[str] = None
            if additional_meta_dict:
                try:
                    additional_metadata_json = json.dumps(additional_meta_dict)
                except TypeError:
                    logger.warning(
                        f"Could not serialize additional metadata for {url}: {additional_meta_dict}",
                        exc_info=True,
                    )

            # 4. Map to POST_SCHEMA structure
            # Ensure created_at is timezone-aware (UTC)
            created_at_dt: Optional[datetime] = None
            if metadata_obj.published_at:
                if metadata_obj.published_at.tzinfo is None:
                    created_at_dt = metadata_obj.published_at.replace(tzinfo=timezone.utc)
                else:
                    created_at_dt = metadata_obj.published_at.astimezone(timezone.utc)

            # Use URL from metadata if available (handles redirects), else use input url
            final_url = str(metadata_obj.url) if metadata_obj.url else url
            # Prepare media (og:image)
            media_list: Optional[List[str]] = None
            if metadata_obj.og_image:
                # Ensure og_image is string if it's HttpUrl
                media_list = [str(metadata_obj.og_image)]

            # Create the SummaryItem or ProcessingItem based on needs_summary
            # This parser always produces items needing summary if markdown exists
            status: Literal["needs_summary", "failed"]
            data: Optional[SummaryItem] = None
            error_msg: Optional[str] = None

            if raw_markdown_text:
                try:
                    # Prepare data dictionary matching SummaryItem fields
                    item_data = {
                        "id": id_from_url(final_url),
                        "url": final_url,
                        "source_url": None,
                        "raw_markdown_text": raw_markdown_text,
                        "author_name": metadata_obj.author,
                        "author_url": None,
                        "title": metadata_obj.title,
                        "created_at": created_at_dt,
                        "media": media_list,
                        "metrics": None,
                        "additional_metadata": json.loads(additional_metadata_json)
                        if additional_metadata_json
                        else None,
                    }
                    data = SummaryItem.model_validate(item_data)
                    status = "needs_summary"
                except (ValidationError, json.JSONDecodeError) as e:
                    status = "failed"
                    error_msg = f"Failed to validate/create SummaryItem: {e}"
                    logger.warning(f"{error_msg} for URL {url}")
            else:
                # No markdown, consider it a failed parse for summary purposes
                status = "failed"
                error_msg = "No markdown content extracted to summarize."
                logger.debug(f"{error_msg} for URL {url}")

            # Return list containing one ParseResult
            return [ParseResult(status=status, data=data, error=error_msg)]

        except Exception as e:
            logger.error(f"Error parsing generic HTML page at {url}: {e}", exc_info=True)
            # Return a failed ParseResult
            return [ParseResult(status="failed", error=str(e))]
