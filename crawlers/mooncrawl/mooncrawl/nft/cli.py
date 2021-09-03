"""
A command line tool to crawl information about NFTs from various sources.
"""
import argparse
from typing import cast

from web3 import Web3

from ..ethereum import connect
from .ethereum import get_nft_transfers
from ..settings import MOONSTREAM_IPC_PATH


def web3_client_from_cli_or_env(args: argparse.Namespace) -> Web3:
    """
    Returns a web3 client either by parsing "--web3" argument on the given arguments or by looking up
    the MOONSTREAM_IPC_PATH environment variable.
    """
    web3_connection_string = MOONSTREAM_IPC_PATH
    args_web3 = vars(args).get("web3")
    if args_web3 is not None:
        web3_connection_string = cast(str, args_web3)
    if web3_connection_string is None:
        raise ValueError(
            "Could not find Web3 connection information in arguments or in MOONSTREAM_IPC_PATH environment variable"
        )
    return connect(web3_connection_string)


def ethereum_handler(args: argparse.Namespace) -> None:
    web3_client = web3_client_from_cli_or_env(args)
    transfers = get_nft_transfers(web3_client, args.start, args.end, args.address)
    for transfer in transfers:
        print(transfer)

    print("Total transfers:", len(transfers))
    print("Mints:", len([transfer for transfer in transfers if transfer.is_mint]))


def main() -> None:
    parser = argparse.ArgumentParser(description="Moonstream NFT crawlers")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Subcommands")

    parser_ethereum = subcommands.add_parser(
        "ethereum",
        description="Collect information about NFTs from Ethereum blockchains",
    )
    parser_ethereum.add_argument(
        "-s",
        "--start",
        type=int,
        default=None,
        help="Starting block number (inclusive if block available)",
    )
    parser_ethereum.add_argument(
        "-e",
        "--end",
        type=int,
        default=None,
        help="Ending block number (inclusive if block available)",
    )
    parser_ethereum.add_argument(
        "-a",
        "--address",
        type=str,
        default=None,
        help="(Optional) NFT contract address that you want to limit the crawl to, e.g. 0x06012c8cf97BEaD5deAe237070F9587f8E7A266d for CryptoKitties.",
    )
    parser_ethereum.add_argument(
        "--web3",
        type=str,
        default=None,
        help="(Optional) Web3 connection string. If not provided, uses the value specified by MOONSTREAM_IPC_PATH environment variable.",
    )
    parser_ethereum.set_defaults(func=ethereum_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
