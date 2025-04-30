import os

from starfruit.internal.get_app_dir import get_app_dir

DIMENSIONS = 256
VECTOR_COLUMN_NAME = "vector"
TABLE_NAME = "posts"
QUERY_PREFIX = "search_query: "
DOCUMENT_PREFIX = "search_document: "
LANCEDB_PATH = os.path.join(get_app_dir(), "lancedb")
SQLITE_DB_PATH = os.path.join(get_app_dir(), "metadata.sqlite")
