import os
from contextlib import contextmanager
from enum import Enum as PyEnum
from enum import unique
from typing import Generator

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Unicode,
    UnicodeText,
    create_engine,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Mapped, declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

db_url = os.environ.get("DB_URL", "sqlite:///test.db")
if "sqlite" in db_url:
    print("WARNING: Local SQLite DB in use, this may be unfavorable.")

if "postgres" in db_url:
    JSONType = JSONB
else:
    JSONType = JSON

# sync db
engine = create_engine(
    db_url,
    future=True,
    pool_size=10,
    max_overflow=20,
)
sm = sessionmaker(engine)

# async db
async_engine = create_async_engine(
    db_url.replace(
        "postgresql://",
        "postgresql+asyncpg://",
    ).replace(
        "sqlite://",
        "sqlite+aiosqlite://",
    ),
    future=True,
)
async_sm = sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# actual models!
Base = declarative_base()


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    key = Column(Unicode, nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())

    size = Column(Integer)
    mime = Column(String)

    media_metadata: Mapped["MediaMetadata"] = relationship(
        "MediaMetadata",
        back_populates="file",
    )


class MediaType(PyEnum):
    audio = "audio"
    video = "video"
    image = "image"
    document = "document"


class MediaMetadata(Base):
    __tablename__ = "media_metadata"

    def to_dict(self):
        return {
            "file_id": self.file_id,
            "filename": self.file.key,
            "created": self.file.created_at,
            "mime": self.file.mime,
            "size": self.file.size,
            "media_type": self.media_type,
            "transcript": self.transcript,
            "media_width": self.media_width,
            "media_height": self.media_height,
            "media_length": self.media_length,
            "media_length_ms": self.media_length_ms,
            "metadata": self.meta,
        }

    # primary key + relation
    file_id = Column(ForeignKey("files.id"), primary_key=True)
    file: Mapped["File"] = relationship("File", back_populates="media_metadata")
    media_type = Column(Enum(MediaType), nullable=False)

    # text transcript
    transcript = Column(UnicodeText)

    # dimensions
    media_width = Column(Integer)
    media_height = Column(Integer)

    # media metadata
    media_length = Column(Integer)
    media_length_ms = Column(Integer)

    # extra metadata
    meta = Column(JSONType)
