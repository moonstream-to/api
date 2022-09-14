import logging
import json
from typing import Dict, Any, Optional, List
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
    token_uri_data: TokenURIs,
    label_name=METADATA_CRAWLER_LABEL,
):

    """
    Creates a label model.
    """
    label_model = get_label_model(blockchain_type)

    sanityzed_label_data = json.loads(
        json.dumps(
            {
                "type": "metadata",
                "token_id": token_uri_data.token_id,
                "token_uri": token_uri_data.token_uri,
                "metadata": metadata,
            }
        ).replace(r"\u0000", "")
    )

    label = label_model(
        label=label_name,
        label_data=sanityzed_label_data,
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


def get_uri_addresses(
    db_session: Session, blockchain_type: AvailableBlockchainType
) -> List[str]:

    """
    Get meatadata URIs.
    """

    label_model = get_label_model(blockchain_type)

    addresses = (
        db_session.query(label_model.address.distinct())
        .filter(label_model.label == VIEW_STATE_CRAWLER_LABEL)
        .filter(label_model.label_data["name"].astext == "tokenURI")
    ).all()

    result = [address[0] for address in addresses]

    return result


def get_not_updated_metadata_for_address(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    address: str,
) -> List[TokenURIs]:
    """
    Get existing metadata.
    """

    label_model = get_label_model(blockchain_type)

    table = label_model.__tablename__

    current_metadata = db_session.execute(
        """ with current_tokens_uri as (
                SELECT
                    DISTINCT ON((label_data -> 'inputs' -> 0) :: int) (label_data -> 'inputs' -> 0) :: text as token_id,
                    label_data ->> 'result' as token_uri,
                    block_number,
                    address,
                    block_timestamp
                from
                    {}
                where
                    label = :view_state_label
                    AND address = :address
                    and label_data ->> 'name' = 'tokenURI'
                order by
                    (label_data -> 'inputs' -> 0) :: INT ASC,
                    block_number :: INT DESC
            ),
            tokens_metadata as (
                SELECT
                    DISTINCT ON((label_data ->> 'token_id') :: int) (label_data ->> 'token_id') :: text as token_id,
                    label_data ->>'token_uri' as token_uri,
                    block_number,
                    id
                from
                    {}
                where
                    label = :metadata_label
                    AND address = :address
                order by
                    (label_data ->> 'token_id') :: INT ASC,
                    block_number :: INT DESC
            ),
            tokens_state as (
            SELECT
                current_tokens_uri.token_id,
                current_tokens_uri.token_uri as state_token_uri,
                current_tokens_uri.block_number as view_state_block_number,
                current_tokens_uri.block_timestamp as block_timestamp,
                current_tokens_uri.address as address,
                tokens_metadata.block_number as metadata_block_number,
                tokens_metadata.token_uri as metadata_token_uri,
                tokens_metadata.id as metadata_id
            from
                current_tokens_uri
                left JOIN tokens_metadata ON current_tokens_uri.token_id = tokens_metadata.token_id
            )
            SELECT
                token_id,
                state_token_uri,
                view_state_block_number,
                block_timestamp,
                address,
                metadata_id
            from
                tokens_state
            where
                view_state_block_number > metadata_block_number OR metadata_token_uri is null OR metadata_token_uri != state_token_uri;
        """.format(
            table, table
        ),
        {
            "metadata_label": METADATA_CRAWLER_LABEL,
            "view_state_label": VIEW_STATE_CRAWLER_LABEL,
            "address": address,
        },
    ).all()

    results = [
        TokenURIs(
            token_id=data[0],
            token_uri=data[1],
            block_number=data[2],
            block_timestamp=data[3],
            address=data[4],
            metadata_id=data[5],
        )
        for data in current_metadata
    ]

    return results


def update_metadata(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    id: Dict[str, Any],
    label: Any,
) -> None:
    """
    Update metadata.
    """

    label_model = get_label_model(blockchain_type)

    db_session.query(label_model).filter(label_model.id == id).update(
        {
            "label_data": label.label_data,
            "block_number": label.block_number,
            "block_timestamp": label.block_timestamp,
        },
        synchronize_session=False,
    )
