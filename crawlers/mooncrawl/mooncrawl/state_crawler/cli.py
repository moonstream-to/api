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
import requests
from uuid import UUID
from web3 import Web3

from moonstream.client import Moonstream  # type: ignore
from moonstreamtypes.blockchain import AvailableBlockchainType
from mooncrawl.moonworm_crawler.crawler import _retry_connect_web3

from ..actions import recive_S3_data_from_query, get_all_entries_from_search
from ..blockchain import connect
from ..data import ViewTasks
from ..db import PrePing_SessionLocal, create_moonstream_engine, sessionmaker
from ..settings import (
    bugout_client as bc,
    INFURA_PROJECT_ID,
    infura_networks,
    multicall_contracts,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_STATE_CRAWLER_JOURNAL_ID,
    MOONSTREAM_DB_V3_CONTROLLER_API,
)
from .db import clean_labels, commit_session, view_call_to_label
from .Multicall2_interface import Contract as Multicall2
from .web3_util import FunctionSignature

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


client = Moonstream()


def request_connection_string(
    customer_id: str,
    instance_id: int,
    token: str,
    user: str = "seer",  # token with write access
) -> str:
    """
    Request connection string from the Moonstream API.
    """
    response = requests.get(
        f"{MOONSTREAM_DB_V3_CONTROLLER_API}/customers/{customer_id}/instances/{instance_id}/creds/{user}/url",
        headers={"Authorization": f"Bearer {token}"},
    )

    response.raise_for_status()

    return response.text.replace('"', "")


