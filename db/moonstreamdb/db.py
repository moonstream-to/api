"""
Moonstream database connection.
"""
from contextlib import contextmanager
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

MOONSTREAM_DB_URI = os.environ.get("MOONSTREAM_DB_URI")
if MOONSTREAM_DB_URI is None:
    raise ValueError("MOONSTREAM_DB_URI environment variable must be set")

MOONSTREAM_POOL_SIZE_RAW = os.environ.get("MOONSTREAM_POOL_SIZE", 0)
try:
    if MOONSTREAM_POOL_SIZE_RAW is not None:
        MOONSTREAM_POOL_SIZE = int(MOONSTREAM_POOL_SIZE_RAW)
except:
    raise Exception(
        f"Could not parse MOONSTREAM_POOL_SIZE as int: {MOONSTREAM_POOL_SIZE_RAW}"
    )

MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIS_RAW = os.environ.get(
    "MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIS"
)
MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIS = 30000
try:
    if MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIS_RAW is not None:
        MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIS = int(
            MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIS_RAW
        )
except:
    raise ValueError(
        f"MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIOS must be an integer: {MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIS_RAW}"
    )

# Pooling: https://docs.sqlalchemy.org/en/14/core/pooling.html#sqlalchemy.pool.QueuePool
# Statement timeout: https://stackoverflow.com/a/44936982
engine = create_engine(
    MOONSTREAM_DB_URI,
    pool_size=MOONSTREAM_POOL_SIZE,
    connect_args={
        "options": f"-c statement_timeout={MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIS}"
    },
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
