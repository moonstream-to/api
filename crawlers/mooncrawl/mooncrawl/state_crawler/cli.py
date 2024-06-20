import argparse
import hashlib
import itertools
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures._base import TimeoutError
from pprint import pprint
from typing import Any, Dict, List, Optional
from uuid import UUID

from moonstream.client import Moonstream  # type: ignore
from moonstreamdb.blockchain import AvailableBlockchainType
from mooncrawl.moonworm_crawler.crawler import _retry_connect_web3

from ..actions import recive_S3_data_from_query, get_all_entries_from_search
from ..blockchain import connect
from ..data import ViewTasks
from ..db import PrePing_SessionLocal
from ..settings import (
    bugout_client as bc,
    INFURA_PROJECT_ID,
    infura_networks,
    multicall_contracts,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_STATE_CRAWLER_JOURNAL_ID,
)
from .db import clean_labels, commit_session, view_call_to_label
from .Multicall2_interface import Contract as Multicall2
from .web3_util import FunctionSignature

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


client = Moonstream()


def execute_query(query: Dict[str, Any], token: str):
    """
    Query task example:

    {
        "type": "queryAPI",
        "query_url": "template_erc721_minting",
        "blockchain": "mumbai",
        "params": {
            "address": "0x230E4e85d4549343A460F5dE0a7035130F62d74C"
        },
        "keys": [
            "token_id"
        ]
    }

    """

    # get the query url
    query_url = query["query_url"]

    # get the blockchain
    blockchain = query.get("blockchain")

    # get the parameters
    params = query["params"]

    body = {"params": params}

    if blockchain:
        body["blockchain"] = blockchain

    # run query template via moonstream query API

    data = recive_S3_data_from_query(
        client=client,
        token=token,
        query_name=query_url,
        custom_body=body,
    )

    # extract the keys as a list

    keys = query["keys"]

    # extract the values from the data

    data = data["data"]

    if len(data) == 0:
        return []

    result = []

    for item in data:
        if len(keys) == 1:
            result.append(item[keys[0]])
        else:
            result.append(tuple([item[key] for key in keys]))

    return result


def make_multicall(
    multicall_method: Any,
    calls: List[Any],
    block_timestamp: int,
    block_number: str = "latest",
) -> Any:
    multicall_calls = []

    for call in calls:
        try:
            multicall_calls.append(
                (
                    call["address"],
                    call["method"].encode_data(call["inputs"]).hex(),
                )
            )
        except Exception as e:
            logger.error(
                f'Error encoding data for method {call["method"].name} call: {call}'
            )

    multicall_result = multicall_method(False, calls=multicall_calls).call(
        block_identifier=block_number
    )

    results = []

    # Handle the case with not successful calls
    for index, encoded_data in enumerate(multicall_result):
        try:
            if encoded_data[0]:
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
        except Exception as e:
            results.append(
                {
                    "result": str(encoded_data[1]),
                    "hash": calls[index]["hash"],
                    "method": calls[index]["method"],
                    "address": calls[index]["address"],
                    "name": calls[index]["method"].name,
                    "inputs": calls[index]["inputs"],
                    "call_data": multicall_calls[index][1],
                    "block_number": block_number,
                    "block_timestamp": block_timestamp,
                    "status": encoded_data[0],
                    "error": str(e),
                }
            )

            logger.error(
                f"Error decoding data for for method {call['method'].name} call {calls[index]}: {e}."
            )
            # data is not decoded, return the encoded data
            logger.error(f"Encoded data: {encoded_data}")

    return results


