"""
Session management for SQLite metadata database.
"""

from pathlib import Path

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session

from starfruit.db.const import SQLITE_DB_PATH  # Corrected import
from starfruit.db.sqlite_models import Base
from starfruit.internal.logger import get_logger

logger = get_logger(__name__)


def get_sqlite_session() -> tuple[
    Engine, Session
]:  # Renamed function, return type is non-optional now
    """Initializes and returns a SQLAlchemy Engine and Session connected to the SQLite DB.

    Enables WAL mode for better concurrency.
    Ensures tables are created.
    """
    database_path = SQLITE_DB_PATH  # Use updated constant
    db_file = Path(database_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    db_url = f"sqlite:///{database_path}"
    try:
        # Create engine (always read-write for SQLite with WAL)
        engine = create_engine(db_url)
        # Enable WAL mode using a separate connection for the PRAGMA
        # This needs to happen *before* other connections/sessions are heavily used
        # to ensure WAL mode is active for them.
        with engine.connect() as connection:
            try:
                connection.execute(text("PRAGMA journal_mode=WAL;"))
                connection.commit()  # Commit PRAGMA
            except Exception as wal_e:
                logger.error(f"Failed to set SQLite journal_mode=WAL: {wal_e}", exc_info=True)
                connection.rollback()
                raise wal_e  # Fail if WAL cannot be set, crucial for concurrency

        # Ensure tables are created using the engine
        Base.metadata.create_all(engine)

    except Exception as e:
        logger.error(f"Failed to initialize SQLite engine or tables: {e}", exc_info=True)
        raise e  # Re-raise initialization errors
    # Create and return the session
    session = Session(bind=engine)
    return engine, session  # Return type is now non-optional
