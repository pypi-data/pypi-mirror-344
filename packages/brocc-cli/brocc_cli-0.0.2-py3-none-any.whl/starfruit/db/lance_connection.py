# cli/src/starfruit/db/lance_connection.py
import logging
from typing import Optional

import lancedb

from starfruit.db.const import LANCEDB_PATH, TABLE_NAME
from starfruit.db.lance_schema import ITEM_SCHEMA

logger = logging.getLogger(__name__)


def get_connection() -> Optional[lancedb.DBConnection]:
    """Connects to the LanceDB database at the predefined DB_PATH."""
    try:
        db = lancedb.connect(LANCEDB_PATH)
        logger.debug(f"Successfully connected to LanceDB at {LANCEDB_PATH}")
        return db
    except Exception as e:
        logger.error(f"Failed to connect to LanceDB at {LANCEDB_PATH}: {e}", exc_info=True)
        return None


def get_or_create_table(db: lancedb.DBConnection) -> lancedb.table.Table:
    """Opens the LanceDB table, creating it and its FTS indexes if it doesn't exist.

    Args:
        db: An active LanceDB connection.

    Returns:
        The opened or created LanceDB table handle.

    Raises:
        RuntimeError: If the table cannot be opened or created.
    """
    table_name = TABLE_NAME
    try:
        # Try opening first
        table = db.open_table(table_name)
        # --- Check and create FTS index if missing on existing table --- #
        try:
            indices = table.list_indices()
            fts_index_exists = False
            for idx in indices:
                try:
                    is_fts = idx.index_type == "FTS"
                    has_text_col = "text" in idx.columns
                    if is_fts and has_text_col:
                        fts_index_exists = True
                        break
                except AttributeError as attr_err:
                    logger.warning(
                        f"Attribute error checking index {idx}: {attr_err}", exc_info=True
                    )
                    continue

            if not fts_index_exists:
                try:
                    table.create_fts_index("text", use_tantivy=False, replace=True)
                    logger.info(f"FTS index created on 'text' for existing table '{table_name}'.")
                except Exception as index_create_err:
                    logger.error(
                        f"Failed to create FTS index on 'text' for existing table '{table_name}': {index_create_err}",
                        exc_info=True,
                    )
        except Exception as list_index_err:
            logger.error(
                f"Failed to check indices for existing table '{table_name}': {list_index_err}",
                exc_info=True,
            )
        # --- End FTS Index Check --- #
        return table
    except ValueError as e:
        if "not found" in str(e).lower():
            logger.warning(f"Table '{table_name}' not found. Attempting creation...")
            try:
                table = db.create_table(table_name, schema=ITEM_SCHEMA, exist_ok=True)
                logger.info(f"Table '{table_name}' created successfully.")
                try:
                    logger.info(f"Attempting to create FTS indexes on '{table_name}'...")
                    fts_columns = ["text"]
                    for col in fts_columns:
                        table.create_fts_index(col, use_tantivy=False, replace=True)
                    logger.info(
                        f"Native FTS indexes created/replaced successfully on {fts_columns} for '{table_name}'."
                    )
                except Exception as index_err:
                    logger.error(
                        f"Failed to create one or more FTS indexes on created table '{table_name}': {index_err}",
                        exc_info=True,
                    )
                return table
            except Exception as create_err:
                logger.error(f"Failed to create table '{table_name}': {create_err}", exc_info=True)
                raise RuntimeError(f"Failed to create table '{table_name}'") from create_err
        else:
            logger.error(f"Unexpected ValueError opening table '{table_name}': {e}", exc_info=True)
            raise RuntimeError(f"Unexpected ValueError opening table '{table_name}'") from e
    except Exception as open_err:
        logger.error(f"Failed to open table '{table_name}': {open_err}", exc_info=True)
        raise RuntimeError(f"Failed to open table '{table_name}'") from open_err
