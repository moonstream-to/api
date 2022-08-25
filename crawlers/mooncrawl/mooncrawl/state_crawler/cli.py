import argparse
import json
import hashlib
import itertools
from pprint import pprint
import logging
from random import random
from typing import Optional, List, Any, Union, Dict, Tuple, Callable, Iterable, cast
from uuid import UUID

from moonstreamdb.blockchain import AvailableBlockchainType
from moonstreamdb.db import yield_db_session_ctx
import web3
from web3 import Web3
from web3.middleware import geth_poa_middleware

from ..settings import MOONSTREAM_MOONWORM_TASKS_JOURNAL, NB_CONTROLLER_ACCESS_ID
from .db import get_first_labeled_block_number, get_last_labeled_block_number
from .historical_crawler import historical_crawler
from brownie import Contract, network, chain
import Multicall2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


Multicall2_address = "0xc8E51042792d7405184DfCa245F2d27B94D013b6"


def make_multicall(
    multicall_method: Any,
    calls: List[Any],
    block_number: str = "latest",
) -> Any:
    # print("calls")
    # pprint(calls)
    multicall_result = multicall_method.call(
        False,  # success not required
        [
            (
                call["address"],
                call["method"].encode_input(*call["inputs"]),
            )
            for call in calls
        ],
        block_identifier=block_number,
    )

    results = []

    # Handle the case with not successful calls
    for index, encoded_data in enumerate(multicall_result):
        if encoded_data[0]:
            # print(dir(calls[index]["method"]))
            results.append(
                {
                    "result": calls[index]["method"].decode_output(encoded_data[1]),
                    "hash": calls[index]["hash"],
                    "address": calls[index]["address"],
                    "name": calls[index]["method"]._name,
                    "inputs": calls[index]["inputs"],
                    "block_number": block_number,
                }
            )
        else:
            # print(encoded_data)
            results.append(
                {
                    "result": None,  # calls[index]["method"].decode_output(encoded_data[1]),
                    "hash": calls[index]["hash"],
                    "address": calls[index]["address"],
                    "name": calls[index]["method"]._name,
                    "inputs": calls[index]["inputs"],
                    "block_number": block_number,
                }
            )
    return results


# def crawl_job(job):
#     print(job)
#     pass


#     return generated_hash


