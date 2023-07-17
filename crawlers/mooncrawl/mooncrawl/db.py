from contextlib import contextmanager
from typing import Generator

from moonstreamdb.db import (
    MOONSTREAM_DB_URI,
    MOONSTREAM_DB_URI_READ_ONLY,
    MOONSTREAM_POOL_SIZE,
    create_moonstream_engine,
)
from sqlalchemy.orm import Session, sessionmaker

from .settings import (
    MOONSTREAM_CRAWLERS_DB_STATEMENT_TIMEOUT_MILLIS,
    MOONSTREAM_QUERY_API_DB_STATEMENT_TIMEOUT_MILLIS,
)

engine = create_moonstream_engine(
    url=MOONSTREAM_DB_URI,
    pool_size=MOONSTREAM_POOL_SIZE,
    statement_timeout=MOONSTREAM_CRAWLERS_DB_STATEMENT_TIMEOUT_MILLIS,
)
SessionLocal = sessionmaker(bind=engine)


def yield_db_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


yield_db_session_ctx = contextmanager(yield_db_session)

# pre-ping
pre_ping_engine = create_moonstream_engine(
    url=MOONSTREAM_DB_URI,
    pool_size=MOONSTREAM_POOL_SIZE,
    statement_timeout=MOONSTREAM_CRAWLERS_DB_STATEMENT_TIMEOUT_MILLIS,
    pool_pre_ping=True,
)
PrePing_SessionLocal = sessionmaker(bind=pre_ping_engine)


def yield_db_preping_session() -> Generator[Session, None, None]:
    session = PrePing_SessionLocal()
    try:
        yield session
    finally:
        session.close()


yield_db_preping_session_ctx = contextmanager(yield_db_preping_session)


# Read only
RO_engine = create_moonstream_engine(
    url=MOONSTREAM_DB_URI_READ_ONLY,
    pool_size=MOONSTREAM_POOL_SIZE,
    statement_timeout=MOONSTREAM_CRAWLERS_DB_STATEMENT_TIMEOUT_MILLIS,
)
RO_SessionLocal = sessionmaker(bind=RO_engine)


def yield_db_read_only_session() -> Generator[Session, None, None]:
    session = RO_SessionLocal()
    try:
        yield session
    finally:
        session.close()


yield_db_read_only_session_ctx = contextmanager(yield_db_read_only_session)

# Read only pre-ping
RO_pre_ping_engine = create_moonstream_engine(
    url=MOONSTREAM_DB_URI_READ_ONLY,
    pool_size=MOONSTREAM_POOL_SIZE,
    statement_timeout=MOONSTREAM_CRAWLERS_DB_STATEMENT_TIMEOUT_MILLIS,
    pool_pre_ping=True,
)


RO_SessionLocal_preping = sessionmaker(bind=RO_pre_ping_engine)


def yield_db_read_only_preping_session() -> Generator[Session, None, None]:
    session = RO_SessionLocal_preping()
    try:
        yield session
    finally:
        session.close()


yield_db_read_only_preping_session_ctx = contextmanager(
    yield_db_read_only_preping_session
)


# Read only pre-ping query timeout
RO_pre_ping_query_engine = create_moonstream_engine(
    url=MOONSTREAM_DB_URI_READ_ONLY,
    pool_size=MOONSTREAM_POOL_SIZE,
    statement_timeout=MOONSTREAM_QUERY_API_DB_STATEMENT_TIMEOUT_MILLIS,
    pool_pre_ping=True,
)
