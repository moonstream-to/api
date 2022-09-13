import argparse
import json
import hashlib
import itertools
import logging
from typing import Dict, List, Any, Optional
from uuid import UUID

from moonstreamdb.blockchain import AvailableBlockchainType
from mooncrawl.moonworm_crawler.crawler import _retry_connect_web3
from moonstreamdb.db import (
    MOONSTREAM_DB_URI,
    MOONSTREAM_POOL_SIZE,
    create_moonstream_engine,
)
from sqlalchemy.orm import sessionmaker

from .db import view_call_to_label, commit_session, clean_labels
from .Multicall2_interface import Contract as Multicall2
from ..settings import (
    NB_CONTROLLER_ACCESS_ID,
    MOONSTREAM_STATE_CRAWLER_DB_STATEMENT_TIMEOUT_MILLIS,
    multicall_contracts,
)
from .web3_util import FunctionSignature

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


Multicall2_address = "0xc8E51042792d7405184DfCa245F2d27B94D013b6"


def make_multicall(
    multicall_method: Any,
    calls: List[Any],
    block_timestamp: int,
    block_number: str = "latest",
) -> Any:

    multicall_calls = [
        (
            call["address"],
            call["method"].encode_data(call["inputs"]).hex(),
        )
        for call in calls
    ]

    multicall_result = multicall_method(False, calls=multicall_calls).call(
        block_identifier=block_number
    )

    results = []

    # Handle the case with not successful calls
    for index, encoded_data in enumerate(multicall_result):
        if encoded_data[0]:
            results.append(
                {
                    "result": calls[index]["method"].decode_data(encoded_data[1])[0],
                    "hash": calls[index]["hash"],
                    "method": calls[index]["method"],
                    "address": calls[index]["address"],
                    "name": calls[index]["method"].name,
                    "inputs": calls[index]["inputs"],
                    "call_data": multicall_calls[index][1],
                    "block_number": block_number,
                    "block_timestamp": block_timestamp,
                    "status": encoded_data[0],
                }
            )
        else:
            results.append(
                {
                    "result": calls[index]["method"].decode_data(encoded_data[1]),
                    "hash": calls[index]["hash"],
                    "method": calls[index]["method"],
                    "address": calls[index]["address"],
                    "name": calls[index]["method"].name,
                    "inputs": calls[index]["inputs"],
                    "call_data": multicall_calls[index][1],
                    "block_number": block_number,
                    "block_timestamp": block_timestamp,
                    "status": encoded_data[0],
                }
            )
    return results


def crawl_calls_level(
    db_session,
    calls,
    responces,
    contracts_ABIs,
    interfaces,
    batch_size,
    multicall_method,
    block_number,
    blockchain_type,
    block_timestamp,
):

    calls_of_level = []

    for call in calls:
        parameters = []

        for input in call["inputs"]:

            if type(input["value"]) in (str, int):
                if input["value"] not in responces:
                    parameters.append([input["value"]])
                else:
                    if (
                        contracts_ABIs[call["address"]][input["value"]]["name"]
                        == "totalSupply"
                    ):
                        parameters.append(
                            list(range(1, responces[input["value"]][0] + 1))
                        )
                    else:
                        parameters.append(responces[input["value"]])
            elif type(input["value"]) == list:
                parameters.append(input["value"])
            else:
                raise

        for call_parameters in itertools.product(*parameters):
            calls_of_level.append(
                {
                    "address": call["address"],
                    "method": FunctionSignature(
                        interfaces[call["address"]].get_function_by_name(call["name"])
                    ),
                    "hash": call["generated_hash"],
                    "inputs": call_parameters,
                }
            )

    for call_chunk in [
        calls_of_level[i : i + batch_size]
        for i in range(0, len(calls_of_level), batch_size)
    ]:

        while True:
            try:
                make_multicall_result = make_multicall(
                    multicall_method=multicall_method,
                    calls=call_chunk,
                    block_number=block_number,
                    block_timestamp=block_timestamp,
                )
                break
            except ValueError:
                continue
        # results parsing and writing to database
        add_to_session_count = 0
        for result in make_multicall_result:

            db_view = view_call_to_label(blockchain_type, result)
            db_session.add(db_view)
            add_to_session_count += 1

            if result["hash"] not in responces:
                responces[result["hash"]] = []
            responces[result["hash"]].append(result["result"])
        commit_session(db_session)
        logger.info(f"{add_to_session_count} labels commit to database.")


