import argparse
import json
import os
import time

import requests

from moonstreamdb.db import yield_db_session_ctx
from moonstreamdb.models import EthereumAddress

COINMARKETCAP_API_KEY = os.environ.get("COINMARKETCAP_API_KEY")
if COINMARKETCAP_API_KEY is None:
    raise ValueError("COINMARKETCAP_API_KEY environment variable must be set")

CRAWL_ORIGINS = {
    "pro": "https://pro-api.coinmarketcap.com",
    "sandbox": "https://sandbox-api.coinmarketcap.com",
}


def identities_cmc_handler(args: argparse.Namespace) -> None:
    """
    Parse metadata for Ethereum tokens.
    """
    headers = {
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY,
        "Accept": "application/json",
        "Accept-Encoding": "deflate, gzip",
    }
    if args.sandbox:
        CRAWL_ORIGIN = CRAWL_ORIGINS["sandbox"]
    else:
        CRAWL_ORIGIN = CRAWL_ORIGINS["pro"]
    url = f"{CRAWL_ORIGIN}/v1/cryptocurrency/map"

    start_n = 1
    limit_n = 5000

    while True:
        params = {"start": start_n, "limit": limit_n}
        try:
            r = requests.get(url=url, headers=headers, params=params)
            r.raise_for_status()
            response = r.json()
        except Exception as err:
            raise Exception(err)

        if len(response["data"]) == 0:
            print("No more data, crawling finished")
            break

        with yield_db_session_ctx() as db_session:
            for crypto in response["data"]:
                if crypto["platform"] is not None:
                    if (
                        crypto["platform"]["id"] == 1027
                        and crypto["platform"]["token_address"] is not None
                    ):

                        eth_token = EthereumAddress(
                            address=crypto["platform"]["token_address"],
                            name=crypto["name"],
                            symbol=crypto["symbol"],
                        )
                        db_session.add(eth_token)
                        print(f"Added {crypto['name']} token")

            db_session.commit()
        start_n += limit_n

        print(f"Loop ended, starting new from {start_n} to {start_n + limit_n - 1}")
        time.sleep(1)


def main():
    parser = argparse.ArgumentParser(description="Crawls address identities CLI")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Crawlers commands")

    parser_cmc = subcommands.add_parser("cmc", description="Coinmarketcap commands")
    parser_cmc.set_defaults(func=lambda _: parser_cmc.print_help())
    subcommands_parser_cmc = parser_cmc.add_subparsers(
        description="Ethereum blocks commands"
    )
    parser_cmc.add_argument(
        "-s",
        "--sandbox",
        action="store_true",
        help="Target to sandbox API",
    )
    parser_cmc.set_defaults(func=identities_cmc_handler)

    parser_label_cloud = subcommands.add_parser(
        "label_cloud", description="Etherscan label cloud commands"
    )
    parser_label_cloud.set_defaults(func=identities_get_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
