import json
import logging
from typing import Dict, List, Optional, Union, Any

from moonstreamdb.models import Base
from moonstreamtypes.blockchain import AvailableBlockchainType, get_label_model
from moonworm.crawler.function_call_crawler import ContractFunctionCall  # type: ignore
from sqlalchemy import Integer, String, column, exists, func, select, text, values
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert


from ..settings import CRAWLER_LABEL
from .event_crawler import Event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _event_to_label(
    blockchain_type: AvailableBlockchainType,
    event: Event,
    label_name=CRAWLER_LABEL,
    db_version: int = 2,
) -> Base:  # type: ignore
    """
    Creates a label model.
    """
    label_model = get_label_model(blockchain_type, version=db_version)
    sanityzed_label_data = json.loads(
        json.dumps(
            {
                "type": "event",
                "name": event.event_name,
                "args": event.args,
            }
        ).replace(r"\u0000", "")
    )

    if db_version == 2:
        label = label_model(
            label=label_name,
            label_data=sanityzed_label_data,
            address=event.address,
            block_number=event.block_number,
            block_timestamp=event.block_timestamp,
            transaction_hash=event.transaction_hash,
            log_index=event.log_index,
        )
    else:

        del sanityzed_label_data["type"]
        del sanityzed_label_data["name"]

        label = label_model(
            label=label_name,
            label_name=event.event_name,
            label_data=sanityzed_label_data,
            address=event.address,
            block_number=event.block_number,
            block_timestamp=event.block_timestamp,
            transaction_hash=event.transaction_hash,
            log_index=event.log_index,
            block_hash=event.block_hash.hex(),  # type: ignore
        )

    return label


def _function_call_to_label(
    blockchain_type: AvailableBlockchainType,
    function_call: ContractFunctionCall,
    db_version: int = 2,
    label_name=CRAWLER_LABEL,
) -> Base:  # type: ignore
    """
    Creates a label model.
    """
    label_model = get_label_model(blockchain_type, version=db_version)

    sanityzed_label_data = json.loads(
        json.dumps(
            {
                "type": "tx_call",
                "name": function_call.function_name,
                "caller": function_call.caller_address,
                "args": function_call.function_args,
                "status": function_call.status,
                "gasUsed": function_call.gas_used,
            }
        ).replace(r"\u0000", "")
    )

    if db_version == 2:

        label = label_model(
            label=label_name,
            label_data=sanityzed_label_data,
            address=function_call.contract_address,
            block_number=function_call.block_number,
            transaction_hash=function_call.transaction_hash,
            block_timestamp=function_call.block_timestamp,
        )

    else:

        del sanityzed_label_data["type"]
        del sanityzed_label_data["name"]

        label = label_model(
            label=label_name,
            label_name=function_call.function_name,
            label_data=sanityzed_label_data,
            address=function_call.contract_address,
            block_number=function_call.block_number,
            block_hash=function_call.block_hash.hex(),  # type: ignore
            transaction_hash=function_call.transaction_hash,
            block_timestamp=function_call.block_timestamp,
            caller_address=function_call.caller_address,
            origin_address=function_call.caller_address,
        )

    return label


def get_last_labeled_block_number(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    label_name=CRAWLER_LABEL,
    db_version: int = 2,
) -> Optional[int]:
    label_model = get_label_model(blockchain_type, version=db_version)
    block_number = (
        db_session.query(label_model.block_number)
        .filter(label_model.label == label_name)
        .order_by(label_model.block_number.desc())
        .limit(1)
        .one_or_none()
    )

    return block_number[0] if block_number else None


def get_first_labeled_block_number(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    address: str,
    label_name: str = CRAWLER_LABEL,
    only_events: bool = False,
    db_version: int = 2,
) -> Optional[int]:

    label_model = get_label_model(blockchain_type, version=db_version)

    base_query = (
        db_session.query(label_model.block_number)
        .filter(label_model.label == label_name, label_model.address == address)
        .order_by(label_model.block_number)
    )

    event_blocks = base_query.filter(label_model.log_index != None).first()
    function_blocks = (
        None
        if only_events
        else base_query.filter(label_model.log_index == None).first()
    )

    if event_blocks and function_blocks:
        result = max(event_blocks, function_blocks)
    elif event_blocks or function_blocks:
        result = event_blocks if event_blocks else function_blocks
    else:
        result = None

    return result[0] if result else None


def commit_session(db_session: Session) -> None:
    """
    Save labels in the database.
    """
    try:
        logger.info("Committing session to database")
        db_session.commit()
    except Exception as e:
        logger.error(f"Failed to save labels: {e}")
        db_session.rollback()
        raise e


