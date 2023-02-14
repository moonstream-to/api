import argparse
from contextlib import contextmanager
import json
from urllib.error import HTTPError
import urllib.request
import logging
import random
from typing import Dict, Any, List, Optional

from moonstreamdb.blockchain import AvailableBlockchainType
from moonstreamdb.db import (
    MOONSTREAM_DB_URI,
    MOONSTREAM_POOL_SIZE,
    create_moonstream_engine,
    MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIS,
    MOONSTREAM_DB_URI_READ_ONLY,
)
from sqlalchemy.orm import sessionmaker
from .db import (
    get_uris_of_tokens,
    get_current_metadata_for_address,
    get_tokens_id_wich_may_updated,
    metadata_to_label,
    clean_labels_from_db,
)
from ..settings import (
    MOONSTREAM_STATE_CRAWLER_DB_STATEMENT_TIMEOUT_MILLIS,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


batch_size = 50


@contextmanager
def yield_session_maker(engine):
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def leak_of_crawled_uri(
    ids: List[Optional[str]], leak_rate: float, maybe_updated: List[Optional[str]]
) -> List[Optional[str]]:
    """
    Leak only uri which may be updated.
    """
    assert 0 <= leak_rate <= 1, "Leak rate must be between 0 and 1"

    result = []

    for id in ids:
        if id not in maybe_updated:
            result.append(id)
        elif random.random() > leak_rate:
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
    logger.info(f"Connecting to blockchain {blockchain_type.value}")

    engine = create_moonstream_engine(
        MOONSTREAM_DB_URI,
        pool_pre_ping=True,
        pool_size=MOONSTREAM_POOL_SIZE,
        statement_timeout=MOONSTREAM_STATE_CRAWLER_DB_STATEMENT_TIMEOUT_MILLIS,
    )
    process_session = sessionmaker(bind=engine)
    db_session = process_session()

    # run crawling of levels

    # create read only engine

    # Read only
    read_only_engine = create_moonstream_engine(
        url=MOONSTREAM_DB_URI_READ_ONLY,
        pool_size=MOONSTREAM_POOL_SIZE,
        statement_timeout=MOONSTREAM_DB_STATEMENT_TIMEOUT_MILLIS,
        pool_pre_ping=True,
    )

    with yield_session_maker(engine=read_only_engine) as db_session_read_only:
        try:
            # get all tokens with uri
            logger.info("Requesting all tokens with uri from database")
            uris_of_tokens = get_uris_of_tokens(db_session_read_only, blockchain_type)

            tokens_uri_by_address: Dict[str, Any] = {}

            for token_uri_data in uris_of_tokens:
                if token_uri_data.address not in tokens_uri_by_address:
                    tokens_uri_by_address[token_uri_data.address] = []
                tokens_uri_by_address[token_uri_data.address].append(token_uri_data)

            for address in tokens_uri_by_address:
                logger.info(f"Starting to crawl metadata for address: {address}")

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
                leak_rate = 0.0

                if len(maybe_updated) > 0:
                    leak_rate = max_recrawl / len(maybe_updated)

                    if leak_rate > 1:
                        leak_rate = 1

                parsed_with_leak = leak_of_crawled_uri(
                    already_parsed, leak_rate, maybe_updated
                )

                logger.info(
                    f"Leak rate: {leak_rate} for {address} with maybe updated {len(maybe_updated)}"
                )

                logger.info(f"Already parsed: {len(already_parsed)} for {address}")

                logger.info(
                    f"Amount of tokens for crawl: {len(tokens_uri_by_address[address])- len(parsed_with_leak)} for {address}"
                )

                # Remove already parsed tokens
                tokens_uri_by_address[address] = [
                    token_uri_data
                    for token_uri_data in tokens_uri_by_address[address]
                    if token_uri_data.token_id not in parsed_with_leak
                ]

                for requests_chunk in [
                    tokens_uri_by_address[address][i : i + batch_size]
                    for i in range(0, len(tokens_uri_by_address[address]), batch_size)
                ]:
                    writed_labels = 0
                    db_session.commit()

                    try:
                        with db_session.begin():
                            for token_uri_data in requests_chunk:
                                metadata = crawl_uri(token_uri_data.token_uri)

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
                        logger.error(err)
                        logger.error(
                            f"Error while writing labels for address: {address}"
                        )
                        db_session.rollback()

                clean_labels_from_db(
                    db_session=db_session,
                    blockchain_type=blockchain_type,
                    address=address,
                )

        finally:
            db_session.close()


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
