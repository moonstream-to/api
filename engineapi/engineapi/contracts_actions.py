import argparse
import json
import logging
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple

from bugout.data import BugoutResourceHolder, HolderType
from sqlalchemy import func, or_, text, tuple_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Row
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from web3 import Web3

from . import data, db
from .models import (
    Blockchain,
    CallRequest,
    CallRequestType,
    MetatxRequester,
    RegisteredContract,
)
from .settings import (
    METATX_REQUESTER_TYPE,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_APPLICATION_ID,
    bugout_client,
    bugout_client_semaphore,
)

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


class UnsupportedCallRequestType(Exception):
    """
    Raised when unsupported call request type specified.
    """


class UnsupportedBlockchain(Exception):
    """
    Raised when unsupported blockchain specified.
    """


class CallRequestMethodValueError(Exception):
    """
    Raised when method not acceptable for specified request type.
    """


class CallRequestRequiredParamsValueError(Exception):
    """
    Raised when required params not acceptable for specified request type.
    """


class ContractAlreadyRegistered(Exception):
    pass


class CallRequestAlreadyRegistered(Exception):
    """
    Raised when call request with same parameters registered.
    """


class CallRequestIdDuplicates(Exception):
    """
    Raised when same call request IDs passed in one request.
    """


class MetatxRequestersNotFound(Exception):
    """
    Raised when metatx requesters is not found in Brood resources.
    """


def parse_registered_contract_holders_response(
    bugout_holder: BugoutResourceHolder, name: Optional[str] = None
) -> data.RegisteredContractHolderResponse:
    holder = data.RegisteredContractHolderResponse(
        holder_id=bugout_holder.id,
        holder_type=bugout_holder.holder_type.value,
        permissions=[p.value for p in bugout_holder.permissions],
    )
    if name is not None:
        holder.name = name

    return holder


def parse_registered_contract_response(
    obj: Tuple[RegisteredContract, Blockchain]
) -> data.RegisteredContractResponse:
    return data.RegisteredContractResponse(
        id=obj[0].id,
        blockchain=obj[1].name,
        chain_id=obj[1].chain_id,
        address=obj[0].address,
        metatx_requester_id=obj[0].metatx_requester_id,
        title=obj[0].title,
        description=obj[0].description,
        image_uri=obj[0].image_uri,
        created_at=obj[0].created_at,
        updated_at=obj[0].updated_at,
    )


def parse_call_request_response(
    obj: Tuple[CallRequest, RegisteredContract]
) -> data.CallRequestResponse:
    return data.CallRequestResponse(
        id=obj[0].id,
        contract_id=obj[0].registered_contract_id,
        contract_address=obj[1].address,
        metatx_requester_id=obj[0].metatx_requester_id,
        call_request_type=obj[0].call_request_type_name,
        caller=obj[0].caller,
        method=obj[0].method,
        request_id=str(obj[0].request_id),
        parameters=obj[0].parameters,
        tx_hash=obj[0].tx_hash,
        expires_at=obj[0].expires_at,
        live_at=obj[0].live_at,
        created_at=obj[0].created_at,
        updated_at=obj[0].updated_at,
    )


def validate_method_and_params(
    call_request_type: str, method: str, parameters: Dict[str, Any]
) -> str:
    """
    Validate the given method and parameters for the specified contract_type.
    """
    if call_request_type == "dropper-v0.2.0":
        if method != "claim":
            raise CallRequestMethodValueError(
                "Method must be 'claim' for dropper contract type"
            )
        required_params = {
            "dropId",
            "blockDeadline",
            "amount",
            "signer",
            "signature",
        }
        if set(parameters.keys()) != required_params:
            raise CallRequestRequiredParamsValueError(
                f"Parameters must have {required_params} keys for dropper contract type"
            )
        try:
            Web3.toChecksumAddress(parameters["signer"])
        except:
            raise InvalidAddressFormat("Parameter signer must be a valid address")

    elif call_request_type == "raw":
        if method != "":
            raise CallRequestMethodValueError(
                "Method must be empty string for raw contract type"
            )
        if set(parameters.keys()) != {"calldata"}:
            raise CallRequestRequiredParamsValueError(
                "Parameters must have only 'calldata' key for raw contract type"
            )

    else:
        raise UnsupportedCallRequestType(f"Unknown contract type {call_request_type}")

    return call_request_type


