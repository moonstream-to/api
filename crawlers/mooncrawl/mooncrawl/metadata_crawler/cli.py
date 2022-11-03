import argparse
import json
from time import time, sleep
from urllib.error import HTTPError
import urllib.request
import logging
import requests
from typing import Any
from concurrent.futures import ThreadPoolExecutor

from moonstreamdb.blockchain import AvailableBlockchainType
from moonstreamdb.db import (
    MOONSTREAM_DB_URI,
    MOONSTREAM_POOL_SIZE,
    create_moonstream_engine,
)
from sqlalchemy.orm import sessionmaker
from .db import (
    commit_session,
    get_uri_addresses,
    get_not_updated_metadata_for_address,
    metadata_to_label,
    update_metadata,
)
from ..settings import (
    MOONSTREAM_METADATA_CRAWLER_THREADS,
    MOONSTREAM_STATE_CRAWLER_DB_STATEMENT_TIMEOUT_MILLIS,
)
from ..data import TokenURIs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


batch_size = 50


def crawl_uri(token_uri_data: TokenURIs) -> Any:

    """
    Get metadata from URI
    """
    retry = 0
    result = None
    while retry < 3:
        try:
            req = urllib.request.Request(
                token_uri_data.token_uri,
                None,
                {
                    "User-agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5"
                },
            )
            response = urllib.request.urlopen(req, timeout=5)

            if response.status == 200:
                result = json.loads(response.read())
                break
            retry += 1

        except HTTPError as error:
            logger.error(f"request end with error statuscode: {error.code}")
            logger.error(f"requested uri: {token_uri_data.token_uri}")
            retry += 1
            sleep(2)
            continue
        except Exception as err:
            logger.error(err)
            logger.error(f"requested uri: {token_uri_data.token_uri}")
            retry += 1
            sleep(2)
            continue
    sleep(0.5)
    return result, token_uri_data


def parse_metadata(blockchain_type: AvailableBlockchainType, batch_size: int):

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
    try:

        meradata_addresses = get_uri_addresses(db_session, blockchain_type)

        for address in meradata_addresses:

            not_updated_tokens = get_not_updated_metadata_for_address(
                db_session,
                blockchain_type,
                address=address,
            )

            logger.info(
                f"Start crawling {len(not_updated_tokens)} tokens of address {address}"
            )

            for requests_chunk in [
                not_updated_tokens[i : i + batch_size]
                for i in range(0, len(not_updated_tokens), batch_size)
            ]:
                writed_labels = 0

                with ThreadPoolExecutor(
                    max_workers=MOONSTREAM_METADATA_CRAWLER_THREADS
                ) as executor:

                    for result in executor.map(
                        crawl_uri, [request for request in requests_chunk]
                    ):

                        metadata = result[0]
                        token_uri_data = result[1]
                        label = metadata_to_label(
                            metadata=metadata,
                            blockchain_type=blockchain_type,
                            token_uri_data=token_uri_data,
                        )

                        if token_uri_data.metadata_id is None:

                            db_session.add(label)
                            writed_labels += 1
                            continue

                        update_metadata(
                            db_session,
                            blockchain_type,
                            token_uri_data.metadata_id,
                            label,
                        )
                        writed_labels += 1

                commit_session(db_session)
                logger.info(f"Write {writed_labels} labels for {address}")

    finally:
        db_session.close()


def handle_crawl(args: argparse.Namespace) -> None:

    """
    Parse all metadata of tokens.
    """

    blockchain_type = AvailableBlockchainType(args.blockchain)

    parse_metadata(blockchain_type, args.commit_batch_size)


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
    metadata_crawler_parser.set_defaults(func=handle_crawl)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
