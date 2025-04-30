import threading
from typing import Optional

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from starfruit.db.sqlite_session import get_sqlite_session
from starfruit.internal.logger import get_logger

logger = get_logger(__name__)


class SqliteManager:
    _instance = None
    _lock = threading.Lock()

    engine: Optional[Engine] = None
    _db_init_lock: threading.Lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SqliteManager, cls).__new__(cls)
                    cls._instance.engine = None
        return cls._instance

    def __init__(self):
        pass

    def initialize_db(self) -> bool:
        """Initializes the database engine if not already initialized."""
        with self._db_init_lock:
            if self.engine:
                return True
            try:
                engine, _ = get_sqlite_session()
                self.engine = engine
                if self.engine is None:
                    logger.error(
                        "SQLite database engine initialization failed (get_sqlite_session returned None engine)."
                    )
                    return False
                return True
            except Exception as e:
                logger.error(f"Failed to initialize metadata database engine: {e}", exc_info=True)
                self.engine = None
                return False

    def get_engine(self) -> Optional[Engine]:
        """Returns the SQLAlchemy engine instance, initializing if needed."""
        if not self.engine:
            logger.warning("Engine accessed before initialization. Attempting to initialize...")
            if not self.initialize_db():
                logger.error("Failed to initialize engine on demand.")
                return None
        return self.engine

    def get_session(self) -> Optional[Session]:
        """Returns a new SQLAlchemy session instance bound to the engine."""
        current_engine = self.get_engine()  # Ensure engine is initialized
        if current_engine:
            return Session(bind=current_engine)
        else:
            logger.error("Cannot create session, engine is not available.")
            return None

    def dispose_engine(self):
        """Disposes the SQLAlchemy engine if it exists."""
        if self.engine:
            try:
                self.engine.dispose()
                logger.debug("SQLite database engine disposed.")
                self.engine = None
            except Exception as e:
                logger.error(f"Error disposing metadata database engine: {e}", exc_info=True)

    def shutdown(self):
        """Gracefully disposes the engine."""
        self.dispose_engine()
        logger.info("SQLite manager shutdown complete.")


# Singleton instance
sqlite_manager = SqliteManager()