def create_resource_for_registered_contract(
    registered_contract_id: uuid.UUID, user_id: uuid.UUID
) -> uuid.UUID:
    resource_data = {
        "type": METATX_REQUESTER_TYPE,
        "created_by": str(user_id),
        "registered_contract_id": str(registered_contract_id),
    }

    resource = bugout_client.create_resource(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        application_id=MOONSTREAM_APPLICATION_ID,
        resource_data=resource_data,
    )
    logger.info(
        f"Created resource with ID: {str(resource.id)} for registered contract with ID: {str(registered_contract_id)}"
    )

    _ = bugout_client.add_resource_holder_permissions(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        resource_id=resource.id,
        holder_permissions=BugoutResourceHolder(
            holder_id=str(user_id),
            holder_type="user",
            permissions=["create", "read", "update", "delete"],
        ),
    )
    logger.info(
        f"Granted creator permissions for resource with ID: {str(resource.id)} to metatx requester with ID: {user_id}"
    )

    return resource.id


def delete_resource_for_registered_contract(resource_id: uuid.UUID) -> None:
    try:
        resource = bugout_client.delete_resource(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            resource_id=resource_id,
        )
    except Exception as err:
        logger.error(f"Unable to delete resource with ID: {resource_id}, err: {err}")
        raise

    logger.info(f"Deleted resource with ID: {resource.id} for registered contract")


def delete_metatx_requester(
    db_session: Session, metatx_requester_id: uuid.UUID
) -> None:
    try:
        metatx_requester = (
            db_session.query(MetatxRequester)
            .filter(MetatxRequester.id == metatx_requester_id)
            .one()
        )

        db_session.delete(metatx_requester)
        db_session.commit()
    except Exception as err:
        db_session.rollback()
        logger.error(
            f"Unable to delete metatx requester with ID: {metatx_requester_id}, err: {err}"
        )
        raise

    logger.info(
        f"Deleted metatx requester with ID: {metatx_requester_id} for registered contract"
    )


def clean_metatx_requester_id(db_session: Session, metatx_requester_id: uuid.UUID):
    query = db_session.query(RegisteredContract).filter(
        RegisteredContract.metatx_requester_id == metatx_requester_id
    )
    r_contracts = query.all()

    if len(r_contracts) == 0:
        delete_resource_for_registered_contract(resource_id=metatx_requester_id)

        delete_metatx_requester(
            db_session=db_session, metatx_requester_id=metatx_requester_id
        )


def extend_bugout_holder(
    holder: BugoutResourceHolder,
) -> data.RegisteredContractHolderResponse:
    bugout_client_semaphore.acquire()
    try:
        if holder.holder_type == HolderType.user:
            user = bugout_client.find_user(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN, user_id=holder.id
            )
            return parse_registered_contract_holders_response(
                bugout_holder=holder, name=user.username
            )
        elif holder.holder_type == HolderType.group:
            group = bugout_client.find_group(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN, group_id=holder.id
            )
            return parse_registered_contract_holders_response(
                bugout_holder=holder, name=group.group_name
            )
    finally:
        bugout_client_semaphore.release()


def fetch_metatx_requester_holders(
    resource_id: uuid.UUID, extended: bool = False
) -> List[data.RegisteredContractHolderResponse]:

    holders = bugout_client.get_resource_holders(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        resource_id=resource_id,
    )

    parsed_holders: List[data.RegisteredContractHolderResponse] = []
    if extended is True:
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(extend_bugout_holder, h) for h in holders.holders
            ]

            for future in as_completed(futures):
                try:
                    result = future.result()
                    parsed_holders.append(result)
                except Exception as err:
                    logger.error(str(err))
    else:
        parsed_holders = [
            parse_registered_contract_holders_response(bugout_holder=h)
            for h in holders.holders
        ]

    return parsed_holders


