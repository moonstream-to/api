import logging
import sqlite3
from typing import Any, cast, Iterator, List, Optional, Set
import json
from tqdm import tqdm


from moonstreamdb.models import EthereumLabel
from moonstreamdb.db import yield_db_session_ctx
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from .datastore import load_checkpoint, save_checkpoint, insert_contract_deployments
from .data import BlockBounds, ContractDeployment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_contract_deployments(
    datastore_conn: sqlite3.Connection,
    db_session: Session,
    initial_offset=0,
    bounds: Optional[BlockBounds] = None,
    batch_size: int = 10,
):
    """
    Get all contract deployments in a given block bound and add to sqlite3 database
    """

    raw_created_at_list = (
        db_session.query(EthereumLabel.created_at)
        .filter(EthereumLabel.label == "contract_deployment")
        .order_by(EthereumLabel.created_at.asc())
        .distinct(EthereumLabel.created_at)
    ).all()

    created_at_list = [
        created_at[0] for created_at in raw_created_at_list[initial_offset:]
    ]

    query = db_session.query(EthereumLabel).filter(
        EthereumLabel.label == "contract_deployment"
    )

    if bounds is not None:
        time_filters = [EthereumLabel.block_number >= bounds.starting_block]
        if bounds.ending_block is not None:
            time_filters.append(EthereumLabel.block_number <= bounds.ending_block)
        bounds_filters = [EthereumLabel.hash == None, and_(*time_filters)]

        query = query.filter(or_(*bounds_filters))

    pbar = tqdm(total=(len(raw_created_at_list)))
    pbar.set_description(f"Processing created ats")
    pbar.update(initial_offset)
    batch_start = 0
    batch_end = batch_start + batch_size
    while batch_start <= len(created_at_list):
        labels = query.filter(
            EthereumLabel.created_at.in_(created_at_list[batch_start : batch_end + 1])
        ).all()
        if len(labels) == 0:
            continue
        contract_deployment_batch: List[ContractDeployment] = []
        for label in labels:
            contract_deployment_batch.append(
                ContractDeployment(
                    address=label.address,
                    transaction_hash=label.transaction_hash,
                    block_number=label.block_number,
                    block_timestamp=label.block_timestamp,
                    deployer_address=label.label_data["deployer"],
                    gas_used=label.label_data["gasUsed"],
                    gas_price=label.label_data["gasPrice"],
                    transaction_fee=label.label_data["transactionFee"],
                )
            )
        logger.info(f"Adding {len(contract_deployment_batch)} contract deployments")
        insert_contract_deployments(datastore_conn, contract_deployment_batch)
        pbar.update(batch_end - batch_start + 1)
        batch_start = batch_end + 1
        batch_end = min(batch_end + batch_size, len(created_at_list))
    logger.info("Finished adding contract deployments")
