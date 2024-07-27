import os
from contextlib import contextmanager
from enum import Enum as PyEnum
from enum import unique
from typing import Generator

from sqlalchemy import (
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
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

db_url = os.environ.get("DB_URL", "sqlite:///test.db")
if "sqlite" in db_url:
    print("WARNING: Local SQLite DB in use, this may be unfavorable.")

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


class MediaType(PyEnum):
    audio = "audio"
    video = "video"
    image = "image"
    document = "document"


class MediaMetadata(Base):
    __tablename__ = "media_metadata"

    file_id = Column(ForeignKey("files.id"), primary_key=True)
    media_type = Column(Enum(MediaType), nullable=False)

    # text transcript
    transcript = Column(UnicodeText)

    # dimensions
    media_width = Column(Integer)
    media_height = Column(Integer)

    # media metadata
    media_length = Column(Integer)
    media_length_ms = Column(Integer)
