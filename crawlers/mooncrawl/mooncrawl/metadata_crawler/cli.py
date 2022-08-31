import argparse
import json
import hashlib
import itertools
from pickle import TRUE
from pprint import pprint
import logging
from random import random
import requests
from typing import Dict, List, Any
from uuid import UUID

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


def crawl_uri(metadata_uri: str) -> Dict[str, Any]:

    """
    Get metadata from URI
    """
    retry = 0
    result = None
    while retry < 3:
        try:
            metadata = requests.get(metadata_uri)
            if metadata.status_code == 200:
                result = metadata.data
                break
            retry += 1
        except Exception as err:
            print(err)
            retry += 1
            continue
    return result


def parse_metadata(jobs, blockchain_type, block_number):

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

            for token_uri_data in tokens_uri_by_address[address]:

                if token_uri_data.token_id not in already_parsed:
                    metadata = crawl_uri(token_uri_data)

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

    parse_metadata(blockchain_type)


def parse_abi(args: argparse.Namespace) -> None:
    """
    Parse the abi of the contract and save it to the database.
    """

    with open(args.abi_file, "r") as f:
        # read json and parse only stateMutability equal to view
        abi = json.load(f)

    output_json = []

    for method in abi:
        if method.get("stateMutability") and method["stateMutability"] == "view":
            output_json.append(method)

    with open(f"view+{args.abi_file}", "w") as f:
        json.dump(output_json, f)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=lambda _: parser.print_help())

    subparsers = parser.add_subparsers()

    metadata_crawler_parser = subparsers.add_parser(
        "crawl",
        help="continuous crawling the event/function call jobs from bugout journal",
    )
    metadata_crawler_parser.add_argument(
        "--blockchain-type",
        "-b",
        type=str,
        help="Type of blovkchain wich writng in database",
        required=True,
    )
    metadata_crawler_parser.set_defaults(func=handle_crawl)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
