import json
import logging
from typing import Any, Dict
from hexbytes import HexBytes


from moonstreamtypes.blockchain import AvailableBlockchainType, get_label_model
from sqlalchemy.orm import Session

from ..settings import VIEW_STATE_CRAWLER_LABEL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def view_call_to_label(
    blockchain_type: AvailableBlockchainType,
    call: Dict[str, Any],
    v3: bool = False,
    label_name=VIEW_STATE_CRAWLER_LABEL,
):
    """
    Creates a label model.

    """
    version = 3 if v3 else 2
    label_model = get_label_model(blockchain_type, version=version)

    sanityzed_label_data = json.loads(
        json.dumps(
            {
                "type": "view",
                "name": call["name"],
                "result": call["result"],
                "inputs": call["inputs"],
                "call_data": call["call_data"],
                "status": call["status"],
            }
        ).replace(r"\u0000", "")
    )

    if v3:

        del sanityzed_label_data["type"]
        del sanityzed_label_data["name"]

        ## add zero transaction hash

        label = label_model(
            label=label_name,
            label_name=call["name"],
            label_type="view",
            label_data=sanityzed_label_data,
            ### bytea
            address=HexBytes(call["address"]),
            block_number=call["block_number"],
            transaction_hash="0x2653135e31407726a25dd8d304878578cdfcc7d69a2b319d1aca4a37ed66956a",
            block_timestamp=call["block_timestamp"],
            block_hash=call["block_hash"],
        )

    else:

        label = label_model(
            label=label_name,
            label_data=sanityzed_label_data,
            address=call["address"],
            block_number=call["block_number"],
            transaction_hash=None,
            block_timestamp=call["block_timestamp"],
        )

    return label


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


def clean_labels(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    blocks_cutoff: int,
    block_number: int,
) -> None:
    """
    Remove all labels with the given name from the database.
    """

    label_model = get_label_model(blockchain_type)

    table = label_model.__tablename__
    print(f"Cleaning labels from table {table}")
    print(f"Current block number: {block_number} - blocks cutoff: {blocks_cutoff}")
    print(f"Deleting labels with block_number < {block_number - blocks_cutoff}")

    try:
        logger.info("Removing labels from database")
        query = db_session.query(label_model).filter(
            label_model.label == VIEW_STATE_CRAWLER_LABEL,
            label_model.block_number < block_number - blocks_cutoff,
        )
        result = query.delete(synchronize_session=False)
        db_session.commit()
        logger.info(f"Removed {result} rows from {table}")
    except Exception as e:
        logger.error(f"Failed to remove labels: {e}")
        db_session.rollback()
        raise e
