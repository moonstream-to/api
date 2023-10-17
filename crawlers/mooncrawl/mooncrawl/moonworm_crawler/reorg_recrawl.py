import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from moonstreamdb.blockchain import AvailableBlockchainType, get_block_model
from moonworm.crawler.log_scanner import _fetch_events_chunk, _crawl_events as moonworm_autoscale_crawl_events  # type: ignore
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import and_
from web3 import Web3

from .crawler import EventCrawlJob


def reorg_scan(
    db_session,
    blockchain_type: AvailableBlockchainType,
):
    """
    Cheks for reorgs labels in database
    """
    pass


def update_reorg_labels(
    db_session,
    blockchain_type: AvailableBlockchainType,
    reorg_labels: Any,
):
    """
    Change label to reorg
    """
    pass
