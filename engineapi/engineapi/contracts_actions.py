import argparse
import json
import logging
import uuid
from datetime import timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import func, text
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from web3 import Web3

from . import data, db
from .data import ContractType
from .models import CallRequest, RegisteredContract

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CallRequestNotFound(Exception):
    """
    Raised when call request with the given parameters is not found in the database.
    """


class InvalidAddressFormat(Exception):
    """
    Raised when address not pass web3checksum validation.
    """


class ContractAlreadyRegistered(Exception):
    pass


def validate_method_and_params(
    contract_type: ContractType, method: str, parameters: Dict[str, Any]
) -> None:
    """
    Validate the given method and parameters for the specified contract_type.
    """
    if contract_type == ContractType.raw:
        if method != "":
            raise ValueError("Method must be empty string for raw contract type")
        if set(parameters.keys()) != {"calldata"}:
            raise ValueError(
                "Parameters must have only 'calldata' key for raw contract type"
            )
    elif contract_type == ContractType.dropper:
        if method != "claim":
            raise ValueError("Method must be 'claim' for dropper contract type")
        required_params = {
            "dropId",
            "requestID",
            "blockDeadline",
            "amount",
            "signer",
            "signature",
        }
        if set(parameters.keys()) != required_params:
            raise ValueError(
                f"Parameters must have {required_params} keys for dropper contract type"
            )
        try:
            Web3.toChecksumAddress(parameters["signer"])
        except:
            raise InvalidAddressFormat("Parameter signer must be a valid address")
    else:
        raise ValueError(f"Unknown contract type {contract_type}")


def register_contract(
    db_session: Session,
    blockchain: str,
    address: str,
    contract_type: ContractType,
    moonstream_user_id: uuid.UUID,
    title: Optional[str],
    description: Optional[str],
    image_uri: Optional[str],
) -> data.RegisteredContract:
    """
    Register a contract against the Engine instance
    """
    try:
        contract = RegisteredContract(
            blockchain=blockchain,
            address=Web3.toChecksumAddress(address),
            contract_type=contract_type.value,
            moonstream_user_id=moonstream_user_id,
            title=title,
            description=description,
            image_uri=image_uri,
        )
        db_session.add(contract)
        db_session.commit()
    except IntegrityError as err:
        db_session.rollback()
        raise ContractAlreadyRegistered()
    except Exception as err:
        db_session.rollback()
        logger.error(repr(err))
        raise

    return contract


def update_registered_contract(
    db_session: Session,
    moonstream_user_id: uuid.UUID,
    contract_id: uuid.UUID,
    title: Optional[str] = None,
    description: Optional[str] = None,
    image_uri: Optional[str] = None,
    ignore_nulls: bool = True,
) -> data.RegisteredContract:
    """
    Update the registered contract with the given contract ID provided that the user with moonstream_user_id
    has access to it.
    """
    query = db_session.query(RegisteredContract).filter(
        RegisteredContract.id == contract_id,
        RegisteredContract.moonstream_user_id == moonstream_user_id,
    )

    contract = query.one()

    if not (title is None and ignore_nulls):
        contract.title = title
    if not (description is None and ignore_nulls):
        contract.description = description
    if not (image_uri is None and ignore_nulls):
        contract.image_uri = image_uri

    try:
        db_session.add(contract)
        db_session.commit()
    except Exception as err:
        logger.error(
            f"update_registered_contract -- error storing update in database: {repr(err)}"
        )
        db_session.rollback()
        raise

    return contract


def get_registered_contract(
    db_session: Session,
    moonstream_user_id: uuid.UUID,
    contract_id: uuid.UUID,
) -> RegisteredContract:
    """
    Get registered contract by ID.
    """
    contract = (
        db_session.query(RegisteredContract)
        .filter(RegisteredContract.moonstream_user_id == moonstream_user_id)
        .filter(RegisteredContract.id == contract_id)
        .one()
    )
    return contract