def add_metatx_requester_holder(
    resource_id: uuid.UUID, holder_permissions: BugoutResourceHolder
) -> List[data.RegisteredContractHolderResponse]:
    holders = bugout_client.add_resource_holder_permissions(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        resource_id=resource_id,
        holder_permissions=holder_permissions,
    )
    parsed_holders = [
        parse_registered_contract_holders_response(bugout_holder=h)
        for h in holders.holders
    ]

    return parsed_holders


def delete_metatx_requester_holder(
    resource_id: uuid.UUID, holder_permissions: BugoutResourceHolder
) -> List[data.RegisteredContractHolderResponse]:
    holders = bugout_client.delete_resource_holder_permissions(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        resource_id=resource_id,
        holder_permissions=holder_permissions,
    )
    parsed_holders = [
        parse_registered_contract_holders_response(bugout_holder=h)
        for h in holders.holders
    ]

    return parsed_holders


def register_contract(
    db_session: Session,
    blockchain_name: str,
    address: str,
    user_id: uuid.UUID,
    title: Optional[str],
    description: Optional[str],
    image_uri: Optional[str],
) -> Tuple[RegisteredContract, Blockchain]:
    """
    Register a contract against the Engine instance
    """
    blockchain = (
        db_session.query(Blockchain)
        .filter(Blockchain.name == blockchain_name)
        .one_or_none()
    )

    if blockchain is None:
        raise UnsupportedBlockchain("Unsupported blockchain specified")

    registered_contract_id = uuid.uuid4()

    try:
        resource_id = create_resource_for_registered_contract(
            registered_contract_id=registered_contract_id, user_id=user_id
        )
    except Exception as err:
        logger.error(repr(err))
        raise Exception(
            f"Unhandled exception during resource creation for user with ID: {str(user_id)}"
        )

    try:
        metatx_requester_stmt = insert(MetatxRequester.__table__).values(id=resource_id)
        db_session.execute(metatx_requester_stmt)

        contract = RegisteredContract(
            id=registered_contract_id,
            blockchain_id=blockchain.id,
            address=Web3.toChecksumAddress(address),
            metatx_requester_id=resource_id,
            title=title,
            description=description,
            image_uri=image_uri,
        )
        db_session.add(contract)
        db_session.commit()
    except IntegrityError as err:
        db_session.rollback()
        delete_resource_for_registered_contract(resource_id=resource_id)
        raise ContractAlreadyRegistered()
    except Exception as err:
        db_session.rollback()
        delete_resource_for_registered_contract(resource_id=resource_id)
        logger.error(repr(err))
        raise Exception(
            f"Unhandled exception during creating new registered contract for user with ID: {str(user_id)}"
        )

    return (contract, blockchain)


def update_registered_contract(
    db_session: Session,
    metatx_requester_ids: List[uuid.UUID],
    contract_id: uuid.UUID,
    title: Optional[str] = None,
    description: Optional[str] = None,
    image_uri: Optional[str] = None,
    ignore_nulls: bool = True,
) -> Tuple[RegisteredContract, Blockchain]:
    """
    Update the registered contract with the given contract ID provided that the user with metatx_requester_id
    has access to it.
    """
    contract_with_blockchain = (
        db_session.query(RegisteredContract, Blockchain)
        .join(Blockchain, Blockchain.id == RegisteredContract.blockchain_id)
        .filter(
            RegisteredContract.id == contract_id,
            RegisteredContract.metatx_requester_id.in_(metatx_requester_ids),
        )
        .one()
    )
    registered_contract, blockchain = contract_with_blockchain

    if not (title is None and ignore_nulls):
        registered_contract.title = title
    if not (description is None and ignore_nulls):
        registered_contract.description = description
    if not (image_uri is None and ignore_nulls):
        registered_contract.image_uri = image_uri

    try:
        db_session.add(registered_contract)
        db_session.commit()
    except Exception as err:
        logger.error(
            f"update_registered_contract -- error storing update in database: {repr(err)}"
        )
        db_session.rollback()
        raise

    return (registered_contract, blockchain)


