"""
Engine database connection.
"""
from contextlib import contextmanager
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .settings import (
    ENGINE_DB_URI,
    ENGINE_DB_URI_READ_ONLY,
    ENGINE_POOL_SIZE,
    ENGINE_DB_STATEMENT_TIMEOUT_MILLIS,
    ENGINE_DB_POOL_RECYCLE_SECONDS,
)


def create_local_engine(
    url: Optional[str],
    pool_size: int,
    statement_timeout: int,
    pool_recycle: int,
):
    # Pooling: https://docs.sqlalchemy.org/en/14/core/pooling.html#sqlalchemy.pool.QueuePool
    # Statement timeout: https://stackoverflow.com/a/44936982
    return create_engine(
        url=url,
        pool_size=pool_size,
        pool_recycle=pool_recycle,
        connect_args={"options": f"-c statement_timeout={statement_timeout}"},
    )


engine = create_local_engine(
    url=ENGINE_DB_URI,
    pool_size=ENGINE_POOL_SIZE,
    statement_timeout=ENGINE_DB_STATEMENT_TIMEOUT_MILLIS,
    pool_recycle=ENGINE_DB_POOL_RECYCLE_SECONDS,
)

SessionLocal = sessionmaker(bind=engine)


def yield_db_session() -> Session:
    """
    Yields a database connection (created using environment variables).
    As per FastAPI docs:
    https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


yield_db_session_ctx = contextmanager(yield_db_session)

# Read only connection
RO_engine = create_local_engine(
    url=ENGINE_DB_URI_READ_ONLY,
    pool_size=ENGINE_POOL_SIZE,
    statement_timeout=ENGINE_DB_STATEMENT_TIMEOUT_MILLIS,
    pool_recycle=ENGINE_DB_POOL_RECYCLE_SECONDS,
)

RO_SessionLocal = sessionmaker(bind=RO_engine)


def yield_db_read_only_session() -> Session:
    """
    Yields read only database connection (created using environment variables).
    As per FastAPI docs:
    https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency
    """
    session = RO_SessionLocal()
    try:
        yield session
    finally:
        session.close()


yield_db_read_only_session_ctx = contextmanager(yield_db_read_only_session)
