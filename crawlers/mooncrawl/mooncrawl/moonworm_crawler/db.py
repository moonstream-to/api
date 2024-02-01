import logging
import json
from typing import Dict, List, Optional, Literal

from moonstreamdb.blockchain import AvailableBlockchainType, get_label_model
from moonstreamdb.models import Base
from moonworm.crawler.function_call_crawler import ContractFunctionCall  # type: ignore
from sqlalchemy.orm import Session
from sqlalchemy.sql import text


from ..settings import CRAWLER_LABEL
from .event_crawler import Event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _event_to_label(
    blockchain_type: AvailableBlockchainType, event: Event, label_name=CRAWLER_LABEL
) -> Base:
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
) -> Base:
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

    events_hashes_to_save = [event.transaction_hash for event in events]

    existing_labels = (
        db_session.query(label_model.transaction_hash, label_model.log_index)
        .filter(
            label_model.label == label_name,
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
            labels_to_save.append(_event_to_label(blockchain_type, event, label_name))
        elif (
            event.log_index not in existing_log_index_by_tx_hash[event.transaction_hash]
        ):
            labels_to_save.append(_event_to_label(blockchain_type, event, label_name))

    logger.info(f"Saving {len(labels_to_save)} event labels to session")
    db_session.add_all(labels_to_save)


def add_function_calls_to_session(
    db_session: Session,
    function_calls: List[ContractFunctionCall],
    blockchain_type: AvailableBlockchainType,
    label_name=CRAWLER_LABEL,
) -> None:
    label_model = get_label_model(blockchain_type)
    transactions_hashes_to_save = [
        function_call.transaction_hash for function_call in function_calls
    ]

    existing_labels = (
        db_session.query(label_model.transaction_hash)
        .filter(
            label_model.label == label_name,
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

    logger.info(f"Saving {len(labels_to_save)} labels to session")
    db_session.add_all(labels_to_save)


def deduplicate_records(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    table: Literal["labels", "transactions", "blocks"],
    label_name: Optional[str] = None,
    label_type: Optional[str] = None,
) -> None:
    """
    Deduplicates records in the database.
    label name and label type work only for labels table.
    """

    if table == "blocks":
        raise NotImplementedError("Deduplication for blocks is not implemented yet")

    if table == "labels":
        label_model = get_label_model(blockchain_type)

        if label_name is None or label_type is None:
            raise ValueError(
                "label_name and label_type are required for deduplication of labels"
            )

        if label_type == "event":
            # get list of all label_type addresses

            all_addresses = (
                db_session.query(label_model.address.label("address"))
                .filter(label_model.label == label_name)
                .filter(label_model.label_data["type"] == "event")
                .distinct()
                .all()
            )  # can take a while

            for address_raw in all_addresses:
                address = address_raw[0]

                deduplicate_records = db_session.execute(
                    text(
                        """ 
                    WITH lates_labels AS (
                        SELECT
                            DISTINCT ON (transaction_hash, log_index) transaction_hash, log_index,
                            block_number as block_number,
                            created_at as created_at
                        FROM
                            {}
                        WHERE
                            label=:label
                            AND address=:address
                            AND label_data->>'type' = :label_type
                        ORDER BY
                            transaction_hash ASC,
                            log_index ASC,
                            block_number ASC,
                            created_at ASC
                    )
                    DELETE FROM
                        {} USING lates_labels
                    WHERE
                        label=:label
                        AND address=:address
                        AND label_data->>'type' = :label_type
                        AND {}.id  not in (select id from lates_labels ) RETURNING {}.block_number;
                """.format(
                            table, table, table, table
                        )
                    ),
                    {"address": address, "label": label_name, "label_type": label_type},
                )

                db_session.commit()

                logger.info(
                    f"Deleted {deduplicate_records} duplicate labels for address {address}"
                )

        if label_type == "tx_call":
            # get list of all label_type addresses

            all_addresses = (
                db_session.query(label_model.address.label("address"))
                .filter(label_model.label == label_name)
                .filter(label_model.label_data["type"] == "tx_call")
                .distinct()
                .all()
            )

            for address_raw in all_addresses:
                address = address_raw[0]

                deduplicate_records = db_session.execute(
                    text(
                        """ 
                    WITH lates_labels AS (
                        SELECT
                            DISTINCT ON (transaction_hash) transaction_hash,
                            block_number as block_number,
                            created_at as created_at
                        FROM
                            {}
                        WHERE
                            label=:label
                            AND address=:address
                            AND label_data->>'type' = :label_type
                            AND log_index is null
                        ORDER BY
                            transaction_hash ASC,
                            block_number ASC,
                            created_at ASC
                    )
                    DELETE FROM
                        {} USING lates_labels
                    WHERE
                        label=:label
                        AND address=:address
                        AND label_data->>'type' = :label_type
                        AND log_index is null
                        AND {}.id  not in (select id from lates_labels ) RETURNING {}.block_number;
                """.format(
                            table, table, table, table
                        )
                    ),
                    {"address": address, "label": label_name, "label_type": label_type},
                )

                db_session.commit()

                logger.info(
                    f"Deleted {deduplicate_records} duplicate labels for address {address}"
                )

    if table == "transactions":
        raise NotImplementedError(
            "Deduplication for transactions is not implemented yet"
        )
