import argparse
import json
import logging
import random
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError

from moonstreamdb.blockchain import AvailableBlockchainType

from ..actions import get_all_entries_from_search
from ..settings import MOONSTREAM_ADMIN_ACCESS_TOKEN
from ..db import yield_db_preping_session_ctx, yield_db_read_only_preping_session_ctx
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
            continue
        except Exception as err:
            logger.error(err)
            logger.error(f"request end with error for url: {metadata_uri}")
            retry += 1
            continue
    return result


def process_address_metadata(
    address: str,
    blockchain_type: AvailableBlockchainType,
    batch_size: int,
    max_recrawl: int,
    threads: int,
    job: Optional[dict],
    tokens: List[TokenURIs],
) -> None:
    """
    Process metadata for a single address with v3 support
    """
    with yield_db_read_only_preping_session_ctx() as db_session_read_only:
        try:
            ##  

            already_parsed = get_current_metadata_for_address(
                db_session=db_session_read_only,
                blockchain_type=blockchain_type,
                address=address,
            )


            ### Do we need this?
            ### Can we move it to sql query?
            ### Do we need to get all tokens?
            

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

            # Determine if this is a v3 job
            v3 = job.get("v3", False) if job else False
            
            # Determine leak rate based on job config or default behavior
            leak_rate = 0.0
            update_existing = job.get("update_existing", False) if job else False

            if len(maybe_updated) > 0:
                free_spots = len(maybe_updated) / max_recrawl
                if free_spots > 1:
                    leak_rate = 0
                else:
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
                    with db_session.begin():
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
                                v3=v3,
                                update_existing=update_existing
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


def parse_metadata(
    blockchain_type: AvailableBlockchainType,
    batch_size: int,
    max_recrawl: int,
    threads: int,
    metadata_journal_id: Optional[str] = None,
):
    """
    Parse all metadata of tokens.
    """
    logger.info("Starting metadata crawler")
    logger.info(f"Processing blockchain {blockchain_type.value}")

    spire_jobs = []
    if metadata_journal_id:
        # Get all jobs for this blockchain from Spire
        search_query = f"#metadata-job #{blockchain_type.value}"
        try:
            entries = get_all_entries_from_search(
                journal_id=metadata_journal_id,
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
        except Exception as err:
            logger.error(f"Error fetching jobs from journal: {err}")
            return

    # Process each job
    for job in spire_jobs or [None]:  # If no jobs, run once with None
        try:
            # Get tokens to crawl
            with yield_db_read_only_preping_session_ctx() as db_session_read_only:
                tokens_uri_by_address = get_tokens_to_crawl(
                    db_session_read_only,
                    blockchain_type,
                    job,
                )

            # Process each address
            for address, tokens in tokens_uri_by_address.items():
                process_address_metadata(
                    address=address,
                    blockchain_type=blockchain_type,
                    batch_size=batch_size,
                    max_recrawl=max_recrawl,
                    threads=threads,
                    job=job,
                    tokens=tokens,
                )

        except Exception as err:
            logger.error(f"Error processing job: {err}")
            continue


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
        args.metadata_journal_id,
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
        "--metadata-journal-id",
        type=str,
        help="Optional Spire journal ID containing metadata jobs",
    )
    metadata_crawler_parser.set_defaults(func=handle_crawl)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