def generate_call_tree(jobs):

    contracts_ABIs = {}
    contracts_methods = {}
    calls = {"WithoutSubcalls": [], "WithSubcalls": {}}

    # client = web3.Web3()

    network.connect("polygon-main")

    print(len(chain))
    multicaller = Multicall2.Multicall2(Multicall2_address)

    multicall_method = multicaller.contract.tryAggregate

    # test call

    def recursive_unpack(method_abi: Any, level: int = 0) -> Any:
        have_subcalls = False

        print(level)
        print(method_abi)

        abi = {
            "level": level,
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

        generated_hash = hashlib.md5(json.dumps(abi).encode("utf-8")).hexdigest()

        if have_subcalls:
            abi["generated_hash"] = generated_hash
            abi["address"] = method_abi["address"]
            if not calls["WithSubcalls"].get(level):
                calls["WithSubcalls"][level] = []
            calls["WithSubcalls"][level].append(abi)
        else:
            # generate calls

            # generate parameters list of parameters lists

            parameters = []

            for input in abi["inputs"]:
                if type(input["value"]) in (str, int):
                    parameters.append([input["value"]])
                elif type(input["value"]) == list:
                    parameters.append(input["value"])
                else:
                    raise Exception(f"Unknown type {type(input['value'])}")

            for call_parameters in itertools.product(*parameters):
                # if not calls["WithoutSubcalls"].get(generated_hash):
                #     calls["WithoutSubcalls"][generated_hash] = []
                calls["WithoutSubcalls"].append(
                    {
                        "address": job["address"],
                        "inputs": call_parameters,
                        "generated_hash": generated_hash,
                        "name": abi["name"],
                    }
                )

        if not contracts_methods.get(job["address"]):
            contracts_methods[job["address"]] = []
        if generated_hash not in contracts_methods[job["address"]]:
            contracts_methods[job["address"]].append(generated_hash)
            if not contracts_ABIs.get(job["address"]):
                contracts_ABIs[job["address"]] = {}
            contracts_ABIs[job["address"]][generated_hash] = abi

        return generated_hash

    # selector
    # hashlib.md5(json.dumps(method).encode("utf-8")).hexdigest()

    for job in jobs:
        if job["address"] not in contracts_ABIs:
            contracts_ABIs[job["address"]] = []

        recursive_unpack(job, 0)

    # generate contracts interfaces

    interfaces = {}

    # web3 general interface workflow
    # for contract_address in contracts_ABIs:

    #     # collect abis for each contract
    #     abis = []

    #     for method_hash in contracts_methods[contract_address]:
    #         abis.append(contracts_ABIs[contract_address][method_hash])

    #     # generate interface
    #     interfaces[contract_address] = client.eth.contract(abi=abis,address=contract_address)

    # batch_calls = []

    # for call in calls["WithoutSubcalls"]:
    #     print(dir(interfaces[call["address"]].functions[call["name"]](*call["inputs"])))
    #     batch_calls.append(
    #         {
    #             "to": call["address"],
    #             "call": interfaces[call["address"]].encodeABI(fn_name=call["name"], args=call["inputs"]),
    #             "hash": call["generated_hash"]
    #         }
    #     )

    # Brownie interface generating

    for contract_address in contracts_ABIs:

        # collect abis for each contract
        abis = []

        for method_hash in contracts_methods[contract_address]:
            abis.append(contracts_ABIs[contract_address][method_hash])

        # generate interface
        interfaces[contract_address] = Contract.from_abi(
            random(), contract_address, abis
        )

    batch_calls = []

    for call in calls["WithoutSubcalls"]:
        # print(dir(interfaces[call["address"]]))
        # print(
        #     interfaces[call["address"]].get_method_object(
        #         interfaces[call["address"]].signatures[call["name"]]
        #     )
        # )
        batch_calls.append(
            {
                "address": call["address"],
                "method": interfaces[call["address"]].get_method_object(
                    interfaces[call["address"]].signatures[call["name"]]
                ),
                "hash": call["generated_hash"],
                "inputs": call["inputs"],
            }
        )

    make_multicall_result = make_multicall(
        multicall_method=multicall_method, calls=batch_calls
    )

    # responces dict

    responces = {}  # {generated_hash: []}

    # create chunks of calls
    batch_size = 500

    for call_chunk in [
        batch_calls[i : i + batch_size] for i in range(0, len(batch_calls), batch_size)
    ]:
        print("batch_step", len(call_chunk))

        while True:
            try:
                make_multicall_result = make_multicall(
                    multicall_method=multicall_method, calls=call_chunk
                )
                break
            except ValueError:
                continue
        # results parsing and writing to database

        for result in make_multicall_result:
            if result["hash"] not in responces:
                responces[result["hash"]] = []
            responces[result["hash"]].append(result["result"])

    # proccessing call_tree

    # reverse call_tree
    call_tree_levels = sorted(calls["WithSubcalls"].keys(), reverse=True)

    for level in call_tree_levels:

        calls_of_level = []

        for call in calls["WithSubcalls"][level]:
            parameters = []

            for input in call["inputs"]:

                if type(input["value"]) in (str, int):
                    if input["value"] not in responces:
                        parameters.append([input["value"]])
                    else:
                        # print(responces[input["value"]])
                        if (
                            contracts_ABIs[call["address"]][input["value"]]["name"]
                            == "totalSupply"
                        ):
                            parameters.append(
                                list(range(0, responces[input["value"]][0]))
                            )
                            print(len(list(range(0, responces[input["value"]][0]))))
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
                        "method": interfaces[call["address"]].get_method_object(
                            interfaces[call["address"]].signatures[call["name"]]
                        ),
                        "hash": call["generated_hash"],
                        "inputs": call_parameters,
                    }
                )
            print(len(call_parameters))

        for call_chunk in [
            calls_of_level[i : i + batch_size]
            for i in range(0, len(calls_of_level), batch_size)
        ]:

            print("batch_step", len(call_chunk))

            while True:
                try:
                    make_multicall_result = make_multicall(
                        multicall_method=multicall_method, calls=call_chunk
                    )
                    break
                except ValueError:
                    continue
            # results parsing and writing to database

            for result in make_multicall_result:
                if result["hash"] not in responces:
                    responces[result["hash"]] = []
                responces[result["hash"]].append(result["result"])

    print("contracts_methods")
    pprint(contracts_methods)
    print("contracts_ABIs")
    pprint(contracts_ABIs)
    print("calls")
    pprint(calls)
    print("responses")
    pprint(responces)


