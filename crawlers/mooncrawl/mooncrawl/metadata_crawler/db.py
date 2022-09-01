from cgitb import reset
from genericpath import exists
import logging
from typing import Dict, Any, Optional
from unittest import result

from moonstreamdb.blockchain import AvailableBlockchainType, get_label_model
from sqlalchemy.orm import Session

from ..data import TokenURIs
from ..settings import VIEW_STATE_CRAWLER_LABEL, METADATA_CRAWLER_LABEL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def metadata_to_label(
    blockchain_type: AvailableBlockchainType,
    metadata: Optional[Dict[str, Any]],
    token_uri_data: Dict[str, Any],
    label_name=METADATA_CRAWLER_LABEL,
):

    """
    Creates a label model.
    """
    label_model = get_label_model(blockchain_type)
    label = label_model(
        label=label_name,
        label_data={
            "type": "metadata",
            "token_id": token_uri_data.token_id,
            "metadata": metadata,
        },
        address=token_uri_data.address,
        block_number=token_uri_data.block_number,
        transaction_hash=None,
        block_timestamp=token_uri_data.block_timestamp,
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


def get_uris_of_tokens(
    db_session: Session, blockchain_type: AvailableBlockchainType
) -> Dict[str, str]:

    """
    Get meatadata URIs.
    """
    metadata_for_parsing = db_session.execute(
        """ SELECT
            DISTINCT ON(label_data -> 'inputs'-> 0 ) label_data -> 'inputs'-> 0 as token_id,
            label_data -> 'result' as token_uri,
            block_number as block_number,
            block_timestamp as block_timestamp,
            address as address

        FROM
            polygon_labels
        WHERE
            label = 'view-state-alpha'
            AND label_data ->> 'name' = 'tokenURI'
        ORDER BY
            label_data -> 'inputs'-> 0 ASC,
            block_number :: INT DESC;
    """
    )

    results = [
        TokenURIs(
            token_id=data[0],
            token_uri=data[1],
            block_number=data[2],
            block_timestamp=data[3],
            address=data[4],
        )
        for data in metadata_for_parsing
    ]

    # results = {key: value for key, value in metadata_for_parsing}
    return results


def get_current_metadata_for_address(
    db_session: Session, blockchain_type: AvailableBlockchainType, address: str
):
    """
    Get existing metadata.
    """
    current_metadata = db_session.execute(
        """ SELECT
            DISTINCT ON(label_data ->> 'token_id') label_data ->> 'token_id' as token_id
        FROM
            polygon_labels
        WHERE
            address = :address
            AND label = 'metadata-crawler'
        ORDER BY
            label_data ->> 'token_id' ASC,
            block_number :: INT DESC;
    """,
        {"address": address},
    )

    result = [data[0] for data in current_metadata]

    return result
