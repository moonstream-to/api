"""
Moonstream database connection.
"""

import logging
import os
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    MOONSTREAM_DB_V3_URI = os.environ.get("MOONSTREAM_DB_V3_URI")
    if MOONSTREAM_DB_V3_URI is None:
        raise Warning("MOONSTREAM_DB_V3_URI environment variable must be set")

    MOONSTREAM_DB_V3_URI_READ_ONLY = os.environ.get("MOONSTREAM_DB_V3_URI_READ_ONLY")
    if MOONSTREAM_DB_V3_URI_READ_ONLY is None:
        raise Warning("MOONSTREAM_DB_V3_URI_READ_ONLY environment variable must be set")

    MOONSTREAM_DB_V3_INDEXES_URI = os.environ.get("MOONSTREAM_DB_V3_INDEXES_URI")
    if MOONSTREAM_DB_V3_INDEXES_URI is None:
        raise Warning("MOONSTREAM_DB_V3_INDEXES_URI environment variable must be set")

    MOONSTREAM_DB_V3_INDEXES_URI_READ_ONLY = os.environ.get(
        "MOONSTREAM_DB_V3_INDEXES_URI_READ_ONLY"
    )
    if MOONSTREAM_DB_V3_INDEXES_URI_READ_ONLY is None:
        raise Warning(
            "MOONSTREAM_DB_V3_INDEXES_URI_READ_ONLY environment variable must be set"
        )
except ValueError as e:
    raise ValueError(e)
except Warning:
    logger.warning("Database variables not set")

MOONSTREAM_POOL_SIZE_RAW = os.environ.get("MOONSTREAM_POOL_SIZE")
MOONSTREAM_POOL_SIZE = 1
try:
    if MOONSTREAM_POOL_SIZE_RAW is not None:
        MOONSTREAM_POOL_SIZE = int(MOONSTREAM_POOL_SIZE_RAW)
except:
    raise ValueError(
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
        f"MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIS must be an integer: {MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIS_RAW}"
    )


def create_moonstream_engine(
    url: str,
    pool_size: int,
    statement_timeout: int,
    pool_pre_ping: bool = False,
    schema: Optional[str] = None,
) -> Engine:
    # Pooling: https://docs.sqlalchemy.org/en/14/core/pooling.html#sqlalchemy.pool.QueuePool
    # Statement timeout: https://stackoverflow.com/a/44936982
    options = f"-c statement_timeout={statement_timeout}"
    if schema is not None:
        options += f" -c search_path={schema}"
    return create_engine(
        url=url,
        pool_pre_ping=pool_pre_ping,
        pool_size=pool_size,
        connect_args={"options": options},
    )


class DBEngine:
    def __init__(self, url: str, schema: Optional[str] = None) -> None:
        self._engine = create_moonstream_engine(
            url=url,  # type: ignore
            pool_size=MOONSTREAM_POOL_SIZE,
            statement_timeout=MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIS,
            schema=schema,
        )

    @property
    def engine(self) -> Engine:
        return self._engine


class MoonstreamDBEngine(DBEngine):
    def __init__(self, schema: Optional[str] = None) -> None:
        super().__init__(url=MOONSTREAM_DB_V3_URI, schema=schema)

        self._session_local = sessionmaker(bind=self.engine)

        self._yield_db_session_ctx = contextmanager(self.yield_db_session)

    @property
    def session_local(self):
        return self._session_local

    @property
    def yield_db_session_ctx(self):
        return self._yield_db_session_ctx

    def yield_db_session(
        self,
    ) -> Generator[Session, None, None]:
        """
        Yields a database connection (created using environment variables).
        As per FastAPI docs:
        https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency
        """
        session = self._session_local()
        try:
            yield session
        finally:
            session.close()


class MoonstreamDBEngineRO(DBEngine):
    def __init__(self, schema: Optional[str] = None) -> None:
        super().__init__(url=MOONSTREAM_DB_V3_URI_READ_ONLY, schema=schema)

    @property
    def engine(self):
        raise AttributeError(
            "RO_engine should be used instead of engine for read-only access."
        )

    @property
    def RO_engine(self) -> Engine:
        return self._engine

    @property
    def RO_session_local(self):
        return self._session_local

    @property
    def RO_yield_db_session_ctx(self):
        return self._yield_db_session_ctx

    def yield_db_read_only_session(self) -> Generator[Session, None, None]:
        """
        Yields read-only database connection (created using environment variables).
        As per FastAPI docs:
        https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency
        """
        session = self._session_local()
        try:
            yield session
        finally:
            session.close()


class MoonstreamDBIndexesEngine(DBEngine):
    def __init__(self, schema: Optional[str] = None) -> None:
        super().__init__(url=MOONSTREAM_DB_V3_INDEXES_URI, schema=schema)

        self._session_local = sessionmaker(bind=self.engine)

        self._yield_db_session_ctx = contextmanager(self.yield_db_session)

    @property
    def session_local(self):
        return self._session_local

    @property
    def yield_db_session_ctx(self):
        return self._yield_db_session_ctx

    def yield_db_session(
        self,
    ) -> Generator[Session, None, None]:
        """
        Yields a database connection (created using environment variables).
        As per FastAPI docs:
        https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency
        """
        session = self._session_local()
        try:
            yield session
        finally:
            session.close()


class MoonstreamDBIndexesEngineRO(DBEngine):
    def __init__(self, schema: Optional[str] = None) -> None:
        super().__init__(url=MOONSTREAM_DB_V3_INDEXES_URI_READ_ONLY, schema=schema)

    @property
    def engine(self):
        raise AttributeError(
            "RO_engine should be used instead of engine for read-only access."
        )

    @property
    def RO_engine(self) -> Engine:
        return self._engine

    @property
    def RO_session_local(self):
        return self._session_local

    @property
    def RO_yield_db_session_ctx(self):
        return self._yield_db_session_ctx

    def yield_db_read_only_session(self) -> Generator[Session, None, None]:
        """
        Yields read-only database connection (created using environment variables).
        As per FastAPI docs:
        https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency
        """
        session = self._session_local()
        try:
            yield session
        finally:
            session.close()