def lookup_registered_contracts(
    db_session: Session,
    moonstream_user_id: uuid.UUID,
    blockchain: Optional[str] = None,
    address: Optional[str] = None,
    contract_type: Optional[ContractType] = None,
    limit: int = 10,
    offset: Optional[int] = None,
) -> List[RegisteredContract]:
    """
    Lookup a registered contract
    """
    query = db_session.query(RegisteredContract).filter(
        RegisteredContract.moonstream_user_id == moonstream_user_id
    )

    if blockchain is not None:
        query = query.filter(RegisteredContract.blockchain == blockchain)

    if address is not None:
        query = query.filter(
            RegisteredContract.address == Web3.toChecksumAddress(address)
        )

    if contract_type is not None:
        query = query.filter(RegisteredContract.contract_type == contract_type.value)

    if offset is not None:
        query = query.offset(offset)

    query = query.limit(limit)

    return query.all()


def delete_registered_contract(
    db_session: Session,
    moonstream_user_id: uuid.UUID,
    registered_contract_id: uuid.UUID,
) -> RegisteredContract:
    """
    Delete a registered contract
    """
    try:
        registered_contract = (
            db_session.query(RegisteredContract)
            .filter(RegisteredContract.moonstream_user_id == moonstream_user_id)
            .filter(RegisteredContract.id == registered_contract_id)
            .one()
        )

        db_session.delete(registered_contract)
        db_session.commit()
    except Exception as err:
        db_session.rollback()
        logger.error(repr(err))
        raise

    return registered_contract


def request_calls(
    db_session: Session,
    moonstream_user_id: uuid.UUID,
    registered_contract_id: Optional[uuid.UUID],
    contract_address: Optional[str],
    call_specs: List[data.CallSpecification],
    ttl_days: Optional[int] = None,
) -> int:
    """
    Batch creates call requests for the given registered contract.
    """
    # TODO(zomglings): Do not pass raw ttl_days into SQL query - could be subject to SQL injection
    # For now, in the interest of speed, let us just be super cautious with ttl_days.
    # Check that the ttl_days is indeed an integer
    if registered_contract_id is None and contract_address is None:
        raise ValueError(
            "At least one of registered_contract_id or contract_address is required"
        )

    if ttl_days is not None:
        assert ttl_days == int(ttl_days), "ttl_days must be an integer"
        if ttl_days <= 0:
            raise ValueError("ttl_days must be positive")

    # Check that the moonstream_user_id matches a RegisteredContract with the given id or address
    query = db_session.query(RegisteredContract).filter(
        RegisteredContract.moonstream_user_id == moonstream_user_id
    )

    if registered_contract_id is not None:
        query = query.filter(RegisteredContract.id == registered_contract_id)

    if contract_address is not None:
        query = query.filter(
            RegisteredContract.address == Web3.toChecksumAddress(contract_address)
        )

    try:
        registered_contract = query.one()
    except NoResultFound:
        raise ValueError("Invalid registered_contract_id or moonstream_user_id")

    # Normalize the caller argument using Web3.toChecksumAddress
    contract_type = ContractType(registered_contract.contract_type)
    for specification in call_specs:
        normalized_caller = Web3.toChecksumAddress(specification.caller)

        # Validate the method and parameters for the contract_type
        try:
            validate_method_and_params(
                contract_type, specification.method, specification.parameters
            )
        except InvalidAddressFormat as err:
            raise InvalidAddressFormat(err)
        except Exception as err:
            logger.error(
                f"Unhandled error occurred during methods and parameters validation, err: {err}"
            )

        expires_at = None
        if ttl_days is not None:
            expires_at = func.now() + timedelta(days=ttl_days)

        request = CallRequest(
            registered_contract_id=registered_contract.id,
            caller=normalized_caller,
            moonstream_user_id=moonstream_user_id,
            method=specification.method,
            parameters=specification.parameters,
            expires_at=expires_at,
        )

        db_session.add(request)
    # Insert the new rows into the database in a single transaction
    try:
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e

    return len(call_specs)