def crawl_calls_level(
    web3_client,
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
    max_batch_size=3000,
    min_batch_size=4,
):
    calls_of_level = []

    for call in calls:
        if call["generated_hash"] in responces:
            continue
        parameters = []

        for input in call["inputs"]:
            if type(input["value"]) in (str, int):
                if input["value"] not in responces:
                    parameters.append([input["value"]])
                else:
                    if input["value"] in contracts_ABIs[call["address"]] and (
                        contracts_ABIs[call["address"]][input["value"]]["name"]
                        == "totalSupply"
                    ):  # hack for totalSupply TODO(Andrey): need add propper support for response parsing
                        parameters.append(
                            list(range(1, responces[input["value"]][0][0] + 1))
                        )
                    else:
                        parameters.append(responces[input["value"]])
            elif type(input["value"]) == list:
                parameters.append(input["value"])
            else:
                raise

        for call_parameters in itertools.product(*parameters):
            # hack for tuples product
            if len(call_parameters) == 1 and type(call_parameters[0]) == tuple:
                call_parameters = call_parameters[0]
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

    retry = 0

    while len(calls_of_level) > 0:
        make_multicall_result = []
        try:
            call_chunk = calls_of_level[:batch_size]

            logger.info(
                f"Calling multicall2 with {len(call_chunk)} calls at block {block_number}"
            )

            # 1 thead with timeout for hung multicall calls
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    make_multicall,
                    multicall_method,
                    call_chunk,
                    block_timestamp,
                    block_number,
                )
                make_multicall_result = future.result(timeout=20)
            retry = 0
            calls_of_level = calls_of_level[batch_size:]
            logger.info(f"lenght of task left {len(calls_of_level)}.")
            batch_size = min(batch_size * 2, max_batch_size)
        except ValueError as e:  # missing trie node
            logger.error(f"ValueError: {e}, retrying")
            retry += 1
            if "missing trie node" in str(e):
                time.sleep(4)
            if retry > 5:
                raise (e)
            batch_size = max(batch_size // 4, min_batch_size)
        except TimeoutError as e:  # timeout
            logger.error(f"TimeoutError: {e}, retrying")
            retry += 1
            if retry > 5:
                raise (e)
            batch_size = max(batch_size // 3, min_batch_size)
        except Exception as e:
            logger.error(f"Exception: {e}")
            raise (e)
        time.sleep(2)
        logger.debug(f"Retry: {retry}")
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

    return batch_size


def parse_jobs(
    jobs: List[Any],
    blockchain_type: AvailableBlockchainType,
    web3_provider_uri: Optional[str],
    block_number: Optional[int],
    batch_size: int,
    moonstream_token: str,
    web3_uri: Optional[str] = None,
):
    """
    Parse jobs from list and generate web3 interfaces for each contract.
    """

    contracts_ABIs: Dict[str, Any] = {}
    contracts_methods: Dict[str, Any] = {}
    calls: Dict[int, Any] = {0: []}
    responces: Dict[str, Any] = {}

    if web3_provider_uri is not None:
        try:
            logger.info(
                f"Connecting to blockchain: {blockchain_type} with custom provider!"
            )

            web3_client = connect(
                blockchain_type=blockchain_type, web3_uri=web3_provider_uri
            )
        except Exception as e:
            logger.error(
                f"Web3 connection to custom provider {web3_provider_uri} failed error: {e}"
            )
            raise (e)
    else:
        logger.info(f"Connecting to blockchain: {blockchain_type} with Node balancer.")
        web3_client = _retry_connect_web3(
            blockchain_type=blockchain_type, web3_uri=web3_uri
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

        ### we add queryAPI to that tree

        if method_abi["type"] == "queryAPI":
            # make queryAPI call

            responce = execute_query(method_abi, token=moonstream_token)

            # generate hash for queryAPI call

            generated_hash = hashlib.md5(
                json.dumps(
                    method_abi,
                    sort_keys=True,
                    indent=4,
                    separators=(",", ": "),
                ).encode("utf-8")
            ).hexdigest()

            # add responce to responces

            responces[generated_hash] = responce

            return generated_hash

        abi = {
            "inputs": [],
            "outputs": method_abi["outputs"],
            "name": method_abi["name"],
            "type": "function",
            "stateMutability": "view",
        }

        for input in method_abi["inputs"]:
            if type(input["value"]) in (int, list):
                abi["inputs"].append(input)

            elif type(input["value"]) == str:
                abi["inputs"].append(input)

            elif type(input["value"]) == dict:
                if input["value"]["type"] == "function":
                    hash_link = recursive_unpack(input["value"], level + 1)
                    # replace defenition by hash pointing to the result of the recursive_unpack
                    input["value"] = hash_link
                    have_subcalls = True
                elif input["value"]["type"] == "queryAPI":
                    input["value"] = recursive_unpack(input["value"], level + 1)
                    have_subcalls = True
                abi["inputs"].append(input)
        abi["address"] = method_abi["address"]
        generated_hash = hashlib.md5(
            json.dumps(abi, sort_keys=True, indent=4, separators=(",", ": ")).encode(
                "utf-8"
            )
        ).hexdigest()

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

    # reverse call_tree
    call_tree_levels = sorted(calls.keys(), reverse=True)[:-1]

    db_session = PrePing_SessionLocal()

    # run crawling of levels
    try:
        # initial call of level 0 all call without subcalls directly moved there
        logger.info(f"Crawl level: 0. Jobs amount: {len(calls[0])}")
        logger.info(f"call_tree_levels: {call_tree_levels}")

        batch_size = crawl_calls_level(
            web3_client,
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
            logger.info(f"Crawl level: {level}. Jobs amount: {len(calls[level])}")

            batch_size = crawl_calls_level(
                web3_client,
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

    blockchain_type = AvailableBlockchainType(args.blockchain)

    if args.jobs_file is not None:
        with open(args.jobs_file, "r") as f:
            jobs = json.load(f)

    else:

        logger.info("Reading jobs from the journal")

        jobs = []

        # Bugout
        query = f"#state_job #blockchain:{blockchain_type.value}"

        existing_jobs = get_all_entries_from_search(
            journal_id=MOONSTREAM_STATE_CRAWLER_JOURNAL_ID,
            search_query=query,
            limit=1000,
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            content=True,
        )

        if len(existing_jobs) == 0:
            logger.info("No jobs found in the journal")
            return

        for job in existing_jobs:

            try:
                if job.content is None:
                    logger.error(f"Job content is None for entry {job.entry_url}")
                    continue
                ### parse json
                job_content = json.loads(job.content)
                ### validate via ViewTasks
                ViewTasks(**job_content)
                jobs.append(job_content)
            except Exception as e:

                logger.error(f"Job validation of entry {job.entry_url} failed: {e}")
                continue

    custom_web3_provider = args.web3_uri

    if args.infura and INFURA_PROJECT_ID is not None:
        if blockchain_type not in infura_networks:
            raise ValueError(
                f"Infura is not supported for {blockchain_type} blockchain type"
            )
        logger.info(f"Using Infura!")
        custom_web3_provider = infura_networks[blockchain_type]["url"]

    parse_jobs(
        jobs,
        blockchain_type,
        custom_web3_provider,
        args.block_number,
        args.batch_size,
        args.moonstream_token,
        args.web3_uri,
    )


def parse_abi(args: argparse.Namespace) -> None:
    """
    Parse the abi of the contract and save it to the database.
    """

    with open(args.abi_file, "r") as f:
        abi = json.load(f)

    output_json = []

    for method in abi:
        # read json and parse only stateMutability equal to view
        if method.get("stateMutability") and method["stateMutability"] == "view":
            output_json.append(method)

    with open(f"view+{args.abi_file}", "w") as f:
        json.dump(output_json, f)


def clean_labels_handler(args: argparse.Namespace) -> None:
    blockchain_type = AvailableBlockchainType(args.blockchain)

    web3_client = _retry_connect_web3(
        blockchain_type=blockchain_type, web3_uri=args.web3_uri
    )

    logger.info(f"Label cleaner connected to blockchain: {blockchain_type}")

    block_number = web3_client.eth.get_block("latest").number  # type: ignore

    db_session = PrePing_SessionLocal()

    try:
        clean_labels(db_session, blockchain_type, args.blocks_cutoff, block_number)
    finally:
        db_session.close()


def migrate_state_tasks_handler(args: argparse.Namespace) -> None:

    ### Get all tasks from files
    with open(args.jobs_file, "r") as f:
        jobs = json.load(f)

    # file example jobs/ethereum-jobs.json

    blockchain_type = AvailableBlockchainType(args.blockchain)

    migrated_blockchain = blockchain_type.value

    ### Get all tasks from the journal

    query = f"#state_job #{migrated_blockchain}"

    existing_jobs = get_all_entries_from_search(
        journal_id=MOONSTREAM_STATE_CRAWLER_JOURNAL_ID,
        search_query=query,
        limit=1000,
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        content=True,
    )

    existing_state_tasks_list = []

    print(f"Existing jobs: {len(existing_jobs)}")
    print(f"New jobs: {jobs}")

    ### validate existing jobs
    for job in existing_jobs:

        try:
            if job.content is None:
                logger.error(f"Job content is None for entry {job.entry_url}")
                continue
            ### parse json
            job_content = json.loads(job.content)
            ### validate via ViewTasks
            ViewTasks(**job_content)
        except Exception as e:

            logger.error(f"Job validation of entry {job.entry_url} failed: {e}")
            continue

        ### from tags get blockchain, name and address

        for tag in job.tags:
            if tag.startswith("blockchain"):
                blockchain = tag.split(":")[1]
            if tag.startswith("name"):
                name = tag.split(":")[1]
            if tag.startswith("address"):
                address = tag.split(":")[1]

        existing_state_tasks_list.append(f"{blockchain}:{name}:{address}")

    ### Get all tasks from files

    for job in jobs:

        name = job["name"]

        address = job["address"]

        ### Deduplicate tasks
        if f"{migrated_blockchain}:{name}:{address}" not in existing_state_tasks_list:
            ### create new task

            json_str = json.dumps(job, indent=4)

            ### add tabs to json string for better readability
            json_str_with_tabs = "\n".join(
                "\t" + line for line in json_str.splitlines()
            )

            try:
                bc.create_entry(
                    title=f"{name}:{address}",
                    token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                    journal_id=MOONSTREAM_STATE_CRAWLER_JOURNAL_ID,
                    content=json_str_with_tabs,
                    tags=[
                        "state_job",
                        f"blockchain:{migrated_blockchain}",
                        f"name:{name}",
                        f"address:{address}",
                    ],
                )
            except Exception as e:
                logger.error(f"Error creating entry: {e}")
                continue


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=lambda _: parser.print_help())

    parser.add_argument(
        "--web3-uri",
        help="Node JSON RPC uri",
    )

    subparsers = parser.add_subparsers()

    view_state_crawler_parser = subparsers.add_parser(
        "crawl-jobs",
        help="continuous crawling the view methods from job structure",  # TODO(ANDREY): move tasks to journal
    )
    view_state_crawler_parser.add_argument(
        "--moonstream-token",
        "-t",
        type=str,
        help="Moonstream token",
        required=True,
    )
    view_state_crawler_parser.add_argument(
        "--blockchain",
        "-b",
        type=str,
        help="Type of blovkchain wich writng in database",
        required=True,
    )
    view_state_crawler_parser.add_argument(
        "--infura",
        action="store_true",
        help="Use infura as web3 provider",
    )
    view_state_crawler_parser.add_argument(
        "--block-number", "-N", type=str, help="Block number."
    )
    view_state_crawler_parser.add_argument(
        "--jobs-file",
        "-j",
        type=str,
        help="Path to json file with jobs",
        required=False,
    )
    view_state_crawler_parser.add_argument(
        "--batch-size",
        "-s",
        type=int,
        default=500,
        help="Size of chunks wich send to Multicall2 contract.",
    )
    view_state_crawler_parser.set_defaults(func=handle_crawl)

    view_state_migration_parser = subparsers.add_parser(
        "migrate-jobs",
        help="Migrate jobs from one files to bugout",
    )
    view_state_migration_parser.add_argument(
        "--jobs-file",
        "-j",
        type=str,
        help="Path to json file with jobs",
        required=True,
    )

    view_state_migration_parser.add_argument(
        "--blockchain",
        "-b",
        type=str,
        help="Type of blovkchain wich writng in database",
        required=True,
    )

    view_state_migration_parser.set_defaults(func=migrate_state_tasks_handler)

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
        required=True,
        type=int,
        help="Amount blocks back, after wich data will be remove.",
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
