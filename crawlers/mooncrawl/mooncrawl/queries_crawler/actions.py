import csv
import json
import logging
import re
import uuid
from datetime import datetime, timezone
from enum import Enum
from io import StringIO
from typing import Any, Dict, List, Optional, Tuple

from moonstreamdb.db import (
    MOONSTREAM_DB_URI_READ_ONLY,
    MOONSTREAM_POOL_SIZE,
    create_moonstream_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from ..reporter import reporter
from ..settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_QUERIES_JOURNAL_ID,
    MOONSTREAM_QUERY_API_DB_STATEMENT_TIMEOUT_MILLIS,
    bugout_client,
)
from ..stats_worker.queries import to_json_types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QUERY_REGEX = re.compile("[\[\]@#$%^&?;`/]")


class OutputType(Enum):
    NONE = None
    CSV = "csv"
    JSON = "json"


class QueryNotValid(Exception):
    """
    Raised when query validation not passed.
    """


class QueryNotApproved(Exception):
    """
    Raised when query not approved
    """


def query_validation(query: str) -> str:
    """
    Sanitize provided query.
    """
    if QUERY_REGEX.search(query) != None:
        raise QueryNotValid("Query contains restricted symbols")

    return query


def fetch_query_from_journal(query_id: uuid.UUID, allow_not_approved: bool = False):
    """
    Fetch query from moonstream-queries journal.
    """
    query = bugout_client.get_entry(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
        entry_id=query_id,
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    approved = False
    for tag in query.tags:
        if tag == "approved":
            approved = True
    if not approved and not allow_not_approved:
        raise QueryNotApproved("Query not approved")

    return query


def fetch_data_from_db(
    query_id: str,
    query: str,
    params: Optional[Dict[str, Any]] = None,
) -> Tuple[Any, Any]:
    """
    Fetch data from moonstream database.
    """
    engine = create_moonstream_engine(
        MOONSTREAM_DB_URI_READ_ONLY,
        pool_pre_ping=True,
        pool_size=MOONSTREAM_POOL_SIZE,
        statement_timeout=MOONSTREAM_QUERY_API_DB_STATEMENT_TIMEOUT_MILLIS,
    )
    process_session = sessionmaker(bind=engine)
    db_session = process_session()

    time_now = datetime.now(timezone.utc)

    try:
        result = db_session.execute(text(query), params)
        data_keys = result.keys()
        data_rows = result.fetchall()
    except Exception as err:
        db_session.rollback()
        reporter.error_report(
            err,
            [
                "queries",
                "execution",
                "db",
                f"query_id:{query_id}",
            ],
        )
    finally:
        db_session.close()

    exec_timedelta = datetime.now(timezone.utc) - time_now
    logger.info(
        f"Database query finished in {int(exec_timedelta.total_seconds())} seconds"
    )

    return data_keys, data_rows


def prepare_output(
    output_type: OutputType, data_keys: Tuple[Any], data_rows: Tuple[List[Any]]
) -> str:
    """
    Parse incoming data from database to proper format OutputType.
    """

    def prepare_dict(
        data_temp_keys: Tuple[Any], data_temp_rows: Tuple[List[Any]]
    ) -> List[Dict[str, Any]]:
        output_raw = []
        for row in data_temp_rows:
            data_r = {}
            for i, k in enumerate(data_temp_keys):
                data_r[k] = to_json_types(row[i])
            output_raw.append(data_r)

        return output_raw

    output: Any = None
    if output_type.value == "csv":
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer, delimiter=";")

        csv_writer.writerow(data_keys)
        csv_writer.writerows(data_rows)

        output = csv_buffer.getvalue().encode("utf-8")
    elif output_type.value == "json":
        output_raw = prepare_dict(data_keys, data_rows)
        output = json.dumps(output_raw).encode("utf-8")
    elif output_type.value is None:
        output = prepare_dict(data_keys, data_rows)
    else:
        raise Exception("Unsupported output type")

    return output
