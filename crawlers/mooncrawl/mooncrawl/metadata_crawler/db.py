import logging
import json
from typing import Dict, Any, Optional, List

from moonstreamdb.blockchain import AvailableBlockchainType, get_label_model
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from ..data import TokenURIs
from ..settings import VIEW_STATE_CRAWLER_LABEL, METADATA_CRAWLER_LABEL, CRAWLER_LABEL

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


def get_uris_of_tokens(
    db_session: Session, blockchain_type: AvailableBlockchainType
) -> List[TokenURIs]:
    """
    Get meatadata URIs.
    """

    label_model = get_label_model(blockchain_type)

    table = label_model.__tablename__

    metadata_for_parsing = db_session.execute(
        text(
            """ SELECT
            DISTINCT ON(label_data -> 'inputs'-> 0, address ) label_data -> 'inputs'-> 0 as token_id, address as address,
            label_data -> 'result' as token_uri,
            block_number as block_number,
            block_timestamp as block_timestamp
        FROM
            {}
        WHERE
            label = :label
            AND label_data ->> 'name' in :names
        ORDER BY
            label_data -> 'inputs'-> 0 ASC,
            address ASC,
            block_number :: INT DESC;
    """.format(
                table
            )
        ),
        {
            "table": table,
            "label": VIEW_STATE_CRAWLER_LABEL,
            "names": ("tokenURI", "uri"),
        },
    )

    results = [
        TokenURIs(
            token_id=data[0],
            address=data[1],
            token_uri=data[2][0],
            block_number=data[3],
            block_timestamp=data[4],
        )
        for data in metadata_for_parsing
        if data[1] is not None and len(data[1]) > 0
    ]

    return results


def get_current_metadata_for_address(
    db_session: Session, blockchain_type: AvailableBlockchainType, address: str
):
    """
    Get existing metadata.
    """

    label_model = get_label_model(blockchain_type)

    table = label_model.__tablename__

    current_metadata = db_session.execute(
        text(
            """ SELECT
            DISTINCT ON(label_data ->> 'token_id') label_data ->> 'token_id' as token_id
        FROM
            {}
        WHERE
            address = :address
            AND label = :label
        ORDER BY
            label_data ->> 'token_id' ASC,
            block_number :: INT DESC;
    """.format(
                table
            )
        ),
        {"address": address, "label": METADATA_CRAWLER_LABEL},
    )

    result = [data[0] for data in current_metadata]

    return result


def get_tokens_id_wich_may_updated(
    db_session: Session, blockchain_type: AvailableBlockchainType, address: str
):
    """
    Returns a list of tokens which may have updated information.

    This function queries the database and returns all tokens that have had a transaction executed
    on them after the latest update of their metadata, excluding transactions with names 'safeTransferFrom',
    'approve' and 'transferFrom'.

    TODO(Andrey): This function is not perfect, it may return tokens that have not been updated.
    One way for improvements it's get opcodes for all transactions and check if they update metadata storage.
    Required integration with entity API and opcodes crawler.
    """

    label_model = get_label_model(blockchain_type)

    table = label_model.__tablename__

    tokens = db_session.execute(
        text(
            """
        with token_id_latest_events as (
            SELECT
                DISTINCT ON (
                    label_data -> 'args' ->> 'tokenId',
                    label_data ->> 'name'
                ) label_data -> 'args' ->> 'tokenId' as token_id,
                label_data ->> 'name' as name,
                block_timestamp
            FROM
                {}
            where
                label = :moonworm_label
                and address = :address
                and label_data->> 'type' = 'tx_call'
                and label_data->>'status' = '1'
                and label_data ->> 'name' not in (
                        'safeTransferFrom',
                        'approve',
                        'transferFrom'
                    )
            ORDER BY
                (label_data -> 'args' ->> 'tokenId') ASC,
                (label_data ->> 'name') ASC,
                block_timestamp :: INT DESC,
                log_index :: INT DESC
        ),
        metadata_state as (
            SELECT
                DISTINCT ON(label_data ->> 'token_id') label_data ->> 'token_id' as token_id,
                block_timestamp
            FROM
                {}
            WHERE
                address = :address
                AND label = :metadata_label
            ORDER BY
                label_data ->> 'token_id' ASC,
                block_number :: INT DESC
        )
        SELECT
            distinct token_id_latest_events.token_id
        FROM
            token_id_latest_events
            JOIN metadata_state ON token_id_latest_events.token_id = metadata_state.token_id
        WHERE
            token_id_latest_events.block_timestamp > metadata_state.block_timestamp 
        """.format(
                table, table
            )
        ),
        {
            "address": address,
            "metadata_label": METADATA_CRAWLER_LABEL,
            "moonworm_label": CRAWLER_LABEL,
        },
    )

    result = [data[0] for data in tokens]

    return result


def clean_labels_from_db(
    db_session: Session, blockchain_type: AvailableBlockchainType, address: str
):
    """
    Remove existing labels.
    But keep the latest one for each token.
    """

    label_model = get_label_model(blockchain_type)

    table = label_model.__tablename__

    db_session.execute(
        text(
            """ 
        WITH lates_token_metadata AS (
            SELECT
                DISTINCT ON (label_data->>'token_id') label_data->>'token_id' AS token_id,
                id as id,
                block_number as block_number
            FROM
                {}
            WHERE
                label=:label
                AND address=:address
            ORDER BY
                label_data->>'token_id' ASC,
                block_number DESC
        )
        DELETE FROM
            {} USING lates_token_metadata
        WHERE
            label=:label
            AND address=:address
            AND {}.id  not in (select id from lates_token_metadata) RETURNING {}.block_number;
    """.format(
                table, table, table, table
            )
        ),
        {"address": address, "label": METADATA_CRAWLER_LABEL},
    )