def add_events_to_session(
    db_session: Session,
    events: List[Event],
    blockchain_type: AvailableBlockchainType,
    db_version: int = 2,
    label_name=CRAWLER_LABEL,
) -> None:

    if len(events) == 0:
        return

    label_model = get_label_model(blockchain_type, version=db_version)

    if db_version == 2:

        events_hashes_to_save = set([event.transaction_hash for event in events])

        # Define a CTE VALUES expression to escape big IN clause
        hashes_cte = select(
            values(column("transaction_hash", String), name="hashes").data(
                [(hash,) for hash in events_hashes_to_save]
            )
        ).cte()

        # Retrieve existing transaction hashes and registered log indexes
        query = (
            db_session.query(
                label_model.transaction_hash.label("transaction_hash"),
                func.array_agg(label_model.log_index).label("log_indexes"),
            )
            .filter(
                label_model.label == label_name,
                label_model.log_index.isnot(None),
                exists().where(
                    label_model.transaction_hash == hashes_cte.c.transaction_hash
                ),
            )
            .group_by(label_model.transaction_hash)
        )

        existing_log_index_by_tx_hash = {
            row.transaction_hash: row.log_indexes for row in query
        }

        labels_to_save = [
            _event_to_label(blockchain_type, event, label_name)
            for event in events
            if event.transaction_hash not in existing_log_index_by_tx_hash
            or event.log_index
            not in existing_log_index_by_tx_hash[event.transaction_hash]
        ]

        logger.info(f"Saving {len(labels_to_save)} event labels to session")
        db_session.add_all(labels_to_save)

    else:

        # Define the table name and columns based on the blockchain type
        table = label_model.__table__

        # Create a list of dictionaries representing new records
        records = []
        for event in events:

            label_event = _event_to_label(
                blockchain_type, event, label_name, db_version
            )

            record = {
                "label": label_event.label,
                "transaction_hash": label_event.transaction_hash,
                "log_index": label_event.log_index,
                "block_number": label_event.block_number,
                "block_hash": label_event.block_hash,
                "block_timestamp": label_event.block_timestamp,
                "caller_address": None,
                "origin_address": None,
                "address": label_event.address,
                "label_name": label_event.label_name,
                "label_type": "event",
                "label_data": label_event.label_data,
            }

            records.append(record)

        # Insert records using a single batched query with an ON CONFLICT clause
        statement = insert(table).values(records)
        do_nothing_statement = statement.on_conflict_do_nothing(
            index_elements=["transaction_hash", "log_index"],
            index_where=(table.c.label == "seer") & (table.c.label_type == "event"),
        )

        db_session.execute(do_nothing_statement)

        logger.info(f"Batch inserted {len(records)} event labels into {table.name}")


def add_function_calls_to_session(
    db_session: Session,
    function_calls: List[ContractFunctionCall],
    blockchain_type: AvailableBlockchainType,
    db_version: int = 2,
    label_name=CRAWLER_LABEL,
) -> None:

    if len(function_calls) == 0:
        return

    if db_version == 2:

        label_model = get_label_model(blockchain_type, version=db_version)

        transactions_hashes_to_save = list(
            set([function_call.transaction_hash for function_call in function_calls])
        )

        # Define a CTE VALUES expression to escape big IN clause
        hashes_cte = select(
            values(column("transaction_hash", String), name="hashes").data(
                [(hash,) for hash in transactions_hashes_to_save]
            )
        ).cte()

        # Retrieve existing transaction hashes
        query = db_session.query(
            label_model.transaction_hash.label("transaction_hash")
        ).filter(
            label_model.label == label_name,
            label_model.log_index.is_(None),
            exists().where(
                label_model.transaction_hash == hashes_cte.c.transaction_hash
            ),
        )

        existing_tx_hashes = [row.transaction_hash for row in query]

        labels_to_save = [
            _function_call_to_label(blockchain_type, function_call)
            for function_call in function_calls
            if function_call.transaction_hash not in existing_tx_hashes
        ]

        logger.info(f"Saving {len(labels_to_save)} labels to session")
        db_session.add_all(labels_to_save)

    else:

        label_model = get_label_model(blockchain_type, version=db_version)

        # Define the table name and columns based on the blockchain type
        table = label_model.__table__

        # Create a list of dictionaries representing new records
        records = []
        for function_call in function_calls:

            label_function_call = _function_call_to_label(
                blockchain_type, function_call, db_version
            )

            record = {
                "label": label_name,
                "transaction_hash": label_function_call.transaction_hash,
                "log_index": None,
                "block_number": label_function_call.block_number,
                "block_hash": label_function_call.block_hash,
                "block_timestamp": label_function_call.block_timestamp,
                "caller_address": label_function_call.caller_address,
                "origin_address": label_function_call.caller_address,
                "address": label_function_call.address,
                "label_name": label_function_call.label_name,
                "label_type": "tx_call",
                "label_data": label_function_call.label_data,
            }

            records.append(record)

        # Insert records using a single batched query with an ON CONFLICT clause
        statement = insert(table).values(records)
        do_nothing_statement = statement.on_conflict_do_nothing(
            index_elements=["transaction_hash"],
            index_where=(table.c.label == "seer") & (table.c.label_type == "tx_call"),
        )

        db_session.execute(do_nothing_statement)

        logger.info(
            f"Batch inserted {len(records)} function call labels into {table.name}"
        )