def execute_query(query: Dict[str, Any], token: str) -> Any:
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

    print(f"Executing query: {query}")

    # get the query url
    query_url = query["query_url"]

    # get the blockchain
    blockchain = query.get("blockchain")

    # get the parameters
    params = query["params"]

    body = {"params": params}
    query_params = dict()

    if query.get("customer_id") and query.get("instance_id"):
        query_params["customer_id"] = query["customer_id"]
        query_params["instance_id"] = query["instance_id"]

    if blockchain:
        body["blockchain"] = blockchain

    # run query template via moonstream query API

    data = recive_S3_data_from_query(
        client=client,
        token=token,
        query_name=query_url,
        custom_body=body,
        customer_params=query_params,
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


def encode_calls(calls: List[Dict[str, Any]]) -> List[tuple]:
    """Encodes the call data for multicall."""
    multicall_calls = []
    for call in calls:
        try:
            encoded_data = call["method"].encode_data(call["inputs"]).hex()
            multicall_calls.append((call["address"], encoded_data))
        except Exception as e:
            logger.error(
                f'Error encoding data for method {call["method"].name} call: {call}. Error: {e}'
            )
    return multicall_calls


def perform_multicall(
    multicall_method: Any, multicall_calls: List[tuple], block_identifier: str
) -> Any:
    """Performs the multicall and returns the result."""
    return multicall_method(False, calls=multicall_calls).call(
        block_identifier=block_identifier
    )


def process_multicall_result(
    calls: List[Dict[str, Any]],
    multicall_result: Any,
    multicall_calls: List[tuple],
    block_timestamp: int,
    block_number: str,
    block_hash: Optional[str],
) -> List[Dict[str, Any]]:
    """Processes the multicall result and decodes the data."""
    results = []
    for index, encoded_data in enumerate(multicall_result):
        call = calls[index]
        try:
            result_data = call["method"].decode_data(encoded_data[1])
            result = {
                "result": result_data,
                "hash": call["hash"],
                "method": call["method"],
                "address": call["address"],
                "name": call["method"].name,
                "inputs": call["inputs"],
                "call_data": multicall_calls[index][1],
                "block_number": block_number,
                "block_timestamp": block_timestamp,
                "block_hash": block_hash,
                "status": encoded_data[0],
                "v3": call.get("v3", False),
                "customer_id": call.get("customer_id"),
                "instance_id": call.get("instance_id"),
            }
            results.append(result)
        except Exception as e:
            result = {
                "result": str(encoded_data[1]),
                "hash": call["hash"],
                "method": call["method"],
                "address": call["address"],
                "name": call["method"].name,
                "inputs": call["inputs"],
                "call_data": multicall_calls[index][1],
                "block_number": block_number,
                "block_timestamp": block_timestamp,
                "block_hash": block_hash,
                "status": encoded_data[0],
                "error": str(e),
                "v3": call.get("v3", False),
                "customer_id": call.get("customer_id"),
                "instance_id": call.get("instance_id"),
            }
            results.append(result)
            logger.error(
                f"Error decoding data for method {call['method'].name} call {call}: {e}."
            )
            logger.error(f"Encoded data: {encoded_data}")
    return results


def make_multicall(
    multicall_method: Any,
    calls: List[Dict[str, Any]],
    block_timestamp: int,
    block_number: str = "latest",
    block_hash: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Makes a multicall to the blockchain and processes the results."""
    multicall_calls = encode_calls(calls)
    # breakpoint()
    multicall_result = perform_multicall(
        multicall_method, multicall_calls, block_number
    )
    results = process_multicall_result(
        calls,
        multicall_result,
        multicall_calls,
        block_timestamp,
        block_number,
        block_hash,
    )
    return results


def generate_calls_of_level(
    calls: List[Dict[str, Any]],
    responses: Dict[str, Any],
    contracts_ABIs: Dict[str, Any],
    interfaces: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Generates the calls for the current level."""
    calls_of_level = []
    for call in calls:
        if call["generated_hash"] in responses:
            continue
        parameters = []
        for input in call["inputs"]:
            if isinstance(input["value"], (str, int)):
                if input["value"] not in responses:
                    parameters.append([input["value"]])
                else:
                    if (
                        input["value"] in contracts_ABIs[call["address"]]
                        and contracts_ABIs[call["address"]][input["value"]]["name"]
                        == "totalSupply"
                    ):
                        # Hack for totalSupply
                        parameters.append(
                            list(range(1, responses[input["value"]][0][0] + 1))
                        )
                    else:
                        parameters.append(responses[input["value"]])
            elif isinstance(input["value"], list):
                parameters.append(input["value"])
            else:
                raise Exception("Unknown input value type")
        for call_parameters in itertools.product(*parameters):
            if len(call_parameters) == 1 and isinstance(call_parameters[0], tuple):
                call_parameters = call_parameters[0]
            calls_of_level.append(
                {
                    "address": call["address"],
                    "method": FunctionSignature(
                        interfaces[call["address"]].get_function_by_name(call["name"])
                    ),
                    "hash": call["generated_hash"],
                    "inputs": call_parameters,
                    "v3": call.get("v3", False),
                    "customer_id": call.get("customer_id"),
                    "instance_id": call.get("instance_id"),
                }
            )
    return calls_of_level


def process_results(
    make_multicall_result: List[Dict[str, Any]],
    db_sessions: Dict[Any, Any],
    responses: Dict[str, Any],
    blockchain_type: Any,
) -> int:
    """Processes the results and adds them to the appropriate database sessions."""
    add_to_session_count = 0
    sessions_to_commit = set()
    for result in make_multicall_result:
        v3 = result.get("v3", False)
        if v3:
            customer_id = result.get("customer_id")
            instance_id = result.get("instance_id")
            db_session = db_sessions.get((customer_id, instance_id))
        else:
            db_session = db_sessions.get("v2")
        if db_session is None:
            logger.error(f"No db_session found for result {result}")
            continue
        db_view = view_call_to_label(blockchain_type, result, v3)
        db_session.add(db_view)
        sessions_to_commit.add(db_session)
        add_to_session_count += 1
        if result["hash"] not in responses:
            responses[result["hash"]] = []
        responses[result["hash"]].append(result["result"])
    # Commit all sessions
    for session in sessions_to_commit:
        commit_session(session)
    logger.info(f"{add_to_session_count} labels committed to database.")
    return add_to_session_count


def crawl_calls_level(
    web3_client: Web3,
    db_sessions: Dict[Any, Any],
    calls: List[Dict[str, Any]],
    responses: Dict[str, Any],
    contracts_ABIs: Dict[str, Any],
    interfaces: Dict[str, Any],
    batch_size: int,
    multicall_method: Any,
    block_number: str,
    blockchain_type: Any,
    block_timestamp: int,
    max_batch_size: int = 3000,
    min_batch_size: int = 4,
    block_hash: Optional[str] = None,
) -> int:
    """Crawls calls at a specific level."""
    calls_of_level = generate_calls_of_level(
        calls, responses, contracts_ABIs, interfaces
    )
    retry = 0
    while len(calls_of_level) > 0:
        make_multicall_result = []
        try:
            call_chunk = calls_of_level[:batch_size]
            logger.info(
                f"Calling multicall2 with {len(call_chunk)} calls at block {block_number}"
            )
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    make_multicall,
                    multicall_method,
                    call_chunk,
                    block_timestamp,
                    block_number,
                    block_hash,
                )
                make_multicall_result = future.result(timeout=20)
            retry = 0
            calls_of_level = calls_of_level[batch_size:]
            logger.info(f"Length of tasks left: {len(calls_of_level)}.")
            batch_size = min(batch_size * 2, max_batch_size)
        except ValueError as e:
            logger.error(f"ValueError: {e}, retrying")
            retry += 1
            if "missing trie node" in str(e):
                time.sleep(4)
            if retry > 5:
                raise e
            batch_size = max(batch_size // 4, min_batch_size)
        except TimeoutError as e:
            logger.error(f"TimeoutError: {e}, retrying")
            retry += 1
            if retry > 5:
                raise e
            batch_size = max(batch_size // 3, min_batch_size)
        except Exception as e:
            logger.error(f"Exception: {e}")
            raise e
        time.sleep(2)
        logger.debug(f"Retry: {retry}")
        process_results(make_multicall_result, db_sessions, responses, blockchain_type)
    return batch_size


def connect_to_web3(
    blockchain_type: Any,
    web3_provider_uri: Optional[str],
    web3_uri: Optional[str],
) -> Web3:
    """Connects to the Web3 client."""
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
                f"Web3 connection to custom provider {web3_provider_uri} failed. Error: {e}"
            )
            raise e
    else:
        logger.info(f"Connecting to blockchain: {blockchain_type} with node balancer.")
        web3_client = _retry_connect_web3(
            blockchain_type=blockchain_type, web3_uri=web3_uri
        )
    logger.info(f"Crawler started connected to blockchain: {blockchain_type}")
    return web3_client


def get_block_info(web3_client: Web3, block_number: Optional[int]) -> tuple:
    """Retrieves block information."""
    if block_number is None:
        block_number = web3_client.eth.get_block("latest").number  # type: ignore
    logger.info(f"Current block number: {block_number}")
    block = web3_client.eth.get_block(block_number)  # type: ignore
    block_timestamp = block.timestamp  # type: ignore
    block_hash = block.hash.hex()  # type: ignore
    return block_number, block_timestamp, block_hash


def recursive_unpack(
    method_abi: Any,
    level: int,
    calls: Dict[int, List[Any]],
    contracts_methods: Dict[str, Any],
    contracts_ABIs: Dict[str, Any],
    responses: Dict[str, Any],
    moonstream_token: str,
    v3: bool,
    customer_id: Optional[str] = None,
    instance_id: Optional[str] = None,
) -> str:
    """Recursively unpacks method ABIs to generate a tree of calls."""
    have_subcalls = False
    if method_abi["type"] == "queryAPI":
        # Make queryAPI call
        response = execute_query(method_abi, token=moonstream_token)
        # Generate hash for queryAPI call
        generated_hash = hashlib.md5(
            json.dumps(
                method_abi,
                sort_keys=True,
                indent=4,
                separators=(",", ": "),
            ).encode("utf-8")
        ).hexdigest()
        # Add response to responses
        responses[generated_hash] = response
        return generated_hash

    abi = {
        "inputs": [],
        "outputs": method_abi["outputs"],
        "name": method_abi["name"],
        "type": "function",
        "stateMutability": "view",
        "v3": v3,
        "customer_id": customer_id,
        "instance_id": instance_id,
    }

    for input in method_abi["inputs"]:
        if isinstance(input["value"], (int, list, str)):
            abi["inputs"].append(input)
        elif isinstance(input["value"], dict):
            if input["value"]["type"] in ["function", "queryAPI"]:
                hash_link = recursive_unpack(
                    input["value"],
                    level + 1,
                    calls,
                    contracts_methods,
                    contracts_ABIs,
                    responses,
                    moonstream_token,
                    v3,
                    customer_id,
                    instance_id,
                )
                input["value"] = hash_link
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
        calls.setdefault(level, []).append(abi)
    else:
        level = 0
        calls.setdefault(level, []).append(abi)

    contracts_methods.setdefault(method_abi["address"], [])
    if generated_hash not in contracts_methods[method_abi["address"]]:
        contracts_methods[method_abi["address"]].append(generated_hash)
        contracts_ABIs.setdefault(method_abi["address"], {})
        contracts_ABIs[method_abi["address"]][generated_hash] = abi

    return generated_hash


def build_interfaces(
    contracts_ABIs: Dict[str, Any], contracts_methods: Dict[str, Any], web3_client: Web3
) -> Dict[str, Any]:
    """Builds contract interfaces."""
    interfaces = {}
    for contract_address in contracts_ABIs:
        abis = [
            contracts_ABIs[contract_address][method_hash]
            for method_hash in contracts_methods[contract_address]
        ]
        interfaces[contract_address] = web3_client.eth.contract(
            address=web3_client.toChecksumAddress(contract_address), abi=abis
        )
    return interfaces


def process_address_field(job: Dict[str, Any], moonstream_token: str) -> List[str]:
    """Processes the address field of a job and returns a list of addresses."""
    if isinstance(job["address"], str):
        return [Web3.toChecksumAddress(job["address"])]
    elif isinstance(job["address"], list):
        return [
            Web3.toChecksumAddress(address) for address in job["address"]
        ]  # manual job multiplication
    elif isinstance(job["address"], dict):
        if job["address"].get("type") == "queryAPI":
            # QueryAPI job multiplication
            addresses = execute_query(job["address"], token=moonstream_token)
            checsum_addresses = []
            for address in addresses:
                try:
                    checsum_addresses.append(Web3.toChecksumAddress(address))
                except Exception as e:
                    logger.error(f"Invalid address: {address}")
                    continue
            return checsum_addresses
        else:
            raise ValueError(f"Invalid address type: {type(job['address'])}")
    else:
        raise ValueError(f"Invalid address type: {type(job['address'])}")


def parse_jobs(
    jobs: List[Any],
    blockchain_type: Any,
    web3_provider_uri: Optional[str],
    block_number: Optional[int],
    batch_size: int,
    moonstream_token: str,
    web3_uri: Optional[str] = None,
    customer_db_uri: Optional[str] = None,
):
    """
    Parses jobs from a list and generates web3 interfaces for each contract.
    """
    contracts_ABIs: Dict[str, Any] = {}
    contracts_methods: Dict[str, Any] = {}
    calls: Dict[int, List[Any]] = {0: []}
    responses: Dict[str, Any] = {}
    db_sessions: Dict[Any, Any] = {}

    web3_client = connect_to_web3(blockchain_type, web3_provider_uri, web3_uri)
    block_number, block_timestamp, block_hash = get_block_info(
        web3_client, block_number
    )

    multicaller = Multicall2(
        web3_client, web3_client.toChecksumAddress(multicall_contracts[blockchain_type])
    )
    multicall_method = multicaller.tryAggregate

    # All sessions are stored in the dictionary db_sessions
    # Under one try block
    try:
        # Process jobs and create session

        for job in jobs:

            ### process address field
            ### Handle case when 1 job represents multiple contracts
            addresses = process_address_field(job, moonstream_token)

            for address in addresses[1:]:
                new_job = job.copy()
                new_job["address"] = address
                jobs.append(new_job)

            job["address"] = addresses[0]

            v3 = job.get("v3", False)
            customer_id = job.get("customer_id")
            instance_id = job.get("instance_id")

            ### DB sessions
            if customer_db_uri is not None:
                if v3 and (customer_id, instance_id) not in db_sessions:
                    # Create session
                    engine = create_moonstream_engine(customer_db_uri, 2, 100000)
                    session = sessionmaker(bind=engine)
                    try:
                        db_sessions[(customer_id, instance_id)] = session()
                    except Exception as e:
                        logger.error(f"Connection to {engine} failed: {e}")
                        continue
                else:
                    if "v2" not in db_sessions:
                        engine = create_moonstream_engine(customer_db_uri, 2, 100000)
                        db_sessions["v2"] = sessionmaker(bind=engine)()
            elif v3:
                if (customer_id, instance_id) not in db_sessions:
                    # Create session
                    # Assume fetch_connection_string fetches the connection string
                    connection_string = request_connection_string(
                        customer_id=customer_id,
                        instance_id=instance_id,
                        token=moonstream_token,
                    )
                    engine = create_moonstream_engine(connection_string, 2, 100000)
                    session = sessionmaker(bind=engine)
                    try:
                        db_sessions[(customer_id, instance_id)] = session()
                    except Exception as e:
                        logger.error(f"Connection to {engine} failed: {e}")
                        continue
            else:
                if "v2" not in db_sessions:
                    db_sessions["v2"] = PrePing_SessionLocal()

            if job["address"] not in contracts_ABIs:
                contracts_ABIs[job["address"]] = {}

            recursive_unpack(
                job,
                0,
                calls,
                contracts_methods,
                contracts_ABIs,
                responses,
                moonstream_token,
                v3,
                customer_id,
                instance_id,
            )

        interfaces = build_interfaces(contracts_ABIs, contracts_methods, web3_client)

        call_tree_levels = sorted(calls.keys(), reverse=True)[:-1]

        logger.info(f"Crawl level: 0. Jobs amount: {len(calls[0])}")
        logger.info(f"Call tree levels: {call_tree_levels}")

        batch_size = crawl_calls_level(
            web3_client=web3_client,
            db_sessions=db_sessions,
            calls=calls[0],
            responses=responses,
            contracts_ABIs=contracts_ABIs,
            interfaces=interfaces,
            batch_size=batch_size,
            multicall_method=multicall_method,
            block_number=block_number,  # type: ignore
            blockchain_type=blockchain_type,
            block_timestamp=block_timestamp,
            block_hash=block_hash,
        )

        for level in call_tree_levels:
            logger.info(f"Crawl level: {level}. Jobs amount: {len(calls[level])}")
            batch_size = crawl_calls_level(
                web3_client=web3_client,
                db_sessions=db_sessions,
                calls=calls[level],
                responses=responses,
                contracts_ABIs=contracts_ABIs,
                interfaces=interfaces,
                batch_size=batch_size,
                multicall_method=multicall_method,
                block_number=block_number,  # type: ignore
                blockchain_type=blockchain_type,
                block_timestamp=block_timestamp,
                block_hash=block_hash,
            )
    finally:
        # Close all sessions
        for session in db_sessions.values():
            try:
                session.close()
            except Exception as e:
                logger.error(f"Failed to close session: {e}")


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
        args.customer_db_uri,
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

    logger.info(f"Existing jobs: {len(existing_jobs)}")
    logger.info(f"New jobs: {jobs}")

    ### validate existing jobs
    for bugout_job in existing_jobs:

        try:
            if bugout_job.content is None:
                logger.error(f"Job content is None for entry {bugout_job.entry_url}")
                continue
            ### parse json
            job_content = json.loads(bugout_job.content)
            ### validate via ViewTasks
            ViewTasks(**job_content)
        except Exception as e:

            logger.error(f"Job validation of entry {bugout_job.entry_url} failed: {e}")
            continue

        ### from tags get blockchain, name and address

        for tag in bugout_job.tags:
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
    view_state_crawler_parser.add_argument(
        "--customer-db-uri",
        type=str,
        help="URI for the customer database",
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