def parse_jobs(
    jobs: List[Any],
    blockchain_type: AvailableBlockchainType,
    block_number: Optional[int],
    batch_size: int,
    access_id: UUID,
):
    """
    Parse jobs from list and generate web3 interfaces for each contract.
    """

    contracts_ABIs: Dict[str, Any] = {}
    contracts_methods: Dict[str, Any] = {}
    calls: Dict[int, Any] = {0: []}

    web3_client = _retry_connect_web3(
        blockchain_type=blockchain_type, access_id=access_id
    )

    logger.info(f"Crawler started connected to blockchain: {blockchain_type}")

    if block_number is None:
        block_number = web3_client.eth.get_block("latest").number  # type: ignore

    logger.info(f"Current block number: {block_number}")

    block_timestamp = web3_client.eth.get_block(block_number).timestamp  # type: ignore

    multicaller = Multicall2(
        web3_client, web3_client.toChecksumAddress(multicall_contracts[blockchain_type])
    )

    multicall_method = multicaller.tryAggregate

    def recursive_unpack(method_abi: Any, level: int = 0) -> Any:
        """
        Generate tree of calls for crawling
        """
        have_subcalls = False

        abi = {
            "inputs": [],
            "outputs": method_abi["outputs"],
            "name": method_abi["name"],
            "type": "function",
            "stateMutability": "view",
        }

        for input in method_abi["inputs"]:
            if type(input["value"]) in (str, int, list):

                abi["inputs"].append(input)

            elif type(input["value"]) == dict:
                if input["value"]["type"] == "function":
                    hash_link = recursive_unpack(input["value"], level + 1)
                    # replace defenition by hash pointing to the result of the recursive_unpack
                    input["value"] = hash_link
                    have_subcalls = True
                abi["inputs"].append(input)
        abi["address"] = method_abi["address"]
        generated_hash = hashlib.md5(json.dumps(abi).encode("utf-8")).hexdigest()

        abi["generated_hash"] = generated_hash
        if have_subcalls:
            level += 1
            if not calls.get(level):
                calls[level] = []
            calls[level].append(abi)
        else:

            level = 0

            if not calls.get(level):
                calls[level] = []
            calls[level].append(abi)

        if not contracts_methods.get(job["address"]):
            contracts_methods[job["address"]] = []
        if generated_hash not in contracts_methods[job["address"]]:
            contracts_methods[job["address"]].append(generated_hash)
            if not contracts_ABIs.get(job["address"]):
                contracts_ABIs[job["address"]] = {}
            contracts_ABIs[job["address"]][generated_hash] = abi

        return generated_hash

    for job in jobs:
        if job["address"] not in contracts_ABIs:
            contracts_ABIs[job["address"]] = []

        recursive_unpack(job, 0)

    # generate contracts interfaces

    interfaces = {}

    for contract_address in contracts_ABIs:

        # collect abis for each contract
        abis = []

        for method_hash in contracts_methods[contract_address]:
            abis.append(contracts_ABIs[contract_address][method_hash])

        # generate interface
        interfaces[contract_address] = web3_client.eth.contract(
            address=web3_client.toChecksumAddress(contract_address), abi=abis
        )

    responces: Dict[str, Any] = {}

    # reverse call_tree
    call_tree_levels = sorted(calls.keys(), reverse=True)[:-1]

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
        # initial call of level 0 all call without subcalls directly moved there
        logger.info("Crawl level: 0")
        logger.info(f"Jobs amount: {len(calls[0])}")

        crawl_calls_level(
            db_session,
            calls[0],
            responces,
            contracts_ABIs,
            interfaces,
            batch_size,
            multicall_method,
            block_number,
            blockchain_type,
            block_timestamp,
        )

        for level in call_tree_levels:

            logger.info(f"Crawl level: {level}")
            logger.info(f"Jobs amount: {len(calls[level])}")

            crawl_calls_level(
                db_session,
                calls[level],
                responces,
                contracts_ABIs,
                interfaces,
                batch_size,
                multicall_method,
                block_number,
                blockchain_type,
                block_timestamp,
            )

    finally:
        db_session.close()


