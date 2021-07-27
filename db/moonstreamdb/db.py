"""
Exploration database connection.
"""
from contextlib import contextmanager
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

EXPLORATION_DB_URI = os.environ.get("EXPLORATION_DB_URI")
if EXPLORATION_DB_URI is None:
    raise ValueError("EXPLORATION_DB_URI environment variable must be set")
EXPLORATION_POOL_SIZE_RAW = os.environ.get("EXPLORATION_POOL_SIZE", 0)
try:
    if EXPLORATION_POOL_SIZE_RAW is not None:
        EXPLORATION_POOL_SIZE = int(EXPLORATION_POOL_SIZE_RAW)
except:
    raise Exception(
        f"Could not parse EXPLORATION_POOL_SIZE as int: {EXPLORATION_POOL_SIZE_RAW}"
    )

# https://docs.sqlalchemy.org/en/14/core/pooling.html#sqlalchemy.pool.QueuePool
engine = create_engine(EXPLORATION_DB_URI, pool_size=EXPLORATION_POOL_SIZE)
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
