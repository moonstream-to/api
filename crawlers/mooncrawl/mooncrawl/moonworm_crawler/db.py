import logging
import json
from typing import Dict, List, Optional

from moonstreamdb.blockchain import (
    AvailableBlockchainType,
    get_label_model,
    get_block_model,
)
from moonstreamdb.models import Base
from moonworm.crawler.function_call_crawler import ContractFunctionCall  # type: ignore

# from sqlalchemy.dialects.postgresql.dml import insert
from sqlalchemy.orm import Session, aliased
from sqlalchemy import insert, text, and_, exists, or_, func, update


from ..settings import CRAWLER_LABEL
from .event_crawler import Event
from web3 import Web3


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _event_to_label(
    blockchain_type: AvailableBlockchainType, event: Event, label_name=CRAWLER_LABEL
) -> Base:  # type: ignore
    """
    Creates a label model.
    """
    label_model = get_label_model(blockchain_type)
    sanityzed_label_data = json.loads(
        json.dumps(
            {
                "type": "event",
                "name": event.event_name,
                "args": event.args,
            }
        ).replace(r"\u0000", "")
    )

    label = label_model(
        label=label_name,
        label_data=sanityzed_label_data,
        address=event.address,
        block_number=event.block_number,
        block_timestamp=event.block_timestamp,
        transaction_hash=event.transaction_hash,
        log_index=event.log_index,
    )
    return label


def _function_call_to_label(
    blockchain_type: AvailableBlockchainType,
    function_call: ContractFunctionCall,
    label_name=CRAWLER_LABEL,
) -> Base:  # type: ignore
    """
    Creates a label model.
    """
    label_model = get_label_model(blockchain_type)

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

    label = label_model(
        label=label_name,
        label_data=sanityzed_label_data,
        address=function_call.contract_address,
        block_number=function_call.block_number,
        transaction_hash=function_call.transaction_hash,
        block_timestamp=function_call.block_timestamp,
    )

    return label


def get_last_labeled_block_number(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    label_name=CRAWLER_LABEL,
) -> Optional[int]:
    label_model = get_label_model(blockchain_type)
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
    label_name=CRAWLER_LABEL,
    only_events: bool = False,
) -> Optional[int]:
    label_model = get_label_model(blockchain_type)
    block_number_query = (
        db_session.query(label_model.block_number)
        .filter(label_model.label == label_name)
        .filter(label_model.address == address)
    )

    function_call_block_numbers = (
        block_number_query.filter(label_model.log_index == None)
        .order_by(label_model.block_number)
        .limit(50)
        .all()
    )
    event_block_numbers = (
        block_number_query.filter(label_model.log_index != None)
        .order_by(label_model.block_number)
        .limit(50)
        .all()
    )

    if only_events:
        return event_block_numbers[0][0] if event_block_numbers else None
    else:
        event_block_number = event_block_numbers[0][0] if event_block_numbers else -1
        function_call_block_number = (
            function_call_block_numbers[0][0] if function_call_block_numbers else -1
        )
        max_block_number = max(event_block_number, function_call_block_number)
        return max_block_number if max_block_number != -1 else None


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
    label_name=CRAWLER_LABEL,
) -> None:
    label_model = get_label_model(blockchain_type)

    label_name = f"{label_name}-unverified"

    events_insert = []
    for raw_event in events:
        db_event = _event_to_label(blockchain_type, raw_event, label_name)
        events_insert.append(
            {
                "label": db_event.label,
                "label_data": db_event.label_data,
                "address": db_event.address,
                "block_number": db_event.block_number,
                "block_timestamp": db_event.block_timestamp,
                "transaction_hash": db_event.transaction_hash,
                "log_index": db_event.log_index,
            }
        )

    insert_statement = insert(label_model).values(events_insert)

    db_session.execute(insert_statement)


def add_function_calls_to_session(
    db_session: Session,
    function_calls: List[ContractFunctionCall],
    blockchain_type: AvailableBlockchainType,
    label_name=CRAWLER_LABEL,
) -> None:
    label_model = get_label_model(blockchain_type)

    label_name = f"{label_name}-unverified"

    function_calls_insert = []

    for raw_function_call in function_calls:
        db_function_call = _function_call_to_label(
            blockchain_type, raw_function_call, label_name
        )
        function_calls_insert.append(
            {
                "label": db_function_call.label,
                "label_data": db_function_call.label_data,
                "address": db_function_call.address,
                "block_number": db_function_call.block_number,
                "block_timestamp": db_function_call.block_timestamp,
                "transaction_hash": db_function_call.transaction_hash,
            }
        )

    logger.info(f"Saving {len(function_calls_insert)} labels to session")
    insert_statement = insert(label_model).values(function_calls_insert)

    db_session.execute(insert_statement)