def handle_crawl(args: argparse.Namespace) -> None:

    """
    Ability to track states of the contracts.

    Read all view methods of the contracts and crawl
    """

    my_job = {
        "type": "function",
        "stateMutability": "view",
        "inputs": [
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256",
                "value": {
                    "type": "function",
                    "name": "totalSupply",
                    "outputs": [
                        {
                            "internalType": "uint256",
                            "name": "",
                            "type": "uint256",
                        }
                    ],
                    "address": "0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
                    "inputs": [],
                },
            }
        ],
        "name": "tokenURI",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "address": "0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
    }

    blockchain_type = AvailableBlockchainType(args.blockchain)

    parse_jobs(
        [my_job], blockchain_type, args.block_number, args.batch_size, args.access_id
    )


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


def clean_labels_handler(args: argparse.Namespace) -> None:

    blockchain_type = AvailableBlockchainType(args.blockchain)

    web3_client = _retry_connect_web3(
        blockchain_type=blockchain_type, access_id=args.access_id
    )

    logger.info(f"Label cleaner connected to blockchain: {blockchain_type}")

    block_number = web3_client.eth.get_block("latest").number  # type: ignore

    engine = create_moonstream_engine(
        MOONSTREAM_DB_URI,
        pool_pre_ping=True,
        pool_size=MOONSTREAM_POOL_SIZE,
        statement_timeout=MOONSTREAM_STATE_CRAWLER_DB_STATEMENT_TIMEOUT_MILLIS,
    )
    process_session = sessionmaker(bind=engine)
    db_session = process_session()

    try:
        clean_labels(
            db_session, blockchain_type, args.block_number_cutoff, block_number
        )
    finally:
        db_session.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=lambda _: parser.print_help())

    parser.add_argument(
        "--access-id",
        default=NB_CONTROLLER_ACCESS_ID,
        type=UUID,
        help="User access ID",
    )

    subparsers = parser.add_subparsers()

    view_state_crawler_parser = subparsers.add_parser(
        "crawl-jobs",
        help="continuous crawling the view methods from job structure",  # TODO(ANDREY): move tasks to journal
    )
    view_state_crawler_parser.add_argument(
        "--blockchain",
        "-b",
        type=str,
        help="Type of blovkchain wich writng in database",
        required=True,
    )
    view_state_crawler_parser.add_argument(
        "--block-number", "-N", type=str, help="Block number."
    )
    view_state_crawler_parser.add_argument(
        "--batch-size",
        "-s",
        type=int,
        default=500,
        help="Size of chunks wich send to Multicall2 contract.",
    )
    view_state_crawler_parser.set_defaults(func=handle_crawl)

    view_state_cleaner = subparsers.add_parser(
        "clean-state-labels",
        help="Clean labels from database",
    )
    view_state_cleaner.add_argument(
        "--blockchain",
        "-b",
        type=str,
        help="Type of blovkchain wich writng in database",
        required=True,
    )
    view_state_cleaner.add_argument(
        "--blocks-cutoff",
        "-N",
        type=str,
        help="Amount blocks back after wich data will be remove.",
    )
    view_state_cleaner.set_defaults(func=clean_labels_handler)

    generate_view_parser = subparsers.add_parser(
        "parse-abi",
        help="Parse view methods from the abi file.",
    )

    generate_view_parser.add_argument(
        "--abi-file",
        "-a",
        type=str,
        help="Path to abi file.",
    )
    generate_view_parser.set_defaults(func=parse_abi)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
