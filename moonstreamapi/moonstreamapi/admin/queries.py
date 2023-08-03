import argparse
import json
import logging
import textwrap
from typing import Any, Dict

from bugout.data import BugoutResources
from bugout.exceptions import BugoutResponseException
from moonstream.client import Moonstream  # type: ignore
from sqlalchemy import text

from ..actions import get_all_entries_from_search, name_normalization
from ..data import BUGOUT_RESOURCE_QUERY_RESOLVER
from ..settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_QUERIES_JOURNAL_ID,
    MOONSTREAM_QUERY_TEMPLATE_CONTEXT_TYPE,
)
from ..settings import bugout_client as bc

logger = logging.getLogger(__name__)


def create_query_template(args: argparse.Namespace) -> None:
    """
    Create query template for all queries resources.
    """

    query = ""
    with args.query_file:
        query = textwrap.indent(args.query_file.read(), "    ")

    ### Create query template

    name = f"template_{name_normalization(args.name)}"

    try:
        entry = bc.create_entry(
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            title=args.name,
            content=query,
            tags=["query_template", f"query_url:{name}"],
            context_id=name,
            context_type=MOONSTREAM_QUERY_TEMPLATE_CONTEXT_TYPE,
            context_url=name,
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )

    except BugoutResponseException as err:
        logger.error(f"Failed to create query template: {err}")
        return
    except Exception as err:
        logger.error(f"Failed to create query template: {err}")
        return

    logger.info(f"Query template created: {entry.id}")
    logger.info(f"Query template created url name: {name}")

    ### Add query id

    try:
        bc.create_tags(
            journal_id=MOONSTREAM_QUERIES_JOURNAL_ID,
            entry_id=entry.id,
            tags=[f"query_id:{entry.id}"],
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )

    except BugoutResponseException as err:
        logger.error(f"Failed to add query id: {err}")
        return
    except Exception as err:
        logger.error(f"Failed to add query id: {err}")
        return

    logger.info(f"Query created: {json.dumps(entry.dict(), indent=4)}")
