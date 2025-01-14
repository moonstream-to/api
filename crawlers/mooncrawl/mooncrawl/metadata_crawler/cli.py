import argparse
import json
import logging
import random
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from sqlalchemy.orm import Session
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import HTTPError

from bugout.exceptions import BugoutResponseException
from moonstreamtypes.blockchain import AvailableBlockchainType
from moonstreamdb.blockchain import AvailableBlockchainType as AvailableBlockchainTypeV2


from ..actions import get_all_entries_from_search, request_connection_string
from ..settings import MOONSTREAM_ADMIN_ACCESS_TOKEN, MOONSTREAM_METADATA_TASKS_JOURNAL, MOONSTREAM_PUBLIC_QUERIES_DATA_ACCESS_TOKEN
from ..db import yield_db_preping_session_ctx, yield_db_read_only_preping_session_ctx, create_moonstream_engine, sessionmaker
from ..data import TokenURIs
from .db import (
    clean_labels_from_db,
    get_current_metadata_for_address,
    get_tokens_id_wich_may_updated,
    get_uris_of_tokens,
    metadata_to_label,
    get_tokens_to_crawl,
    upsert_metadata_labels,
)

from ..settings import moonstream_client as mc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


batch_size = 50


def leak_of_crawled_uri(
    ids: List[Optional[str]], leak_rate: float, maybe_updated: List[Optional[str]]
) -> List[Optional[str]]:
    """
    Leak only uri which may be updated.
    """
    assert 0 <= leak_rate <= 1, "Leak rate must be between 0 and 1"

    result = []

    for id in ids:
        if id not in maybe_updated and random.random() > leak_rate:
            result.append(id)

    return result


def crawl_uri(metadata_uri: str) -> Any:
    """
    Get metadata from URI
    """
    retry = 0
    result = None
    while retry < 3:
        try:
            if metadata_uri.startswith("ipfs://"):
                metadata_uri = metadata_uri.replace(
                    "ipfs://", "https://ipfs.io/ipfs/", 1
                )
            req = urllib.request.Request(
                metadata_uri, headers={"User-Agent": "Mozilla/5.0"}
            )

            response = urllib.request.urlopen(req, timeout=10)

            if metadata_uri.startswith("data:application/json") or response.status == 200:
                result = json.loads(response.read())
                break
            retry += 1

        except HTTPError as error:
            logger.error(f"request end with error statuscode: {error.code}")
            retry += 1
            if error.code == 404:
                return None
            continue
        except Exception as err:
            logger.error(err)
            logger.error(f"request end with error for url: {metadata_uri}")
            retry += 1
            continue
    return result


def process_address_metadata_with_leak(
    address: str,
    blockchain_type: AvailableBlockchainType,
    batch_size: int,
    max_recrawl: int,
    threads: int,
    tokens: List[TokenURIs],
) -> None:
    """
    Process metadata for a single address with v3 support
    """
    with yield_db_read_only_preping_session_ctx() as db_session_read_only:
        try:

            already_parsed = get_current_metadata_for_address(
                db_session=db_session_read_only,
                blockchain_type=blockchain_type,
                address=address,
            )

            maybe_updated = get_tokens_id_wich_may_updated(
                db_session=db_session_read_only,
                blockchain_type=blockchain_type,
                address=address,
            )
        except Exception as err:
            logger.warning(f"Error while getting metadata state for address {address}: {err}")
            return

    with yield_db_preping_session_ctx() as db_session:
        try:
            logger.info(f"Starting to crawl metadata for address: {address}")

            leak_rate = 0
            if len(maybe_updated) > 0:
                free_spots = len(maybe_updated) / max_recrawl
                if free_spots < 1:
                    leak_rate = 1 - (
                        len(already_parsed) - max_recrawl + len(maybe_updated)
                    ) / len(already_parsed)

            parsed_with_leak = leak_of_crawled_uri(
                already_parsed, leak_rate, maybe_updated
            )

            logger.info(
                f"Leak rate: {leak_rate} for {address} with maybe updated {len(maybe_updated)}"
            )
            logger.info(f"Already parsed: {len(already_parsed)} for {address}")
            logger.info(f"Amount of tokens to parse: {len(tokens)} for {address}")

            # Remove already parsed tokens
            new_tokens = [
                token for token in tokens
                if token.token_id not in parsed_with_leak
            ]

            for requests_chunk in [
                new_tokens[i : i + batch_size]
                for i in range(0, len(new_tokens), batch_size)
            ]:
                metadata_batch = []
                try:

                    # Gather all metadata in parallel
                    with ThreadPoolExecutor(max_workers=threads) as executor:
                        future_to_token = {
                            executor.submit(crawl_uri, token.token_uri): token
                            for token in requests_chunk
                        }
                        for future in as_completed(future_to_token):
                            token = future_to_token[future]
                            try:
                                metadata = future.result(timeout=10)
                                if metadata:
                                    metadata_batch.append((token, metadata))
                            except Exception as e:
                                logger.error(f"Error fetching metadata for token {token.token_id}: {e}")
                                continue

                    if metadata_batch:
                        # Batch upsert all metadata
                        upsert_metadata_labels(
                            db_session=db_session,
                            blockchain_type=blockchain_type,
                            metadata_batch=metadata_batch,
                            v3=False
                        )
                        
                        clean_labels_from_db(
                            db_session=db_session,
                            blockchain_type=blockchain_type,
                            address=address,
                        )
                        logger.info(f"Write {len(metadata_batch)} labels for {address}")

                except Exception as err:
                    logger.warning(f"Error while writing labels for address {address}: {err}")
                    db_session.rollback()

        except Exception as err:
            logger.warning(f"Error while crawling metadata for address {address}: {err}")
            db_session.rollback()