def get_registered_contract(
    db_session: Session,
    metatx_requester_ids: List[uuid.UUID],
    contract_id: uuid.UUID,
) -> Tuple[RegisteredContract, Blockchain]:
    """
    Get registered contract by ID.
    """
    contract_with_blockchain = (
        db_session.query(RegisteredContract, Blockchain)
        .join(Blockchain, Blockchain.id == RegisteredContract.blockchain_id)
        .filter(RegisteredContract.metatx_requester_id.in_(metatx_requester_ids))
        .filter(RegisteredContract.id == contract_id)
        .one()
    )
    registered_contract, blockchain = contract_with_blockchain

    return (registered_contract, blockchain)


def lookup_registered_contracts(
    db_session: Session,
    metatx_requester_ids: List[uuid.UUID],
    blockchain: Optional[str] = None,
    address: Optional[str] = None,
    limit: int = 10,
    offset: Optional[int] = None,
) -> List[Row[Tuple[RegisteredContract, Blockchain]]]:
    """
    Lookup a registered contract
    """
    query = (
        db_session.query(RegisteredContract, Blockchain)
        .join(Blockchain, Blockchain.id == RegisteredContract.blockchain_id)
        .filter(RegisteredContract.metatx_requester_id.in_(metatx_requester_ids))
    )

    if blockchain is not None:
        query = query.filter(Blockchain.name == blockchain)

    if address is not None:
        query = query.filter(
            RegisteredContract.address == Web3.toChecksumAddress(address)
        )

    if offset is not None:
        query = query.offset(offset)

    contracts_with_blockchain = query.limit(limit).all()

    return contracts_with_blockchain


def delete_registered_contract(
    db_session: Session,
    metatx_requester_ids: List[uuid.UUID],
    registered_contract_id: uuid.UUID,
) -> Tuple[RegisteredContract, Blockchain]:
    """
    Delete a registered contract
    """

    try:
        contract_with_blockchain = (
            db_session.query(RegisteredContract, Blockchain)
            .join(Blockchain, Blockchain.id == RegisteredContract.blockchain_id)
            .filter(RegisteredContract.metatx_requester_id.in_(metatx_requester_ids))
            .filter(RegisteredContract.id == registered_contract_id)
            .one()
        )
        contract = contract_with_blockchain[0]

        db_session.delete(contract)
        db_session.commit()
    except Exception as err:
        db_session.rollback()
        logger.error(repr(err))
        raise

    registered_contract, blockchain = contract_with_blockchain

    return (registered_contract, blockchain)


