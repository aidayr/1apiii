import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy import JSON, String, text
from sqlalchemy.exc import InterfaceError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    type_annotation_map = {
        str: String().with_variant(String(255), "postgresql"),
        dict[str, Any]: JSON,
    }


class Database:
    def __init__(self) -> None:
        self._engine = create_async_engine(settings.postgres_url)
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def init_db(self, max_retries: int = 30, retry_delay: int = 5):
        for attempt in range(max_retries):
            try:
                async with self._engine.connect() as conn:
                    await conn.execute(text("SELECT 1"))
                logger.info("Database connection established")

                async with self._engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
                    logger.info("✅ Database initialized successfully")
                    return
            except (OperationalError, InterfaceError) as e:
                if "Connection refused" in str(e) or "could not connect" in str(e):
                    if attempt == max_retries - 1:
                        logger.error(
                            f"❌ Failed to connect after {max_retries} attempts: {e}"
                        )
                        raise
                    logger.warning(
                        f"⚠️ Attempt {attempt + 1}/{max_retries}: Database not ready. "
                        f"Retrying in {retry_delay}s... Error: {e}"
                    )
                    await asyncio.sleep(retry_delay)
                else:
                    logger.error(f"❌ Database error: {e}")
                    raise
            except Exception as e:
                logger.error(f"❌ Unexpected error during database initialization: {e}")
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"Database session error: {e}")
                raise


database = Database()
