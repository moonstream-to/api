import logging
from typing import Dict, Any

from moonstreamdb.blockchain import AvailableBlockchainType, get_label_model
from sqlalchemy.orm import Session

from ..settings import VIEW_STATE_CRAWLER_LABEL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def view_call_to_label(
    blockchain_type: AvailableBlockchainType,
    call: Dict[str, Any],
    label_name=VIEW_STATE_CRAWLER_LABEL,
):

    """
    Creates a label model.

                    "result": calls[index]["method"].decode_output(encoded_data[1]),
                    "hash": calls[index]["hash"],
                    "address": calls[index]["address"],
                    "name": calls[index]["method"].name,
                    "inputs": calls[index]["inputs"],
                    "block_number": block_number,
    """
    label_model = get_label_model(blockchain_type)
    label = label_model(
        label=label_name,
        label_data={
            "type": "view",
            "name": call["name"],
            "result": call["result"],
            "inputs": call["inputs"],
            "call_data": call["call_data"],
            "status": call["status"],
        },
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
