import logging
from typing import Any, Dict, List
import json
from mooncrawl.data import AvailableBlockchainType
from moonstreamdb.models import Base

from sqlalchemy.orm.session import Session
from web3.main import Web3
import time
from ..settings import (
    MOONSTREAM_DATA_JOURNAL_ID,
    bugout_client,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
)
from ..blockchain import connect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _retry_connect_web3(
    blockchain_type: AvailableBlockchainType,
    retry_count: int = 10,
    sleep_time: float = 5,
) -> Web3:
    """
    Retry connecting to the blockchain.
    """
    while retry_count > 0:
        retry_count -= 1
        try:
            web3 = connect(blockchain_type)
            web3.eth.block_number
            logger.info(f"Connected to {blockchain_type}")
            return web3
        except Exception as e:
            if retry_count == 0:
                error = e
                break
            logger.error(f"Failed to connect to {blockchain_type} blockchain: {e}")
            logger.info(f"Retrying in {sleep_time} seconds")
            time.sleep(sleep_time)
    raise Exception(
        f"Failed to connect to {blockchain_type} blockchain after {retry_count} retries: {error}"
    )


def _get_heartbeat_entry_id(crawler_type: str) -> str:
    entries = bugout_client.search(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        journal_id=MOONSTREAM_DATA_JOURNAL_ID,
        query=f"#{crawler_type} #heartbeat",
        limit=1,
    )
    if entries.results:
        return entries.results[0].entry_url.split("/")[-1]
    else:
        logger.info(f"No {crawler_type} heartbeat entry found, creating one")
        entry = bugout_client.create_entry(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_DATA_JOURNAL_ID,
            title=f"{crawler_type} Heartbeat",
            tags=[crawler_type, "heartbeat"],
            content="",
        )
        return str(entry.id)


def heartbeat(crawler_type: str, crawler_status: Dict[str, Any]) -> None:
    """
    Periodically crawler will update the status in bugout entry:
    - Started at timestamp
    - Started at block number
    - Status: Running/Dead
    - Last crawled block number
    - Number of current jobs
    - Time taken to crawl last crawl_step and speed per block

    and other information later will be added.
    """
    heartbeat_entry_id = _get_heartbeat_entry_id(crawler_type)
    bugout_client.update_entry_content(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        journal_id=MOONSTREAM_DATA_JOURNAL_ID,
        entry_id=heartbeat_entry_id,
        title=f"{crawler_type} Heartbeat",
        content=f"{json.dumps(crawler_status, indent=2)}",
    )


def save_labels(db_session: Session, labels: List[Base]) -> None:
    """
    Save labels in the database.
    """
    try:
        db_session.add_all(labels)
        db_session.commit()
    except Exception as e:
        logger.error(f"Failed to save labels: {e}")
        db_session.rollback()
        raise e