def write_to_db(
    web3: Web3,
    blockchain_type: AvailableBlockchainType,
    db_session: Session,
    label_name=CRAWLER_LABEL,
    conformations: int = 100,
):
    """
    Take all unvirified labels and update label to label_name.
    Get last block number from block model and update label to label_name with deduplication of labels distinct ON (transaction_hash, log_index) for events and distinct ON (transaction_hash) for function calls.
    And that
    """

    label_model = get_label_model(blockchain_type)

    block_model = get_block_model(blockchain_type)

    label_name_unverified = f"{label_name}-unverified"

    label_model_alias = aliased(label_model, name="polygon_labels2")

    # update all labels to label_name

    blockchain_block_number = web3.eth.block_number

    latest_block = (
        db_session.query(block_model.block_number)
        .order_by(block_model.block_number.desc())
        .limit(1)
    )

    latest_block_cte = latest_block.cte("latest_block")

    events = (
        db_session.query(
            label_model.id, label_model.transaction_hash, label_model.log_index
        )
        .distinct(label_model.transaction_hash, label_model.log_index)
        .filter(label_model.label == label_name_unverified)
        .filter(label_model.log_index != None)
        .filter(
            or_(
                label_model.block_number <= latest_block_cte.c.block_number,
                label_model.block_number <= blockchain_block_number - conformations,
            )
        )
        .filter(
            ~db_session.query(label_model_alias)
            .filter(
                and_(
                    label_model_alias.label == label_name,
                    label_model_alias.transaction_hash == label_model.transaction_hash,
                    label_model_alias.log_index == label_model.log_index,
                )
            )
            .exists()
        )
        .order_by(
            label_model.transaction_hash,
            label_model.log_index,
            label_model.block_number.desc(),
        )
    )

    events_cte = events.cte("events")

    function_calls = (
        db_session.query(
            label_model.id, label_model.transaction_hash, label_model.log_index
        )
        .distinct(label_model.transaction_hash)
        .filter(label_model.label == label_name_unverified)
        .filter(label_model.log_index == None)
        .filter(
            or_(
                label_model.block_number <= latest_block_cte.c.block_number,
                label_model.block_number <= blockchain_block_number - conformations,
            )
        )
        .filter(
            ~db_session.query(label_model_alias)
            .filter(
                and_(
                    label_model_alias.label == label_name,
                    label_model_alias.transaction_hash == label_model.transaction_hash,
                    label_model_alias.log_index == None,
                )
            )
            .exists()
        )
        .order_by(label_model.transaction_hash, label_model.block_number.desc())
    )

    function_calls_cte = function_calls.cte("function_calls")

    union_all_subquery = (
        db_session.query(events_cte)
        .union_all(db_session.query(function_calls_cte))
        .subquery()
    )

    logger.info("Updating labels")
    # Update query
    updated_labels = (
        db_session.query(label_model)
        .filter(label_model.id == union_all_subquery.c.events_id)
        .update(
            {"label": label_name}, synchronize_session=False
        )  # returns number of rows updated by query
    )

    logger.info(
        f"latest block number database {latest_block.one_or_none()} , blockchain {blockchain_block_number} - conformations {conformations}"
    )

    logger.info(f"Updated {updated_labels} labels")


def delete_unverified_duplicates(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    label_name=CRAWLER_LABEL,
):
    """
    Delete all unverified labels which already have verified labels.
    """

    label_model = get_label_model(blockchain_type)

    label_name_unverified = f"{label_name}-unverified"

    label_model_alias = aliased(label_model, name="polygon_labels2")

    duplicated_events = (
        db_session.query(
            label_model.id, label_model.transaction_hash, label_model.log_index
        )
        .distinct(label_model.transaction_hash, label_model.log_index)
        .filter(label_model.label == label_name_unverified)
        .filter(label_model.log_index != None)
        .filter(
            db_session.query(label_model_alias)
            .filter(
                and_(
                    label_model_alias.label == label_name,
                    label_model_alias.transaction_hash == label_model.transaction_hash,
                    label_model_alias.log_index == label_model.log_index,
                )
            )
            .exists()
        )
        .order_by(
            label_model.transaction_hash,
            label_model.log_index,
            label_model.block_number.desc(),
        )
    )

    events_cte = duplicated_events.cte("events")

    duplicated_function_calls = (
        db_session.query(
            label_model.id, label_model.transaction_hash, label_model.log_index
        )
        .distinct(label_model.transaction_hash)
        .filter(label_model.label == label_name_unverified)
        .filter(label_model.log_index == None)
        .filter(
            db_session.query(label_model_alias)
            .filter(
                and_(
                    label_model_alias.label == label_name,
                    label_model_alias.transaction_hash == label_model.transaction_hash,
                    label_model_alias.log_index == None,
                )
            )
            .exists()
        )
        .order_by(label_model.transaction_hash, label_model.block_number.desc())
    )

    function_calls_cte = duplicated_function_calls.cte("function_calls")

    union_all_subquery = (
        db_session.query(events_cte)
        .union_all(db_session.query(function_calls_cte))
        .subquery()
    )

    logger.info("Deleting duplicates labels")

    # Delete query

    deleted_labels = (
        db_session.query(label_model)
        .filter(label_model.id == union_all_subquery.c.events_id)
        .delete(synchronize_session=False)  # returns number of rows updated by query
    )

    logger.info(f"Deleted duplicates {deleted_labels} labels")
