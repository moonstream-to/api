import argparse
import json
from urllib.error import HTTPError
import urllib.request
import logging
from typing import Dict, Any

from moonstreamdb.blockchain import AvailableBlockchainType
from moonstreamdb.db import (
    MOONSTREAM_DB_URI_READ_ONLY,
    MOONSTREAM_POOL_SIZE,
    create_moonstream_engine,
)
from sqlalchemy.orm import sessionmaker
from .db import (
    commit_session,
    get_uris_of_tokens,
    get_current_metadata_for_address,
    metadata_to_label,
)
from ..settings import (
    MOONSTREAM_STATE_CRAWLER_DB_STATEMENT_TIMEOUT_MILLIS,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


batch_size = 50


def crawl_uri(metadata_uri: str) -> Dict[str, Any]:

    """
    Get metadata from URI
    """
    retry = 0
    result = None
    while retry < 3:
        try:

            response = urllib.request.urlopen(metadata_uri, timeout=5)

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
            retry += 1
            continue
    return result


def parse_metadata(blockchain_type: AvailableBlockchainType, batch_size: int):

    engine = create_moonstream_engine(
        MOONSTREAM_DB_URI_READ_ONLY,
        pool_pre_ping=True,
        pool_size=MOONSTREAM_POOL_SIZE,
        statement_timeout=MOONSTREAM_STATE_CRAWLER_DB_STATEMENT_TIMEOUT_MILLIS,
    )
    process_session = sessionmaker(bind=engine)
    db_session = process_session()

    # run crawling of levels
    try:

        uris_of_tokens = get_uris_of_tokens(db_session, blockchain_type)

        tokens_uri_by_address = {}

        for token_uri_data in uris_of_tokens:
            if token_uri_data.address not in tokens_uri_by_address:
                tokens_uri_by_address[token_uri_data.address] = []
            tokens_uri_by_address[token_uri_data.address].append(token_uri_data)

        for address in tokens_uri_by_address:

            already_parsed = get_current_metadata_for_address(
                db_session=db_session, blockchain_type=blockchain_type, address=address
            )

            for requests_chunk in [
                tokens_uri_by_address[address][i : i + batch_size]
                for i in range(0, len(tokens_uri_by_address[address]), batch_size)
            ]:

                for token_uri_data in requests_chunk:

                    if token_uri_data.token_id not in already_parsed:
                        metadata = crawl_uri(token_uri_data.token_uri)

                        db_session.add(
                            metadata_to_label(
                                blockchain_type=blockchain_type,
                                metadata=metadata,
                                token_uri_data=token_uri_data,
                            )
                        )
                commit_session(db_session)

    finally:
        db_session.close()


def handle_crawl(args: argparse.Namespace) -> None:

    """
    Parse all metadata of tokens.
    """

    blockchain_type = AvailableBlockchainType(args.blockchain_type)

    parse_metadata(blockchain_type, args.batch_size)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=lambda _: parser.print_help())

    subparsers = parser.add_subparsers()

    metadata_crawler_parser = subparsers.add_parser(
        "crawl",
        help="Crawler of tokens metadata.",
    )
    metadata_crawler_parser.add_argument(
        "--blockchain-type",
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