def process_address_metadata(
    address: str,
    blockchain_type: AvailableBlockchainType,
    db_session: Session,
    batch_size: int,
    max_recrawl: int,
    threads: int,
    tokens: List[TokenURIs],
) -> None:
    """
    Process metadata for a single address with v3 support
    Leak logic is implemented in sql statement
    """




    for requests_chunk in [
        tokens[i : i + batch_size]
        for i in range(0, len(tokens), batch_size)
    ]:
        metadata_batch = []
        with ThreadPoolExecutor(max_workers=threads) as executor:
            future_to_token = {
                executor.submit(crawl_uri, token.token_uri): token
                for token in requests_chunk
            }
            for future in as_completed(future_to_token):
                token = future_to_token[future]
                metadata = future.result(timeout=10)
                metadata_batch.append((token, metadata))


        upsert_metadata_labels(
            db_session=db_session,
            blockchain_type=blockchain_type,
            metadata_batch=metadata_batch,
            v3=True
        )

        db_session.commit()

        clean_labels_from_db(
            db_session=db_session,
            blockchain_type=blockchain_type,
            address=address,
            version=3
        )

        db_session.commit()



    

def parse_metadata(
    blockchain_type: AvailableBlockchainType,
    batch_size: int,
    max_recrawl: int,
    threads: int,
    custom_db_uri: Optional[str] = None,
):
    """
    Parse all metadata of tokens.
    """
    logger.info("Starting metadata crawler")
    logger.info(f"Processing blockchain {blockchain_type.value}")

    # Check if blockchain exists in v2 package
    if blockchain_type.value in [chain.value for chain in AvailableBlockchainTypeV2]:
        try:
            logger.info(f"Processing v2 blockchain: {blockchain_type.value}")
            # Get tokens to crawl v2 flow
            with yield_db_read_only_preping_session_ctx() as db_session_read_only:
                tokens_uri_by_address = get_tokens_to_crawl(
                    db_session_read_only,
                    blockchain_type,
                    {},
                )

            # Process each address
            for address, tokens in tokens_uri_by_address.items():
                process_address_metadata_with_leak(
                    address=address,
                    blockchain_type=blockchain_type,
                    batch_size=batch_size,
                    max_recrawl=max_recrawl,
                    threads=threads,
                    tokens=tokens,
                )
        except Exception as err:
            logger.error(f"V2 flow failed: {err}, continuing with Spire flow")

    # Continue with Spire flow regardless of v2 result
    spire_jobs = []

    # Get all jobs for this blockchain from Spire
    search_query = f"#metadata-job #{blockchain_type.value}"
    try:
        entries = get_all_entries_from_search(
            journal_id=MOONSTREAM_METADATA_TASKS_JOURNAL,
            search_query=search_query,
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            content=True,
            limit=1000,
        )
        
        logger.info(f"Found {len(entries)} metadata jobs for blockchain {blockchain_type.value}")
        
        for entry in entries:
            try:
                if not entry.content:
                    continue
                
                job = json.loads(entry.content)
                if job.get("blockchain") != blockchain_type.value:
                    logger.warning(f"Skipping job with mismatched blockchain: {job.get('blockchain')} != {blockchain_type.value}")
                    continue
                spire_jobs.append(job)
            except Exception as err:
                id = entry.entry_url.split("/")[-1]
                logger.error(f"Error parsing job from entry {id}: {err}")
                continue
    except BugoutResponseException as err:
        logger.error(f"Bugout error fetching jobs from journal: {err.detail}")
    except Exception as err:
        logger.error(f"Error fetching jobs from journal: {err}")
        return

    # Process each job

    # sessions list for each customer and instance
    sessions_by_customer: Dict[Tuple[str, str], Session] = {}

    # all sessions in one try block
    try: 
        for job in spire_jobs:
            try:
                customer_id = job.get("customer_id")
                instance_id = job.get("instance_id")

                if (customer_id, instance_id) not in sessions_by_customer:
                    # Create session
                    # Assume fetch_connection_string fetches the connection string
                    if custom_db_uri:
                        connection_string = custom_db_uri
                    else:
                        connection_string = request_connection_string(
                            customer_id=customer_id,
                            instance_id=instance_id,
                            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                        )
                    engine = create_moonstream_engine(connection_string, 2, 100000)
                    session = sessionmaker(bind=engine)
                    try:
                        sessions_by_customer[(customer_id, instance_id)] = session()
                    except Exception as e:
                        logger.error(f"Connection to {engine} failed: {e}")
                        continue

                
                # Get tokens to crawl
                tokens_uri_by_address = get_tokens_to_crawl(
                    sessions_by_customer[(customer_id, instance_id)],
                    blockchain_type,
                    job,
                ) 

                for address, tokens in tokens_uri_by_address.items():
                    process_address_metadata(
                        address=address,
                        blockchain_type=blockchain_type,
                        db_session=sessions_by_customer[(customer_id, instance_id)],
                        batch_size=batch_size,
                        max_recrawl=max_recrawl,
                        threads=threads,
                        tokens=tokens,
                    )
            except Exception as err:
                logger.error(f"Error processing job: {err}")
                continue
    except Exception as err:
        logger.error(f"Error processing jobs: {err}")
        raise err
     
    finally:
        for session in sessions_by_customer.values():
            try:
                session.close()
            except Exception as err:
                logger.error(f"Error closing session: {err}")


