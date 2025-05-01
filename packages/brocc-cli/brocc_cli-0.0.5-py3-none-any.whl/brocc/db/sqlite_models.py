from __future__ import annotations

import datetime
from datetime import timezone
from typing import Optional

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Index,
    Integer,
    Sequence,
    String,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, declarative_base

from brocc.db.normalize_datetime import normalize_datetime_to_utc
from brocc.internal.logger import get_logger
from brocc.parse.types import ParsedContent

Base = declarative_base()
logger = get_logger(__name__)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, Sequence("items_id_seq"), primary_key=True)
    url = Column(String, nullable=False, unique=True)
    source_url = Column(String, nullable=True)
    author_name = Column(String, nullable=True)
    author_url = Column(String, nullable=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    ingested_at = Column(
        DateTime, nullable=False, default=lambda: datetime.datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.datetime.now(timezone.utc),
        onupdate=lambda: datetime.datetime.now(timezone.utc),
    )
    raw_content_hash = Column(String, nullable=False)
    media = Column(JSON, nullable=True)
    metrics = Column(JSON, nullable=True)
    additional_metadata = Column(JSON, nullable=True)
    processed_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index("ix_items_url", "url"),
        Index("ix_items_raw_content_hash", "raw_content_hash"),
    )

    @classmethod
    def check_and_upsert_metadata(
        cls,
        session: Session,
        parsed_content: ParsedContent,
    ) -> Optional[int]:
        """Checks if item exists/needs update, upserts metadata, returns ID if processing should proceed."""
        item_id: Optional[int] = None
        try:
            db_item = session.query(cls).filter(cls.url == parsed_content.url).first()

            created_at_dt = normalize_datetime_to_utc(parsed_content.metadata.created_at)
            now = datetime.datetime.now(timezone.utc)

            if db_item:
                if bool(db_item.raw_content_hash == parsed_content.raw_content_hash):
                    logger.debug(
                        f"Item {db_item.id} ({parsed_content.url}) content hash unchanged. Skipping."
                    )
                    session.commit()
                    return None
                else:
                    logger.debug(
                        f"Item {db_item.id} ({parsed_content.url}) content hash changed. Updating."
                    )
                    db_item.raw_content_hash = parsed_content.raw_content_hash
                    db_item.title = parsed_content.metadata.title
                    db_item.author_name = parsed_content.metadata.author_name
                    db_item.author_url = parsed_content.metadata.author_url
                    db_item.source_url = parsed_content.metadata.source_url
                    db_item.media = parsed_content.metadata.media
                    db_item.metrics = parsed_content.metadata.metrics
                    db_item.additional_metadata = parsed_content.metadata.additional_metadata
                    if created_at_dt:
                        db_item.created_at = created_at_dt
                    db_item.updated_at = now
                    db_item.processed_at = None
                    session.merge(db_item)
                    item_id = db_item.id  # type: ignore[assignment]
            else:
                logger.debug(f"New item ({parsed_content.url}). Creating.")
                new_db_item = cls(
                    url=parsed_content.url,
                    raw_content_hash=parsed_content.raw_content_hash,
                    title=parsed_content.metadata.title,
                    author_name=parsed_content.metadata.author_name,
                    author_url=parsed_content.metadata.author_url,
                    source_url=parsed_content.metadata.source_url,
                    created_at=created_at_dt,
                    media=parsed_content.metadata.media,
                    metrics=parsed_content.metadata.metrics,
                    additional_metadata=parsed_content.metadata.additional_metadata,
                    ingested_at=now,
                    updated_at=now,
                    processed_at=None,
                )
                session.add(new_db_item)
                session.flush()
                item_id = new_db_item.id  # type: ignore[assignment]

            session.commit()
            return item_id

        except SQLAlchemyError as e:
            logger.error(
                f"Database error during check_and_upsert for {parsed_content.url}: {e}",
                exc_info=True,
            )
            session.rollback()
            return None
        except Exception as e:
            logger.error(
                f"Unexpected error during check_and_upsert for {parsed_content.url}: {e}",
                exc_info=True,
            )
            session.rollback()
            return None
