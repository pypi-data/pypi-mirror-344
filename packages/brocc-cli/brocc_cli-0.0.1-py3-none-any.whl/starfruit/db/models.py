from __future__ import annotations

import datetime
from datetime import timezone
from typing import Tuple

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Integer,
    Sequence,
    String,
)
from sqlalchemy.orm import Session, declarative_base

from starfruit.db.normalize_datetime import normalize_datetime_to_utc
from starfruit.internal.logger import get_logger
from starfruit.tasks.task_item import ProcessingItem

Base = declarative_base()
logger = get_logger(__name__)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, Sequence("items_id_seq"), primary_key=True)
    url = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    author_name = Column(String, nullable=True)
    author_url = Column(String, nullable=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    ingested_at = Column(
        DateTime, nullable=True, default=lambda: datetime.datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime,
        nullable=True,
        default=lambda: datetime.datetime.now(timezone.utc),
        onupdate=lambda: datetime.datetime.now(timezone.utc),
    )
    content_hash = Column(String, nullable=True)
    media = Column(JSON, nullable=True)
    metrics = Column(JSON, nullable=True)
    additional_metadata = Column(JSON, nullable=True)  #

    @classmethod
    def create_or_update(
        cls,
        session: Session,
        proc_item: ProcessingItem,
    ) -> Tuple["Item", bool]:
        """Finds or creates an Item, updates if found, returns item and if LanceDB needs update."""

        db_item = session.query(cls).filter(cls.url == proc_item.url).first()

        created_at_dt = normalize_datetime_to_utc(getattr(proc_item, "created_at", None))

        if db_item:
            needs_lance_update = bool(db_item.content_hash != proc_item.content_hash)

            # Update fields
            db_item.source_url = proc_item.source_url
            db_item.author_name = proc_item.author_name
            db_item.author_url = proc_item.author_url
            db_item.title = proc_item.title
            db_item.content_hash = proc_item.content_hash
            db_item.media = proc_item.media
            db_item.metrics = proc_item.metrics
            db_item.additional_metadata = proc_item.additional_metadata
            if created_at_dt:
                db_item.created_at = created_at_dt

            session.merge(db_item)
            session.flush()  # Flush after merge to ensure ID is populated before return
            logger.debug(f"Merged updates for item #{db_item.id}")
            return db_item, needs_lance_update
        else:
            # New item
            needs_lance_update = True
            ingested_at_dt = datetime.datetime.now(timezone.utc)

            new_db_item = cls(
                url=proc_item.url,
                source_url=proc_item.source_url,
                author_name=proc_item.author_name,
                author_url=proc_item.author_url,
                title=proc_item.title,
                created_at=created_at_dt,
                ingested_at=ingested_at_dt,
                content_hash=proc_item.content_hash,
                media=proc_item.media,
                metrics=proc_item.metrics,
                additional_metadata=proc_item.additional_metadata,
            )
            session.add(new_db_item)
            session.flush()
            logger.debug(f"Added new item #{new_db_item.id}")
            return new_db_item, needs_lance_update