def get_call_requests(
    db_session: Session,
    request_id: uuid.UUID,
) -> data.CallRequest:
    """
    Get call request by ID.
    """
    results = (
        db_session.query(CallRequest, RegisteredContract)
        .join(
            RegisteredContract,
            CallRequest.registered_contract_id == RegisteredContract.id,
        )
        .filter(CallRequest.id == request_id)
        .all()
    )
    if len(results) == 0:
        raise CallRequestNotFound("Call request with given ID not found")
    elif len(results) != 1:
        raise Exception(
            f"Incorrect number of results found for moonstream_user_id {moonstream_user_id} and request_id {request_id}"
        )
    return data.CallRequest(
        contract_address=results[0][1].address, **results[0][0].__dict__
    )


def list_call_requests(
    db_session: Session,
    contract_id: Optional[uuid.UUID],
    contract_address: Optional[str],
    caller: Optional[str],
    limit: int = 10,
    offset: Optional[int] = None,
    show_expired: bool = False,
) -> List[data.CallRequest]:
    """
    List call requests for the given moonstream_user_id
    """
    if caller is None:
        raise ValueError("caller must be specified")

    if contract_id is None and contract_address is None:
        raise ValueError(
            "At least one of contract_id or contract_address must be specified"
        )

    # If show_expired is False, filter out expired requests using current time on database server
    query = (
        db_session.query(CallRequest, RegisteredContract)
        .join(
            RegisteredContract,
            CallRequest.registered_contract_id == RegisteredContract.id,
        )
        .filter(CallRequest.caller == Web3.toChecksumAddress(caller))
    )

    if contract_id is not None:
        query = query.filter(CallRequest.registered_contract_id == contract_id)

    if contract_address is not None:
        query = query.filter(
            RegisteredContract.address == Web3.toChecksumAddress(contract_address)
        )

    if not show_expired:
        query = query.filter(
            CallRequest.expires_at > func.now(),
        )

    if offset is not None:
        query = query.offset(offset)

    query = query.limit(limit)
    results = query.all()
    return [
        data.CallRequest(
            contract_address=registered_contract.address, **call_request.__dict__
        )
        for call_request, registered_contract in results
    ]


# TODO(zomglings): What should the delete functionality for call requests look like?
# - Delete expired requests for a given caller?
# - Delete all requests for a given caller?
# - Delete all requests for a given contract?
# - Delete request by ID?
# Should we implement these all using a single delete method, or a different method for each
# use case?
# Will come back to this once API is live.


def delete_requests(
    db_session: Session,
    moonstream_user_id: uuid.UUID,
    request_ids: List[uuid.UUID] = [],
) -> int:
    """
    Delete a requests.
    """
    try:
        requests_to_delete_query = (
            db_session.query(CallRequest)
            .filter(CallRequest.moonstream_user_id == moonstream_user_id)
            .filter(CallRequest.id.in_(request_ids))
        )
        requests_to_delete_num: int = requests_to_delete_query.delete(
            synchronize_session=False
        )
        db_session.commit()
    except Exception as err:
        db_session.rollback()
        logger.error(repr(err))
        raise Exception("Failed to delete call requests")

    return requests_to_delete_num


def handle_register(args: argparse.Namespace) -> None:
    """
    Handles the register command.
    """
    try:
        with db.yield_db_session_ctx() as db_session:
            contract = register_contract(
                db_session=db_session,
                blockchain=args.blockchain,
                address=args.address,
                contract_type=args.contract_type,
                moonstream_user_id=args.user_id,
                title=args.title,
                description=args.description,
                image_uri=args.image_uri,
            )
    except Exception as err:
        logger.error(err)
        return
    print(contract.json())