def handle_crawl(args: argparse.Namespace) -> None:
    """
    Parse all metadata of tokens.
    """
    blockchain_type = AvailableBlockchainType(args.blockchain)
    parse_metadata(
        blockchain_type,
        args.commit_batch_size,
        args.max_recrawl,
        args.threads,
        args.custom_db_uri,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=lambda _: parser.print_help())

    subparsers = parser.add_subparsers()

    metadata_crawler_parser = subparsers.add_parser(
        "crawl",
        help="Crawler of tokens metadata.",
    )
    metadata_crawler_parser.add_argument(
        "--blockchain",
        "-b",
        type=str,
        help="Type of blockchain which writing in database",
        required=True,
    )
    metadata_crawler_parser.add_argument(
        "--commit-batch-size",
        "-c",
        type=int,
        default=50,
        help="Amount of requests before commiting to database",
    )
    metadata_crawler_parser.add_argument(
        "--max-recrawl",
        "-m",
        type=int,
        default=300,
        help="Maximum amount of recrawling of already crawled tokens",
    )
    metadata_crawler_parser.add_argument(
        "--threads",
        "-t",
        type=int,
        default=4,
        help="Amount of threads for crawling",
    )
    metadata_crawler_parser.add_argument(
        "--custom-db-uri",
        type=str,
        help="Custom db uri to use for crawling",
    )
    metadata_crawler_parser.set_defaults(func=handle_crawl)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
