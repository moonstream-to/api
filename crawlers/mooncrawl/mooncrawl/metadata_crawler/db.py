import json
import logging
from hexbytes import HexBytes
from typing import Any, Dict, List, Optional, Tuple
###from sqlalchemy import 
from sqlalchemy.dialects.postgresql import insert

from datetime import datetime

##from moonstreamdb.blockchain import AvailableBlockchainType, get_label_model
from moonstreamtypes.blockchain import AvailableBlockchainType, get_label_model
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from ..actions import recive_S3_data_from_query
from ..data import TokenURIs
from ..settings import (
    CRAWLER_LABEL,
    METADATA_CRAWLER_LABEL,
    VIEW_STATE_CRAWLER_LABEL,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    bugout_client as bc,
    moonstream_client as mc,
)
from moonstream.client import Moonstream  # type: ignore


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def metadata_to_label(
    blockchain_type: AvailableBlockchainType,
    metadata: Optional[Dict[str, Any]],
    token_uri_data: TokenURIs,
    label_name=METADATA_CRAWLER_LABEL,
    v3: bool = False,
):
    """
    Creates a label model with support for v2 and v3 database structures.
    """
    version = 3 if v3 else 2
    label_model = get_label_model(blockchain_type, version=version)

    sanityzed_label_data = json.loads(
        json.dumps(
            {
                "type": "metadata",
                "token_id": token_uri_data.token_id,
                "metadata": metadata,
            }
        ).replace(r"\u0000", "")
    )

    if v3:
        # V3 structure similar to state crawler
        label_data = {
            "token_id": token_uri_data.token_id,
            "metadata": metadata,
        }

        label = label_model(
            label=label_name,
            label_name="metadata",  # Fixed name for metadata labels
            label_type="metadata",
            label_data=label_data,
            address=HexBytes(token_uri_data.address),
            block_number=token_uri_data.block_number,
            # Use a fixed tx hash for metadata since it's not from a transaction
            block_timestamp=token_uri_data.block_timestamp,
            block_hash=token_uri_data.block_hash if hasattr(token_uri_data, 'block_hash') else None,
        )
    else:
        # Original v2 structure
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
    db_session: Session, blockchain_type: AvailableBlockchainType, version: int = 2
) -> List[TokenURIs]:
    """
    Get meatadata URIs.
    """

    label_model = get_label_model(blockchain_type, version=version)

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
    db_session: Session, blockchain_type: AvailableBlockchainType, address: str, version: int = 2
):
    """
    Get existing metadata.
    """

    label_model = get_label_model(blockchain_type, version=version)

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
            AND label_data ->>'metadata' != 'null'
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
    db_session: Session, blockchain_type: AvailableBlockchainType, address: str, version: int = 2
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

    label_model = get_label_model(blockchain_type, version=version)

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


def get_tokens_from_query_api(
    client: Moonstream,
    query_name: str,
    params: dict,
    token: str,
) -> List[TokenURIs]:
    """
    Get token URIs from Query API results
    """
    try:
        data = recive_S3_data_from_query(
            client=client,
            token=token,
            query_name=query_name,
            params=params,
        )
        
        # Convert query results to TokenURIs format
        results = []
        for item in data.get("data", []):
            results.append(
                TokenURIs(
                    token_id=str(item.get("token_id")),
                    address=item.get("address"),
                    token_uri=item.get("token_uri"),
                    block_number=item.get("block_number"),
                    block_timestamp=item.get("block_timestamp"),
                )
            )
        return results
    except Exception as err:
        logger.error(f"Error fetching data from Query API: {err}")
        return []

def get_tokens_to_crawl(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    spire_job: Optional[dict] = None,
) -> Dict[str, List[TokenURIs]]:
    """`
    Get tokens to crawl either from Query API (if specified in Spire job) or database
    """
    tokens_uri_by_address = {}

    if spire_job:
        if "query_api" not in spire_job:
            raise ValueError("Query API is not specified in Spire job")

        # Get tokens from Query API
        query_config = spire_job["query_api"]
        client = Moonstream()
        
        tokens = get_tokens_from_query_api(
            client=client,
            query_name=query_config["name"],
            params=query_config["params"],
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        )
        
        # Group by address
        for token in tokens:
            if token.address not in tokens_uri_by_address:
                tokens_uri_by_address[token.address] = []
            tokens_uri_by_address[token.address].append(token)
    else:
        # Get tokens from database (existing logic)
        uris_of_tokens = get_uris_of_tokens(db_session, blockchain_type)
        for token_uri_data in uris_of_tokens:
            if token_uri_data.address not in tokens_uri_by_address:
                tokens_uri_by_address[token_uri_data.address] = []
            tokens_uri_by_address[token_uri_data.address].append(token_uri_data)

    return tokens_uri_by_address

def upsert_metadata_labels(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    metadata_batch: List[Tuple[TokenURIs, Optional[Dict[str, Any]]]],
    v3: bool = False,
    db_batch_size: int = 100,

) -> None:
    """
    Batch upsert metadata labels - update if exists, insert if not.
    """
    try:
        version = 3 if v3 else 2
        label_model = get_label_model(blockchain_type, version=version)

        
        # Prepare batch of labels
        labels_data = []
        for token_uri_data, metadata in metadata_batch:

            if v3:
                # V3 structure
                label_data = {
                    "token_id": token_uri_data.token_id,
                    "metadata": metadata,
                }
                
                labels_data.append({
                    "label": METADATA_CRAWLER_LABEL,
                    "label_name": "metadata",
                    "label_type": "metadata",
                    "label_data": label_data,
                    "address": HexBytes(token_uri_data.address),
                    "block_number": token_uri_data.block_number,
                    "block_timestamp": token_uri_data.block_timestamp,
                    "block_hash": getattr(token_uri_data, 'block_hash', None),
                })
            else:
                # V2 structure
                label_data = {
                    "type": "metadata",
                    "token_id": token_uri_data.token_id,
                    "metadata": metadata,
                }
                
                labels_data.append({
                    "label": METADATA_CRAWLER_LABEL,
                    "label_data": label_data,
                    "address": token_uri_data.address,
                    "block_number": token_uri_data.block_number,
                    "transaction_hash": None,
                    "block_timestamp": token_uri_data.block_timestamp,
                })

        if not labels_data:
            return

        # Create insert statement
        insert_stmt = insert(label_model).values(labels_data)
        result_stmt = insert_stmt.on_conflict_do_nothing(
        )

        db_session.execute(result_stmt)

    except Exception as err:
        logger.error(f"Error batch upserting metadata labels: {err}")
        raise