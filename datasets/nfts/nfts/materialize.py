import contextlib
import logging
import sqlite3
from typing import Any, Dict, Tuple, Union, cast, Iterator, List, Optional, Set
import json
from concurrent.futures import (
    ProcessPoolExecutor,
    as_completed,
    ThreadPoolExecutor,
    Future,
    wait,
)
from dataclasses import dataclass

from moonstreamdb.models import (
    EthereumLabel,
    PolygonLabel,
)

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from tqdm import tqdm
from web3 import Web3

from .data import (
    NftApprovalEvent,
    NftApprovalForAllEvent,
    NftTransaction,
    NftTransferEvent,
    Erc20TransferEvent,
)
from .datastore import insert_events, insert_transactions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ERC721_LABEL = "erc721-v2"
ERC20_LABEL = "test-erc20"


def _get_last_labeled_erc721_block(
    session: Session, label_model: Union[EthereumLabel, PolygonLabel]
) -> int:
    last = (
        session.query(label_model.block_number)
        .filter(label_model.label == ERC721_LABEL)
        .order_by(label_model.block_number.desc())
        .first()
    )
    if last is None:
        raise ValueError(f"No ERC721 labels found in {label_model.__tablename__} table")
    return last[0]


def parse_transaction_label(
    label_model: Union[EthereumLabel, PolygonLabel], blockchain_type: str
) -> NftTransaction:

    # TODO: this is done because I forgot to add value in polygon labels
    value = 0
    if label_model.label_data.get("value") is not None:
        value = label_model.label_data["value"]

    return NftTransaction(
        blockchain_type=blockchain_type,
        block_number=label_model.block_number,
        block_timestamp=label_model.block_timestamp,
        transaction_hash=label_model.transaction_hash,
        contract_address=label_model.address,
        caller_address=label_model.label_data["caller"],
        function_name=label_model.label_data["name"],
        function_args=label_model.label_data["args"],
        gas_price=label_model.label_data["gasPrice"],
        value=value,
        max_fee_per_gas=label_model.label_data["maxFeePerGas"],
        max_priority_fee_per_gas=label_model.label_data["maxPriorityFeePerGas"],
    )


def _parse_transfer_event(
    label_model: Union[EthereumLabel, PolygonLabel], blockchain_type: str
) -> NftTransferEvent:

    if label_model.label_data["args"].get("tokenId") is not None:
        return NftTransferEvent(
            blockchain_type=blockchain_type,
            token_address=label_model.address,
            from_address=label_model.label_data["args"]["from"],
            to_address=label_model.label_data["args"]["to"],
            token_id=label_model.label_data["args"]["tokenId"],
            log_index=label_model.log_index,
            transaction_hash=label_model.transaction_hash,
        )
    else:
        return Erc20TransferEvent(
            blockchain_type=blockchain_type,
            token_address=label_model.address,
            from_address=label_model.label_data["args"]["from"],
            to_address=label_model.label_data["args"]["to"],
            value=label_model.label_data["args"]["value"],
            log_index=label_model.log_index,
            transaction_hash=label_model.transaction_hash,
        )


def _parse_approval_event(
    label_model: Union[EthereumLabel, PolygonLabel], blockchain_type: str
) -> NftApprovalEvent:

    return NftApprovalEvent(
        blockchain_type=blockchain_type,
        token_address=label_model.address,
        owner=label_model.label_data["args"]["owner"],
        approved=label_model.label_data["args"]["approved"],
        token_id=label_model.label_data["args"]["tokenId"],
        log_index=label_model.log_index,
        transaction_hash=label_model.transaction_hash,
    )


def _parse_approval_for_all_event(
    label_model: Union[EthereumLabel, PolygonLabel], blockchain_type: str
) -> NftApprovalForAllEvent:
    return NftApprovalForAllEvent(
        blockchain_type=blockchain_type,
        token_address=label_model.address,
        owner=label_model.label_data["args"]["owner"],
        operator=label_model.label_data["args"]["operator"],
        approved=label_model.label_data["args"]["approved"],
        log_index=label_model.log_index,
        transaction_hash=label_model.transaction_hash,
    )


def parse_event(
    label_model: Union[EthereumLabel, PolygonLabel], blockchain_type: str
) -> Union[NftTransferEvent, NftApprovalEvent, NftApprovalForAllEvent]:
    if label_model.label_data["name"] == "Transfer":
        return _parse_transfer_event(label_model, blockchain_type)
    elif label_model.label_data["name"] == "Approval":
        return _parse_approval_event(label_model, blockchain_type)
    elif label_model.label_data["name"] == "ApprovalForAll":
        return _parse_approval_for_all_event(label_model, blockchain_type)
    else:
        raise ValueError(f"Unknown label type: {label_model.label_data['name']}")


def crawl_erc721_labels(
    db_session: Session,
    datastore: str,
    label_model: Union[EthereumLabel, PolygonLabel],
    start_block: int,
    end_block: int,
    blockchain_type: str,
    batch_size: int = 10000,
):
    logger.info(
        f"Crawling {label_model.__tablename__} from {start_block} to {end_block}"
    )
    pbar = tqdm(total=(end_block - start_block + 1))
    pbar.set_description(
        f"Crawling {label_model.__tablename__} blocks {start_block}-{end_block}"
    )

    def _crawl(from_block, to_block) -> bool:
        labels = (
            db_session.query(label_model)
            .filter(
                and_(
                    label_model.block_number >= from_block,
                    label_model.block_number <= to_block,
                    or_(
                        label_model.label == ERC721_LABEL,
                        label_model.label == ERC20_LABEL,
                    ),
                )
            )
            .all()
        )
        transactions = []
        events = []
        for label in labels:
            if label.label_data["type"] == "tx_call":
                transactions.append(parse_transaction_label(label, blockchain_type))
            else:
                events.append(parse_event(label, blockchain_type))

        logger.info(f"Parsed {len(events)} events and {len(transactions)} transactions")
        with contextlib.closing(sqlite3.connect(datastore, timeout=200)) as conn:
            insert_transactions(conn, transactions)
            insert_events(conn, events)
        logger.info(f"Saved {len(events)} events and {len(transactions)} transactions")
        return True

    def crawl_with_threads(ranges: List[Tuple[int, int]]):
        futures: Dict[Future, Tuple[int, int]] = {}
        with ThreadPoolExecutor(max_workers=30) as executor:
            for from_block, to_block in ranges:
                future = executor.submit(_crawl, from_block, to_block)
                futures[future] = (from_block, to_block)

        for future in as_completed(futures):
            from_block, to_block = futures[future]
            logger.info(f"Crawled {from_block}-{to_block}")
            if future.exception() is not None:
                logger.error(
                    f"Error crawling {from_block}-{to_block}", future.exception()
                )

        wait(list(futures.keys()))

    current_block = start_block

    while current_block <= end_block:
        batch_end = min(current_block + batch_size * 10, end_block)

        # divide into batches with batch_size
        ranges = []
        batch_start = current_block
        while batch_start <= batch_end:
            ranges.append((batch_start, min(batch_start + batch_size, batch_end)))
            batch_start += batch_size + 1

        print(f"Crawling {len(ranges)} ranges")
        print(ranges)
        crawl_with_threads(ranges)
        print(f"Crawled")
        pbar.update(batch_end - current_block + 1)
        current_block = batch_end + 1