def handle_list(args: argparse.Namespace) -> None:
    """
    Handles the list command.
    """
    try:
        with db.yield_db_session_ctx() as db_session:
            contracts = lookup_registered_contracts(
                db_session=db_session,
                moonstream_user_id=args.user_id,
                blockchain=args.blockchain,
                address=args.address,
                contract_type=args.contract_type,
                limit=args.limit,
                offset=args.offset,
            )
    except Exception as err:
        logger.error(err)
        return

    print(json.dumps([contract.dict() for contract in contracts]))


def handle_delete(args: argparse.Namespace) -> None:
    """
    Handles the delete command.
    """
    try:
        with db.yield_db_session_ctx() as db_session:
            deleted_contract = delete_registered_contract(
                db_session=db_session,
                registered_contract_id=args.id,
                moonstream_user_id=args.user_id,
            )
    except Exception as err:
        logger.error(err)
        return

    print(deleted_contract.json())


def handle_request_calls(args: argparse.Namespace) -> None:
    """
    Handles the request-calls command.

    Reads a file of JSON-formatted call specifications from `args.call_specs`,
    validates them, and adds them to the call_requests table in the Engine database.

    :param args: The arguments passed to the CLI command.
    """
    with args.call_specs as ifp:
        try:
            call_specs_raw = json.load(ifp)
        except Exception as e:
            logger.error(f"Failed to load call specs: {e}")
            return

        call_specs = [data.CallSpecification(**spec) for spec in call_specs_raw]

    try:
        with db.yield_db_session_ctx() as db_session:
            request_calls(
                db_session=db_session,
                moonstream_user_id=args.moonstream_user_id,
                registered_contract_id=args.registered_contract_id,
                call_specs=call_specs,
                ttl_days=args.ttl_days,
            )
    except Exception as e:
        logger.error(f"Failed to request calls: {e}")
        return


def handle_list_requests(args: argparse.Namespace) -> None:
    """
    Handles the requests command.

    :param args: The arguments passed to the CLI command.
    """
    try:
        with db.yield_db_session_ctx() as db_session:
            call_requests = list_call_requests(
                db_session=db_session,
                contract_id=args.registered_contract_id,
                caller=args.caller,
                limit=args.limit,
                offset=args.offset,
                show_expired=args.show_expired,
            )
    except Exception as e:
        logger.error(f"Failed to list call requests: {e}")
        return

    print(json.dumps([request.dict() for request in call_requests]))


