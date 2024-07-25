import os
from contextlib import contextmanager
from enum import Enum as PyEnum
from enum import unique
from typing import Generator

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

db_url = os.environ.get("DB_URL", "sqlite:///test.db")
if "sqlite" in db_url:
    print("WARNING: Local SQLite DB in use, this may be unfavorable.")

engine = create_engine(db_url, future=True, pool_size=10, max_overflow=20)
sm = sessionmaker(engine)

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
async_sm = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