def create_request_calls(
    db_session: Session,
    metatx_requester_ids: List[uuid.UUID],
    registered_contract_id: Optional[uuid.UUID],
    contract_address: Optional[str],
    call_specs: List[data.CallSpecification],
    ttl_days: Optional[int] = None,
    live_at: Optional[int] = None,
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

    if live_at is not None:
        assert live_at == int(live_at)
        if live_at <= 0:
            raise ValueError("live_at must be positive")

    # Check that the moonstream_user_id matches a RegisteredContract with the given id or address
    query = db_session.query(RegisteredContract).filter(
        RegisteredContract.metatx_requester_id.in_(metatx_requester_ids)
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
        raise ValueError("Invalid registered_contract_id or metatx_requester_ids")

    # Normalize the caller argument using Web3.toChecksumAddress
    for specification in call_specs:
        normalized_caller = Web3.toChecksumAddress(specification.caller)

        # Validate the method and parameters for the contract_type
        try:
            call_request_type = validate_method_and_params(
                call_request_type=specification.call_request_type,
                method=specification.method,
                parameters=specification.parameters,
            )
        except UnsupportedCallRequestType as err:
            raise UnsupportedCallRequestType(err)
        except CallRequestMethodValueError as err:
            raise CallRequestMethodValueError(err)
        except CallRequestRequiredParamsValueError as err:
            raise CallRequestRequiredParamsValueError(err)
        except InvalidAddressFormat as err:
            raise InvalidAddressFormat(err)
        except Exception as err:
            logger.error(
                f"Unhandled error occurred during methods and parameters validation, err: {err}"
            )
            raise Exception()

        expires_at = None
        if ttl_days is not None:
            expires_at = func.now() + timedelta(days=ttl_days)

        request = CallRequest(
            registered_contract_id=registered_contract.id,
            call_request_type_name=call_request_type,
            metatx_requester_id=registered_contract.metatx_requester_id,
            caller=normalized_caller,
            method=specification.method,
            request_id=specification.request_id,
            parameters=specification.parameters,
            expires_at=expires_at,
            live_at=datetime.fromtimestamp(live_at) if live_at is not None else None,
        )

        db_session.add(request)
    # Insert the new rows into the database in a single transaction
    try:
        db_session.commit()
    except IntegrityError as err:
        db_session.rollback()
        raise CallRequestAlreadyRegistered()
    except Exception as e:
        db_session.rollback()
        raise e

    return len(call_specs)


def get_call_request_from_tuple(
    db_session: Session,
    metatx_requester_ids: List[uuid.UUID],
    requests: Set[Tuple[str, str]],
    contract_id: Optional[uuid.UUID] = None,
    contract_address: Optional[str] = None,
) -> List[CallRequest]:
    if contract_id is None and contract_address is None:
        raise ValueError(
            "At least one of contract_id or contract_address must be specified"
        )
    query = (
        db_session.query(CallRequest)
        .join(
            RegisteredContract,
            CallRequest.registered_contract_id == RegisteredContract.id,
        )
        .filter(RegisteredContract.metatx_requester_id.in_(metatx_requester_ids))
        .filter(tuple_(CallRequest.caller, CallRequest.request_id).in_(requests))
    )
    if contract_id is not None:
        query = query.filter(RegisteredContract.id == contract_id)
    if contract_address is not None:
        query = query.filter(
            RegisteredContract.address == Web3.toChecksumAddress(contract_address)
        )

    existing_requests = query.all()

    return existing_requests


def get_call_request(
    db_session: Session,
    request_id: uuid.UUID,
) -> Tuple[CallRequest, RegisteredContract]:
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
            f"Incorrect number of results found for request_id {request_id}"
        )

    call_request, registered_contract = results[0]

    return (call_request, registered_contract)


def list_blockchains(
    db_session: Session,
) -> List[Blockchain]:
    blockchains = db_session.query(Blockchain).all()
    return blockchains


def list_call_request_types(
    db_session: Session,
) -> List[CallRequestType]:
    call_request_types = db_session.query(CallRequestType).all()
    return call_request_types


def list_call_requests(
    db_session: Session,
    contract_id: Optional[uuid.UUID],
    contract_address: Optional[str],
    caller: Optional[str],
    limit: int = 10,
    offset: Optional[int] = None,
    show_expired: bool = False,
    live_after: Optional[int] = None,
    metatx_requester_ids: List[uuid.UUID] = [],
) -> List[Row[Tuple[CallRequest, RegisteredContract, CallRequestType]]]:
    """
    List call requests.

    Argument moonstream_user_id took from authorization workflow. And if it is specified
    then user has access to call_requests before live_at param.
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

    # If user id not specified, do not show call_requests before live_at.
    # Otherwise check show_before_live_at argument from query parameter
    if len(metatx_requester_ids) != 0:
        query = query.filter(
            CallRequest.metatx_requester_id.in_(metatx_requester_ids),
        )
    else:
        query = query.filter(
            or_(CallRequest.live_at < func.now(), CallRequest.live_at == None)
        )

    if live_after is not None:
        assert live_after == int(live_after)
        if live_after <= 0:
            raise ValueError("live_after must be positive")
        query = query.filter(CallRequest.live_at >= datetime.fromtimestamp(live_after))

    if offset is not None:
        query = query.offset(offset)

    query = query.limit(limit)
    results = query.all()
    return results


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
    metatx_requester_ids: List[uuid.UUID],
    request_ids: List[uuid.UUID] = [],
) -> int:
    """
    Delete a requests.
    """
    try:
        requests_to_delete_query = (
            db_session.query(CallRequest)
            .filter(CallRequest.metatx_requester_id.in_(metatx_requester_ids))
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


def complete_call_request(
    db_session: Session,
    tx_hash: str,
    call_request_id: uuid.UUID,
    caller: str,
) -> CallRequest:
    results = (
        db_session.query(CallRequest, RegisteredContract)
        .join(
            RegisteredContract,
            CallRequest.registered_contract_id == RegisteredContract.id,
        )
        .filter(CallRequest.id == call_request_id)
        .filter(CallRequest.caller == caller)
        .all()
    )

    if len(results) == 0:
        raise CallRequestNotFound("Call request with given ID not found")
    elif len(results) != 1:
        raise Exception(
            f"Incorrect number of results found for request_id {call_request_id}"
        )
    call_request, registered_contract = results[0]

    call_request.tx_hash = tx_hash

    try:
        db_session.add(call_request)
        db_session.commit()
    except Exception as err:
        logger.error(
            f"complete_call_request -- error updating in database: {repr(err)}"
        )
        db_session.rollback()
        raise

    return (call_request, registered_contract)


def fetch_metatx_requester_ids(token: uuid.UUID) -> List[uuid.UUID]:
    params = {"type": "metatx_requester"}

    try:
        resources = bugout_client.list_resources(token=token, params=params)
    except Exception as err:
        logger.error("Failed to list resources")
        raise Exception(err)

    if len(resources.resources) == 0:
        raise MetatxRequestersNotFound(
            "No metatx requesters for specific user available"
        )

    metatx_requester_ids = [r.id for r in resources.resources]

    return metatx_requester_ids


def count_contracts_and_requests_for_requester(
    db_session: Session, metatx_requester_ids: List[uuid.UUID]
) -> List[data.MetatxRequestersResponse]:
    registered_contracts_subquery = (
        db_session.query(
            RegisteredContract.metatx_requester_id,
            func.count(RegisteredContract.id).label("registered_contracts_count"),
        )
        .filter(RegisteredContract.metatx_requester_id.in_(metatx_requester_ids))
        .group_by(RegisteredContract.metatx_requester_id)
        .subquery()
    )
    call_requests_subquery = (
        db_session.query(
            CallRequest.metatx_requester_id,
            func.count(CallRequest.id).label("call_requests_count"),
        )
        .filter(CallRequest.metatx_requester_id.in_(metatx_requester_ids))
        .group_by(CallRequest.metatx_requester_id)
        .subquery()
    )

    query = db_session.query(
        registered_contracts_subquery.c.metatx_requester_id,
        registered_contracts_subquery.c.registered_contracts_count,
        call_requests_subquery.c.call_requests_count,
    ).outerjoin(
        call_requests_subquery,
        registered_contracts_subquery.c.metatx_requester_id
        == call_requests_subquery.c.metatx_requester_id,
    )

    results = query.all()

    metatx_requesters: List[data.MetatxRequestersResponse] = []
    for r in results:
        metatx_requester_id = r[0]
        metatx_requesters.append(
            data.MetatxRequestersResponse(
                metatx_requester_id=metatx_requester_id,
                registered_contracts_count=r[1],
                call_requests_count=r[2],
            )
        )

        metatx_requester_ids.remove(metatx_requester_id)

    # Add empty metatx requesters
    for r_id in metatx_requester_ids:
        metatx_requesters.append(
            data.MetatxRequestersResponse(
                metatx_requester_id=r_id,
                registered_contracts_count=0,
                call_requests_count=0,
            )
        )

    return metatx_requesters


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
                user_id=args.user_id,
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
                metatx_requester_ids=[args.resource_id],
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
                moonstream_user_ids=[args.resource_id],
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
            create_request_calls(
                db_session=db_session,
                metatx_requester_ids=[args.resource_id],
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
        required=False,
        default=None,
        help="The type of the contract",
    )
    list_contracts_parser.add_argument(
        "-r",
        "--resource-id",
        type=uuid.UUID,
        required=True,
        help="The ID of the Bugout resource representing metatx requester whose contracts to list",
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
        "-r",
        "--resource-id",
        type=uuid.UUID,
        required=True,
        help="The ID of the Bugout resource representing metatx requester whose contract to delete",
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
        "-r",
        "--resource-id",
        type=uuid.UUID,
        required=True,
        help="The ID of the Bugout resource representing metatx requester who owns the contract",
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
