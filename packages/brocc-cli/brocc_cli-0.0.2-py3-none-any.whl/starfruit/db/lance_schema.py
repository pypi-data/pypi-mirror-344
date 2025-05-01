import pyarrow as pa

from starfruit.db.const import DIMENSIONS, VECTOR_COLUMN_NAME

ITEM_SCHEMA = pa.schema(
    [
        pa.field("id", pa.int64(), nullable=False),  # SQLite ID
        pa.field("text", pa.string(), nullable=True),  # text (FTS-indexed)
        pa.field(VECTOR_COLUMN_NAME, pa.list_(pa.float32(), DIMENSIONS), nullable=False),
    ]
)
