import argparse
import json
import logging
import random
import urllib.request
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError

from moonstreamdb.blockchain import AvailableBlockchainType
from sqlalchemy.orm import sessionmaker

from ..db import (
    yield_db_preping_session_ctx,
    yield_db_read_only_preping_session_ctx,
)
from ..settings import MOONSTREAM_CRAWLERS_DB_STATEMENT_TIMEOUT_MILLIS
from .db import (
    clean_labels_from_db,
    get_current_metadata_for_address,
    get_tokens_id_wich_may_updated,
    get_uris_of_tokens,
    metadata_to_label,
)

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
            response = urllib.request.urlopen(metadata_uri, timeout=10)

            if response.status == 200:
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


def parse_metadata(
    blockchain_type: AvailableBlockchainType, batch_size: int, max_recrawl: int
):
    """
    Parse all metadata of tokens.
    """

    logger.info("Starting metadata crawler")
    logger.info(f"Processing blockchain {blockchain_type.value}")

    # run crawling of levels
    with yield_db_read_only_preping_session_ctx() as db_session_read_only:
        try:
            # get all tokens with uri
            logger.info("Requesting all tokens with uri from database")
            uris_of_tokens = get_uris_of_tokens(db_session_read_only, blockchain_type)

            tokens_uri_by_address: Dict[str, Any] = {}

            for token_uri_data in uris_of_tokens:
                if token_uri_data.address not in tokens_uri_by_address:
                    tokens_uri_by_address[token_uri_data.address] = []
                tokens_uri_by_address[token_uri_data.address].append(token_uri_data)

        except Exception as err:
            logger.error(f"Error while requesting tokens with uri from database: {err}")
            return

    for address in tokens_uri_by_address:
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
                logger.warning(err)
                logger.warning(
                    f"Error while requesting metadata for address: {address}"
                )
                continue

        with yield_db_preping_session_ctx() as db_session:
            try:
                logger.info(f"Starting to crawl metadata for address: {address}")

                leak_rate = 0.0

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

                logger.info(
                    f"Amount of state in database: {len(tokens_uri_by_address[address])} for {address}"
                )

                logger.info(
                    f"Amount of tokens parsed with leak: {len(parsed_with_leak)} for {address}"
                )

                # Remove already parsed tokens
                new_tokens_uri_by_address = [
                    token_uri_data
                    for token_uri_data in tokens_uri_by_address[address]
                    if token_uri_data.token_id not in parsed_with_leak
                ]

                logger.info(
                    f"Amount of tokens to parse: {len(new_tokens_uri_by_address)} for {address}"
                )

                for requests_chunk in [
                    new_tokens_uri_by_address[i : i + batch_size]
                    for i in range(0, len(new_tokens_uri_by_address), batch_size)
                ]:
                    writed_labels = 0
                    db_session.commit()

                    try:
                        with db_session.begin():
                            for token_uri_data in requests_chunk:
                                with ThreadPoolExecutor(max_workers=1) as executor:
                                    future = executor.submit(
                                        crawl_uri, token_uri_data.token_uri
                                    )
                                    metadata = future.result(timeout=10)
                                db_session.add(
                                    metadata_to_label(
                                        blockchain_type=blockchain_type,
                                        metadata=metadata,
                                        token_uri_data=token_uri_data,
                                    )
                                )
                                writed_labels += 1

                            if writed_labels > 0:
                                clean_labels_from_db(
                                    db_session=db_session,
                                    blockchain_type=blockchain_type,
                                    address=address,
                                )
                                logger.info(
                                    f"Write {writed_labels} labels for {address}"
                                )
                        # trasaction is commited here
                    except Exception as err:
                        logger.warning(err)
                        logger.warning(
                            f"Error while writing labels for address: {address}"
                        )
                        db_session.rollback()

                clean_labels_from_db(
                    db_session=db_session,
                    blockchain_type=blockchain_type,
                    address=address,
                )
            except Exception as err:
                logger.warning(err)
                logger.warning(f"Error while crawling metadata for address: {address}")
                db_session.rollback()
                continue


def handle_crawl(args: argparse.Namespace) -> None:
    """
    Parse all metadata of tokens.
    """

    blockchain_type = AvailableBlockchainType(args.blockchain)

    parse_metadata(blockchain_type, args.commit_batch_size, args.max_recrawl)


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
        help="Type of blockchain wich writng in database",
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
    metadata_crawler_parser.set_defaults(func=handle_crawl)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
