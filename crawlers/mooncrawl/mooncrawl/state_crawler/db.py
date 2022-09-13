import logging
import json
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

    """
    label_model = get_label_model(blockchain_type)

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
    block_number_cutoff: int,
    block_number: int,
) -> None:
    """
    Remove all labels with the given name from the database.
    """

    label_model = get_label_model(blockchain_type)

    table = label_model.__tablename__

    try:
        logger.info("Removing labels from database")
        db_session.execute(
            """DELETE FROM {} WHERE label =:label and block_number < :block_number""".format(
                table
            ),
            {
                "label": VIEW_STATE_CRAWLER_LABEL,
                "block_number": block_number - block_number_cutoff,
            },
        )
    except Exception as e:
        logger.error(f"Failed to remove labels: {e}")
        db_session.rollback()
        raise e