def handle_crawl(args: argparse.Namespace) -> None:

    """
    Ability to track states of the contracts.

    Read all view methods of the contracts and crawl

    The querstion is input patameters of method

    tags:
    address:0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f

    type:function

    abi_method_hash:5fbaec05ae19ac90eea75b676a20e495

    subscription_type:polygon_smartcontract

    abi_name:transfer

    status:active

    contract_address:0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f

    content:
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_tokenId",
                "type": "uint256"
            }
        ],
        "name": "getDNA",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }


    {
        "inputs": [
                    {
                        "name": "_tokenId",
                        "type": "uint256"
                        "position":0,
                        "value": {
                            "address": "0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
                            "inputs": [],
                            "name": "totalSupply"
                        }
                    }
                ],
        "name": "getDNA",
        "address": "0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
    }


    {
        "inputs": [
                    {
                        "name": "_tokenId",
                        "type": "uint256"
                        "value": {
                            "address": "0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
                            "inputs": [],
                            "name": "totalSupply"
                        }
                    }
                ],
        "name": "getDNA",
        "address": "0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
    }


    {
        "name": "getUnicornBodyParts",
        "address": "0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
        "inputs": [ {
            "name": "_dna",
            "type": "uint256"
            "value":{
                    "inputs": [
                                {
                                    "name": "_tokenId",
                                    "type": "uint256"
                                    "value": {
                                        "address": "0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
                                        "inputs": [],
                                        "name": "totalSupply"
                                    }
                                }
                            ],
                    "name": "getDNA",
                    "address": "0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
                }
            }
        ]
    }





    """

    my_job = {
        "name": "getUnicornBodyParts",
        "address": "0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
        "type": "function",
        "inputs": [
            {
                "name": "_dna",
                "type": "uint256",
                "internalType": "uint256",
                "value": {
                    "type": "function",
                    "inputs": [
                        {
                            "internalType": "uint256",
                            "modify": "range",
                            "name": "_tokenId",
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
                    "name": "getDNA",
                    "outputs": [
                        {"internalType": "uint256", "name": "", "type": "uint256"}
                    ],
                    "address": "0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",
                },
            }
        ],
        "outputs": [
            {"internalType": "uint256", "name": "bodyPartId", "type": "uint256"},
            {"internalType": "uint256", "name": "facePartId", "type": "uint256"},
            {"internalType": "uint256", "name": "hornPartId", "type": "uint256"},
            {"internalType": "uint256", "name": "hoovesPartId", "type": "uint256"},
            {"internalType": "uint256", "name": "manePartId", "type": "uint256"},
            {"internalType": "uint256", "name": "tailPartId", "type": "uint256"},
            {"internalType": "uint8", "name": "mythicCount", "type": "uint8"},
        ],
    }

    # blockchain_type = AvailableBlockchainType(args.blockchain_type)

    # if args.web3 is None:
    #     raise ValueError("Web3 provider URL is required")

    # web3 = Web3(Web3.HTTPProvider(args.web3))

    # if args.poa:
    #     web3.middleware_stack.inject(geth_poa_middleware, layer=0)

    # Generate call tree
    call_tree = generate_call_tree([my_job])
    print(call_tree)


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

    parser.add_argument(
        "--access-id",
        default=NB_CONTROLLER_ACCESS_ID,
        type=UUID,
        help="User access ID",
    )

    subparsers = parser.add_subparsers()

    parser_parse_abi = subparsers.add_parser(
        "parse_job",
        help="continuous crawling the event/function call jobs from bugout journal",
    )
    parser_parse_abi.set_defaults(func=handle_crawl)

    crawl_parser = subparsers.add_parser(
        "crawl",
        help="continuous crawling the event/function call jobs from bugout journal",
    )

    crawl_parser.add_argument(
        "--start",
        "-s",
        type=int,
        default=None,
        help="start block number",
    )
    crawl_parser.add_argument(
        "--blockchain-type",
        "-b",
        type=str,
        help=f"Available blockchain types: {[member.value for member in AvailableBlockchainType]}",
    )
    crawl_parser.add_argument(
        "--web3",
        type=str,
        default=None,
        help="Web3 provider URL",
    )
    crawl_parser.add_argument(
        "--poa",
        action="store_true",
        default=False,
        help="Use PoA middleware",
    )

    crawl_parser.add_argument(
        "--max-blocks-batch",
        "-m",
        type=int,
        default=80,
        help="Maximum number of blocks to crawl in a single batch",
    )

    crawl_parser.add_argument(
        "--min-blocks-batch",
        "-n",
        type=int,
        default=20,
        help="Minimum number of blocks to crawl in a single batch",
    )

    crawl_parser.add_argument(
        "--confirmations",
        "-c",
        type=int,
        default=175,
        help="Number of confirmations to wait for",
    )

    crawl_parser.add_argument(
        "--min-sleep-time",
        "-t",
        type=float,
        default=0.1,
        help="Minimum time to sleep between crawl step",
    )

    crawl_parser.add_argument(
        "--heartbeat-interval",
        "-i",
        type=float,
        default=60,
        help="Heartbeat interval in seconds",
    )

    crawl_parser.add_argument(
        "--new-jobs-refetch-interval",
        "-r",
        type=float,
        default=180,
        help="Time to wait before refetching new jobs",
    )

    crawl_parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force start from the start block",
    )

    crawl_parser.set_defaults(func=handle_crawl)

    generate_view_parser = subparsers.add_parser(
        "parse-abi",
        help="parse the abi of the contract",
    )

    generate_view_parser.add_argument(
        "--abi-file",
        "-a",
        type=str,
        help="abi file",
    )
    generate_view_parser.set_defaults(func=parse_abi)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
