import logging
from typing import Any, Dict, List, Optional, Union

from eth_typing.evm import ChecksumAddress
from hexbytes.main import HexBytes
from moonstreamdb.db import yield_db_session_ctx
from moonstreamdb.models import (
    Base,
    EthereumLabel,
    EthereumTransaction,
    PolygonLabel,
    PolygonTransaction,
)
from moonworm.crawler.function_call_crawler import (
    ContractFunctionCall,
)

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import label

from ..blockchain import connect, get_block_model, get_label_model
from ..data import AvailableBlockchainType
from ..settings import CRAWLER_LABEL
from .crawler import FunctionCallCrawlJob, _generate_reporter_callback
from .event_crawler import Event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _event_to_label(blockchain_type: AvailableBlockchainType, event: Event) -> Base:
    """
    Creates a label model.
    """
    label_model = get_label_model(blockchain_type)
    label = label_model(
        label=CRAWLER_LABEL,
        label_data={
            "type": "event",
            "name": event.event_name,
            "args": event.args,
        },
        address=event.address,
        block_number=event.block_number,
        block_timestamp=event.block_timestamp,
        transaction_hash=event.transaction_hash,
        log_index=event.log_index,
    )
    return label


def _function_call_to_label(
    blockchain_type: AvailableBlockchainType, function_call: ContractFunctionCall
) -> Base:
    """
    Creates a label model.
    """
    label_model = get_label_model(blockchain_type)
    label = label_model(
        label=CRAWLER_LABEL,
        label_data={
            "type": "tx_call",
            "name": function_call.function_name,
            "caller": function_call.caller_address,
            "args": function_call.function_args,
            "status": function_call.status,
            "gasUsed": function_call.gas_used,
        },
        address=function_call.contract_address,
        block_number=function_call.block_number,
        transaction_hash=function_call.transaction_hash,
        block_timestamp=function_call.block_timestamp,
    )

    return label


def get_last_labeled_block_number(
    db_session: Session, blockchain_type: AvailableBlockchainType
) -> Optional[int]:
    label_model = get_label_model(blockchain_type)
    block_number = (
        db_session.query(label_model.block_number)
        .filter(label_model.label == CRAWLER_LABEL)
        .order_by(label_model.block_number.desc())
        .limit(1)
        .one_or_none()
    )

    return block_number[0] if block_number else None


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


def save_events(
    db_session: Session, events: List[Event], blockchain_type: AvailableBlockchainType
) -> None:
    label_model = get_label_model(blockchain_type)

    events_hashes_to_save = [event.transaction_hash for event in events]

    existing_labels = (
        db_session.query(label_model.transaction_hash, label_model.log_index)
        .filter(
            label_model.label == CRAWLER_LABEL,
            label_model.log_index != None,
            label_model.transaction_hash.in_(events_hashes_to_save),
        )
        .all()
    )

    existing_labels_transactions = []
    existing_log_index_by_tx_hash: Dict[str, List[int]] = {}
    for label in existing_labels:
        if label[0] not in existing_labels_transactions:
            existing_labels_transactions.append(label[0])
            existing_log_index_by_tx_hash[label[0]] = []
        existing_log_index_by_tx_hash[label[0]].append(label[1])

    labels_to_save = []
    for event in events:
        if event.transaction_hash not in existing_labels_transactions:
            labels_to_save.append(_event_to_label(blockchain_type, event))
        elif (
            event.log_index not in existing_log_index_by_tx_hash[event.transaction_hash]
        ):
            labels_to_save.append(_event_to_label(blockchain_type, event))

    save_labels(db_session, labels_to_save)


def save_function_calls(
    db_session: Session,
    function_calls: List[ContractFunctionCall],
    blockchain_type: AvailableBlockchainType,
) -> None:

    label_model = get_label_model(blockchain_type)
    transactions_hashes_to_save = [
        function_call.transaction_hash for function_call in function_calls
    ]

    existing_labels = (
        db_session.query(label_model.transaction_hash)
        .filter(
            label_model.label == CRAWLER_LABEL,
            label_model.log_index == None,
            label_model.transaction_hash.in_(transactions_hashes_to_save),
        )
        .all()
    )

    existing_labels_transactions = [label[0] for label in existing_labels]

    labels_to_save = [
        _function_call_to_label(blockchain_type, function_call)
        for function_call in function_calls
        if function_call.transaction_hash not in existing_labels_transactions
    ]

    save_labels(db_session, labels_to_save)