def generate_cli() -> argparse.ArgumentParser:
    """
    Generates a CLI which can be used to manage registered contracts on an Engine instance.
    """
    parser = argparse.ArgumentParser(description="Manage registered contracts")
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers()

    register_usage = "Register a new contract"
    register_parser = subparsers.add_parser(
        "register", help=register_usage, description=register_usage
    )
    register_parser.add_argument(
        "-b",
        "--blockchain",
        type=str,
        required=True,
        help="The blockchain the contract is deployed on",
    )
    register_parser.add_argument(
        "-a",
        "--address",
        type=str,
        required=True,
        help="The address of the contract",
    )
    register_parser.add_argument(
        "-c",
        "--contract-type",
        type=ContractType,
        choices=ContractType,
        required=True,
        help="The type of the contract",
    )
    register_parser.add_argument(
        "-u",
        "--user-id",
        type=uuid.UUID,
        required=True,
        help="The ID of the Moonstream user under whom to register the contract",
    )
    register_parser.add_argument(
        "-t",
        "--title",
        type=str,
        required=False,
        default=None,
        help="The title of the contract",
    )
    register_parser.add_argument(
        "-d",
        "--description",
        type=str,
        required=False,
        default=None,
        help="The description of the contract",
    )
    register_parser.add_argument(
        "-i",
        "--image-uri",
        type=str,
        required=False,
        default=None,
        help="The image URI of the contract",
    )
    register_parser.set_defaults(func=handle_register)

    list_contracts_usage = "List all contracts matching certain criteria"
    list_contracts_parser = subparsers.add_parser(
        "list", help=list_contracts_usage, description=list_contracts_usage
    )
    list_contracts_parser.add_argument(
        "-b",
        "--blockchain",
        type=str,
        required=False,
        default=None,
        help="The blockchain the contract is deployed on",
    )
    list_contracts_parser.add_argument(
        "-a",
        "--address",
        type=str,
        required=False,
        default=None,
        help="The address of the contract",
    )
    list_contracts_parser.add_argument(
        "-c",
        "--contract-type",
        type=ContractType,
        choices=ContractType,
        required=False,
        default=None,
        help="The type of the contract",
    )
    list_contracts_parser.add_argument(
        "-u",
        "--user-id",
        type=uuid.UUID,
        required=True,
        help="The ID of the Moonstream user whose contracts to list",
    )
    list_contracts_parser.add_argument(
        "-N",
        "--limit",
        type=int,
        required=False,
        default=10,
        help="The number of contracts to return",
    )
    list_contracts_parser.add_argument(
        "-n",
        "--offset",
        type=int,
        required=False,
        default=0,
        help="The offset to start returning contracts from",
    )
    list_contracts_parser.set_defaults(func=handle_list)

    delete_usage = "Delete a registered contract from an Engine instance"
    delete_parser = subparsers.add_parser(
        "delete", help=delete_usage, description=delete_usage
    )
    delete_parser.add_argument(
        "--id",
        type=uuid.UUID,
        required=True,
        help="The ID of the contract to delete",
    )
    delete_parser.add_argument(
        "-u",
        "--user-id",
        type=uuid.UUID,
        required=True,
        help="The ID of the Moonstream user whose contract to delete",
    )
    delete_parser.set_defaults(func=handle_delete)

    request_calls_usage = "Create call requests for a registered contract"
    request_calls_parser = subparsers.add_parser(
        "request-calls", help=request_calls_usage, description=request_calls_usage
    )
    request_calls_parser.add_argument(
        "-i",
        "--registered-contract-id",
        type=uuid.UUID,
        required=True,
        help="The ID of the registered contract to create call requests for",
    )
    request_calls_parser.add_argument(
        "-u",
        "--moonstream-user-id",
        type=uuid.UUID,
        required=True,
        help="The ID of the Moonstream user who owns the contract",
    )
    request_calls_parser.add_argument(
        "-c",
        "--calls",
        type=argparse.FileType("r"),
        required=True,
        help="Path to the JSON file with call specifications",
    )
    request_calls_parser.add_argument(
        "-t",
        "--ttl-days",
        type=int,
        required=False,
        default=None,
        help="The number of days until the call requests expire",
    )
    request_calls_parser.set_defaults(func=handle_request_calls)

    list_requests_usage = "List requests for calls on a registered contract"
    list_requests_parser = subparsers.add_parser(
        "requests", help=list_requests_usage, description=list_requests_usage
    )
    list_requests_parser.add_argument(
        "-i",
        "--registered-contract-id",
        type=uuid.UUID,
        required=True,
        help="The ID of the registered contract to list call requests for",
    )
    list_requests_parser.add_argument(
        "-c",
        "--caller",
        type=Web3.toChecksumAddress,
        required=True,
        help="Caller's address",
    )
    list_requests_parser.add_argument(
        "-N",
        "--limit",
        type=int,
        required=False,
        default=10,
        help="The number of call requests to return",
    )
    list_requests_parser.add_argument(
        "-n",
        "--offset",
        type=int,
        required=False,
        default=0,
        help="The offset to start returning contracts from",
    )
    list_requests_parser.add_argument(
        "--show-expired",
        action="store_true",
        help="Set this flag to also show expired requests. Default behavior is to hide these.",
    )
    list_requests_parser.set_defaults(func=handle_list_requests)

    return parser


def main() -> None:
    parser = generate_cli()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
