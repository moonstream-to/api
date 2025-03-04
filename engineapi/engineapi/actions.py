from datetime import datetime
from collections import Counter
import json
from typing import List, Any, Optional, Dict, Union, Tuple, cast
import uuid
import logging

from bugout.data import (
    BugoutResource,
    BugoutSearchResult,
    ResourcePermissions,
    HolderType,
    BugoutResourceHolder,
)
from eth_typing import Address
from hexbytes import HexBytes
import requests  # type: ignore
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, Query
from sqlalchemy import func, text, or_, and_, Subquery, literal_column
from sqlalchemy.sql import exists, select, column, table
from sqlalchemy.engine import Row
from web3 import Web3
from web3.types import ChecksumAddress

from .data import (
    Score,
    LeaderboardScore,
    LeaderboardConfigUpdate,
    LeaderboardConfig,
    LeaderboardPosition,
    ColumnsNames,
)
from .contracts import Dropper_interface, ERC20_interface, Terminus_interface
from .models import (
    DropperClaimant,
    DropperContract,
    DropperClaim,
    Leaderboard,
    LeaderboardScores,
    LeaderboardVersion,
)
from . import signatures
from .settings import (
    bugout_client as bc,
    BLOCKCHAIN_WEB3_PROVIDERS,
    LEADERBOARD_RESOURCE_TYPE,
    MOONSTREAM_APPLICATION_ID,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_LEADERBOARD_CONFIGURATION_JOURNAL_ID,
)


class LeaderboardsResourcesNotFound(Exception):
    pass


class AuthorizationError(Exception):
    pass


class DropWithNotSettedBlockDeadline(Exception):
    pass


class DublicateClaimantError(Exception):
    pass


class DuplicateLeaderboardAddressError(Exception):
    def __init__(self, message, duplicates):
        super(DuplicateLeaderboardAddressError, self).__init__(message)
        self.message = message
        self.duplicates = duplicates


class LeaderboardNormalizeScoresError(Exception):
    def __init__(self, message, normilize_errors):
        super(LeaderboardNormalizeScoresError, self).__init__(message)
        self.message = message
        self.normilize_errors = normilize_errors


class LeaderboardPushScoreError(Exception):
    pass


class LeaderboardIsEmpty(Exception):
    pass


class LeaderboardDeleteScoresError(Exception):
    pass


class LeaderboardCreateError(Exception):
    pass


class LeaderboardUpdateError(Exception):
    pass


class LeaderboardDeleteError(Exception):
    pass


class LeaderboardConfigNotFound(Exception):
    pass


class LeaderboardConfigAlreadyActive(Exception):
    pass


class LeaderboardConfigAlreadyInactive(Exception):
    pass


class LeaderboardVersionNotFound(Exception):
    pass


class LeaderboardAssignResourceError(Exception):
    pass


BATCH_SIGNATURE_PAGE_SIZE = 500

logger = logging.getLogger(__name__)


def create_dropper_contract(
    db_session: Session,
    blockchain: Optional[str],
    dropper_contract_address,
    title,
    description,
    image_uri,
):
    """
    Create a new dropper contract.
    """

    dropper_contract = DropperContract(
        blockchain=blockchain,
        address=Web3.toChecksumAddress(dropper_contract_address),
        title=title,
        description=description,
        image_uri=image_uri,
    )
    db_session.add(dropper_contract)
    db_session.commit()
    return dropper_contract


def delete_dropper_contract(
    db_session: Session, blockchain: Optional[str], dropper_contract_address
):
    dropper_contract = (
        db_session.query(DropperContract)
        .filter(
            DropperContract.address == Web3.toChecksumAddress(dropper_contract_address)
        )
        .filter(DropperContract.blockchain == blockchain)
        .one()
    )

    db_session.delete(dropper_contract)
    db_session.commit()
    return dropper_contract


def list_dropper_contracts(
    db_session: Session, blockchain: Optional[str]
) -> List[Dict[str, Any]]:
    """
    List all dropper contracts
    """

    dropper_contracts = []

    dropper_contracts = db_session.query(DropperContract)

    if blockchain:
        dropper_contracts = dropper_contracts.filter(
            DropperContract.blockchain == blockchain
        )

    return dropper_contracts


def get_dropper_contract_by_id(
    db_session: Session, dropper_contract_id: uuid.UUID
) -> DropperContract:
    """
    Get a dropper contract by its ID
    """
    query = db_session.query(DropperContract).filter(
        DropperContract.id == dropper_contract_id
    )
    return query.one()


def list_drops_terminus(db_session: Session, blockchain: Optional[str] = None):
    """
    List distinct of terminus addressess
    """

    terminus = (
        db_session.query(
            DropperClaim.terminus_address,
            DropperClaim.terminus_pool_id,
            DropperContract.blockchain,
        )
        .join(DropperContract)
        .filter(DropperClaim.terminus_address.isnot(None))
        .filter(DropperClaim.terminus_pool_id.isnot(None))
    )
    if blockchain:
        terminus = terminus.filter(DropperContract.blockchain == blockchain)

    terminus = terminus.distinct(
        DropperClaim.terminus_address, DropperClaim.terminus_pool_id
    )

    return terminus


def list_drops_blockchains(db_session: Session):
    """
    List distinct of blockchains
    """

    blockchains = (
        db_session.query(DropperContract.blockchain)
        .filter(DropperContract.blockchain.isnot(None))
        .distinct(DropperContract.blockchain)
    )

    return blockchains


def list_claims(db_session: Session, dropper_contract_id, active=True):
    """
    List all claims
    """

    claims = (
        db_session.query(
            DropperClaim.id,
            DropperClaim.title,
            DropperClaim.description,
            DropperClaim.terminus_address,
            DropperClaim.terminus_pool_id,
            DropperClaim.claim_block_deadline,
        )
        .filter(DropperClaim.dropper_contract_id == dropper_contract_id)
        .filter(DropperClaim.active == active)
        .all()
    )

    return claims


def delete_claim(db_session: Session, dropper_claim_id):
    """
    Delete a claim
    """

    claim = (
        db_session.query(DropperClaim).filter(DropperClaim.id == dropper_claim_id).one()  # type: ignore
    )

    db_session.delete(claim)
    db_session.commit()

    return claim


def create_claim(
    db_session: Session,
    dropper_contract_id: uuid.UUID,
    claim_id: Optional[int] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    terminus_address: Optional[ChecksumAddress] = None,
    terminus_pool_id: Optional[int] = None,
    claim_block_deadline: Optional[int] = None,
):
    """
    Create a new dropper claim.
    """

    # get the dropper contract

    dropper_contract = (
        db_session.query(DropperContract)
        .filter(DropperContract.id == dropper_contract_id)
        .one()
    )

    dropper_claim = DropperClaim(
        dropper_contract_id=dropper_contract.id,
        claim_id=claim_id,
        title=title,
        description=description,
        terminus_address=terminus_address,
        terminus_pool_id=terminus_pool_id,
        claim_block_deadline=claim_block_deadline,
    )
    db_session.add(dropper_claim)
    db_session.commit()
    db_session.refresh(dropper_claim)  # refresh the object to get the id
    return dropper_claim


def activate_drop(db_session: Session, dropper_claim_id: uuid.UUID):
    """
    Activate a claim
    """

    claim = (
        db_session.query(DropperClaim).filter(DropperClaim.id == dropper_claim_id).one()  # type: ignore
    )

    claim.active = True
    db_session.commit()

    return claim


def deactivate_drop(db_session: Session, dropper_claim_id: uuid.UUID):
    """
    Activate a claim
    """

    claim = (
        db_session.query(DropperClaim).filter(DropperClaim.id == dropper_claim_id).one()  # type: ignore
    )

    claim.active = False
    db_session.commit()

    return claim


def update_drop(
    db_session: Session,
    dropper_claim_id: uuid.UUID,
    title: Optional[str] = None,
    description: Optional[str] = None,
    terminus_address: Optional[str] = None,
    terminus_pool_id: Optional[int] = None,
    claim_block_deadline: Optional[int] = None,
    claim_id: Optional[int] = None,
    address: Optional[str] = None,
):
    """
    Update a claim
    """

    claim = (
        db_session.query(DropperClaim).filter(DropperClaim.id == dropper_claim_id).one()  # type: ignore
    )

    if title:
        claim.title = title
    if description:
        claim.description = description
    if terminus_address or terminus_pool_id:
        ensure_dropper_contract_owner(db_session, claim.dropper_contract_id, address)
        if terminus_address:
            terminus_address = Web3.toChecksumAddress(terminus_address)
            claim.terminus_address = terminus_address
        if terminus_pool_id:
            claim.terminus_pool_id = terminus_pool_id
    if claim_block_deadline:
        claim.claim_block_deadline = claim_block_deadline
    if claim_id:
        claim.claim_id = claim_id

    db_session.commit()

    return claim


def get_free_drop_number_in_range(
    db_session: Session, dropper_contract_id: uuid.UUID, start: Optional[int], end: int
):
    """
    Return list of free drops number in range
    """

    if start is None:
        start = 0

    drops = (
        db_session.query(DropperClaim)
        .filter(DropperClaim.dropper_contract_id == dropper_contract_id)
        .filter(DropperClaim.claim_id >= start)
        .filter(DropperClaim.claim_id <= end)
        .all()
    )
    free_numbers = list(range(start, end + 1))
    for drop in drops:
        free_numbers.remove(drop.claim_id)
    return drops


def add_claimants(db_session: Session, dropper_claim_id, claimants, added_by):
    """
    Add a claimants to a claim
    """

    # On conflict requirements https://stackoverflow.com/questions/42022362/no-unique-or-exclusion-constraint-matching-the-on-conflict

    claimant_objects = []

    addresses = [Web3.toChecksumAddress(claimant.address) for claimant in claimants]

    if len(claimants) > len(set(addresses)):
        raise DublicateClaimantError("Duplicate claimants")

    for claimant in claimants:
        claimant_objects.append(
            {
                "dropper_claim_id": dropper_claim_id,
                "address": Web3.toChecksumAddress(claimant.address),
                "amount": 0,
                "raw_amount": str(claimant.amount),
                "added_by": added_by,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        )

    insert_statement = insert(DropperClaimant).values(claimant_objects)

    result_stmt = insert_statement.on_conflict_do_update(
        index_elements=[DropperClaimant.address, DropperClaimant.dropper_claim_id],
        set_=dict(
            amount=insert_statement.excluded.amount,
            raw_amount=insert_statement.excluded.raw_amount,
            added_by=insert_statement.excluded.added_by,
            updated_at=datetime.now(),
        ),
    )
    db_session.execute(result_stmt)
    db_session.commit()

    return claimant_objects


def transform_claim_amount(
    db_session: Session, dropper_claim_id: uuid.UUID, db_amount: int
) -> int:
    claim = (
        db_session.query(
            DropperClaim.claim_id, DropperContract.address, DropperContract.blockchain
        )
        .join(DropperContract, DropperContract.id == DropperClaim.dropper_contract_id)
        .filter(DropperClaim.id == dropper_claim_id)
        .one()
    )
    dropper_contract = Dropper_interface.Contract(
        BLOCKCHAIN_WEB3_PROVIDERS[claim.blockchain], claim.address
    )
    claim_info = dropper_contract.getClaim(claim.claim_id).call()
    if claim_info[0] != 20:
        return db_amount

    erc20_contract = ERC20_interface.Contract(
        BLOCKCHAIN_WEB3_PROVIDERS[claim.blockchain], claim_info[1]
    )
    decimals = int(erc20_contract.decimals().call())

    return db_amount * (10**decimals)


def batch_transform_claim_amounts(
    db_session: Session, dropper_claim_id: uuid.UUID, db_amounts: List[int]
) -> List[int]:
    claim = (
        db_session.query(
            DropperClaim.claim_id, DropperContract.address, DropperContract.blockchain
        )
        .join(DropperContract, DropperContract.id == DropperClaim.dropper_contract_id)
        .filter(DropperClaim.id == dropper_claim_id)
        .one()
    )
    dropper_contract = Dropper_interface.Contract(
        BLOCKCHAIN_WEB3_PROVIDERS[claim.blockchain], claim.address
    )
    claim_info = dropper_contract.getClaim(claim.claim_id)
    if claim_info[0] != 20:
        return db_amounts

    erc20_contract = ERC20_interface.Contract(claim.blockchain, claim_info[1])
    decimals = int(erc20_contract.decimals().call())

    return [db_amount * (10**decimals) for db_amount in db_amounts]


def get_claimants(
    db_session: Session,
    dropper_claim_id: uuid.UUID,
    amount: Optional[int] = None,
    added_by: Optional[str] = None,
    address: Optional[ChecksumAddress] = None,
    limit=None,
    offset=None,
):
    """
    Search for a claimant by address
    """
    claimants_query = db_session.query(
        DropperClaimant.address,
        DropperClaimant.amount,
        DropperClaimant.added_by,
        DropperClaimant.raw_amount,
    ).filter(DropperClaimant.dropper_claim_id == dropper_claim_id)

    if amount:
        claimants_query = claimants_query.filter(DropperClaimant.amount == amount)
    if added_by:
        claimants_query = claimants_query.filter(DropperClaimant.added_by == added_by)
    if address:
        claimants_query = claimants_query.filter(DropperClaimant.address == address)

    if limit:
        claimants_query = claimants_query.limit(limit)

    if offset:
        claimants_query = claimants_query.offset(offset)

    return claimants_query.all()


def get_claimant(db_session: Session, dropper_claim_id, address):
    """
    Search for a claimant by address
    """

    claimant_query = (
        db_session.query(
            DropperClaimant.id.label("dropper_claimant_id"),
            DropperClaimant.address,
            DropperClaimant.amount,
            DropperClaimant.raw_amount,
            DropperClaimant.signature,
            DropperClaim.id.label("dropper_claim_id"),
            DropperClaim.claim_id,
            DropperClaim.active,
            DropperClaim.claim_block_deadline,
            DropperClaim.title,
            DropperClaim.description,
            DropperContract.address.label("dropper_contract_address"),
            (DropperClaim.updated_at < DropperClaimant.updated_at).label(
                "is_recent_signature"
            ),
            DropperContract.blockchain.label("blockchain"),
        )
        .join(DropperClaim, DropperClaimant.dropper_claim_id == DropperClaim.id)
        .join(DropperContract, DropperClaim.dropper_contract_id == DropperContract.id)
        .filter(DropperClaimant.dropper_claim_id == dropper_claim_id)
        .filter(DropperClaimant.address == Web3.toChecksumAddress(address))
    )

    return claimant_query.one()


def get_claimant_drops(
    db_session: Session,
    blockchain: str,
    address,
    current_block_number=None,
    limit=None,
    offset=None,
):
    """
    Search for a claimant by address
    """

    claimant_query = (
        db_session.query(
            DropperClaimant.id.label("dropper_claimant_id"),
            DropperClaimant.address,
            DropperClaimant.amount,
            DropperClaimant.raw_amount,
            DropperClaimant.signature,
            DropperClaim.id.label("dropper_claim_id"),
            DropperClaim.claim_id,
            DropperClaim.active,
            DropperClaim.claim_block_deadline,
            DropperClaim.title,
            DropperClaim.description,
            DropperContract.address.label("dropper_contract_address"),
            DropperContract.blockchain,
            (DropperClaim.updated_at < DropperClaimant.updated_at).label(
                "is_recent_signature"
            ),
        )
        .join(DropperClaim, DropperClaimant.dropper_claim_id == DropperClaim.id)
        .join(DropperContract, DropperClaim.dropper_contract_id == DropperContract.id)
        .filter(DropperClaim.active == True)
        .filter(DropperClaimant.address == address)
        .filter(DropperContract.blockchain == blockchain)
    )

    if current_block_number:
        logger.info("Trying to filter block number " + str(current_block_number))
        claimant_query = claimant_query.filter(
            DropperClaim.claim_block_deadline > current_block_number
        )

    claimant_query.order_by(DropperClaimant.created_at.asc())

    if limit:
        claimant_query = claimant_query.limit(limit)

    if offset:
        claimant_query = claimant_query.offset(offset)

    return claimant_query.all()


def get_terminus_claims(
    db_session: Session,
    blockchain: str,
    terminus_address: ChecksumAddress,
    terminus_pool_id: int,
    dropper_contract_address: Optional[ChecksumAddress] = None,
    active: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
):
    """
    Search for a claimant by address
    """

    query = (
        db_session.query(
            DropperClaim.id,
            DropperClaim.title,
            DropperClaim.description,
            DropperClaim.terminus_address,
            DropperClaim.terminus_pool_id,
            DropperClaim.claim_block_deadline,
            DropperClaim.claim_id,
            DropperClaim.active,
            DropperContract.address.label("dropper_contract_address"),
        )
        .join(DropperContract)
        .filter(DropperClaim.terminus_address == terminus_address)
        .filter(DropperClaim.terminus_pool_id == terminus_pool_id)
        .filter(DropperContract.blockchain == blockchain)
    )

    if dropper_contract_address:
        query = query.filter(DropperContract.address == dropper_contract_address)

    if active:
        query = query.filter(DropperClaim.active == active)

    # TODO: add ordering in all pagination queries
    query = query.order_by(DropperClaim.created_at.asc())

    if limit:
        query = query.limit(limit)

    if offset:
        query = query.offset(offset)

    return query


def get_drop(db_session: Session, dropper_claim_id: uuid.UUID):
    """
    Return particular drop
    """
    drop = (
        db_session.query(DropperClaim).filter(DropperClaim.id == dropper_claim_id).one()  # type: ignore
    )
    return drop


def get_claims(
    db_session: Session,
    blockchain: str,
    dropper_contract_address: Optional[ChecksumAddress] = None,
    claimant_address: Optional[ChecksumAddress] = None,
    terminus_address: Optional[ChecksumAddress] = None,
    terminus_pool_id: Optional[int] = None,
    active: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
):
    """
    Search for a claimant by address
    """

    query = (
        db_session.query(
            DropperClaim.id,
            DropperClaim.title,
            DropperClaim.description,
            DropperClaim.terminus_address,
            DropperClaim.terminus_pool_id,
            DropperClaim.claim_block_deadline,
            DropperClaim.claim_id,
            DropperClaim.active,
            DropperClaimant.amount,
            DropperContract.address.label("dropper_contract_address"),
        )
        .join(DropperContract)
        .join(DropperClaimant)
        .filter(DropperContract.blockchain == blockchain)
    )

    if dropper_contract_address:
        query = query.filter(DropperContract.address == dropper_contract_address)

    if claimant_address:
        query = query.filter(DropperClaimant.address == claimant_address)

    if terminus_address:
        query = query.filter(DropperClaim.terminus_address == terminus_address)

    if terminus_pool_id:
        query = query.filter(DropperClaim.terminus_pool_id == terminus_pool_id)

    if active:
        query = query.filter(DropperClaim.active == active)

    query = query.order_by(DropperClaim.created_at.asc())

    if limit:
        query = query.limit(limit)

    if offset:
        query = query.offset(offset)

    return query


def get_drops(
    db_session: Session,
    blockchain: str,
    dropper_contract_address: Optional[ChecksumAddress] = None,
    drop_number: Optional[int] = None,
    terminus_address: Optional[ChecksumAddress] = None,
    terminus_pool_id: Optional[int] = None,
    active: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
):
    """
    Get drops
    """

    query = (
        db_session.query(
            DropperClaim.id,
            DropperClaim.title,
            DropperClaim.description,
            DropperClaim.terminus_address,
            DropperClaim.terminus_pool_id,
            DropperClaim.claim_block_deadline,
            DropperClaim.claim_id.label("drop_number"),
            DropperClaim.active,
            DropperContract.address.label("dropper_contract_address"),
        )
        .join(DropperContract)
        .filter(DropperContract.blockchain == blockchain)
    )

    if dropper_contract_address:
        query = query.filter(DropperContract.address == dropper_contract_address)

    if drop_number:
        query = query.filter(DropperClaim.claim_id == drop_number)

    if terminus_address:
        query = query.filter(DropperClaim.terminus_address == terminus_address)

    if terminus_pool_id:
        query = query.filter(DropperClaim.terminus_pool_id == terminus_pool_id)

    if active:
        query = query.filter(DropperClaim.active == active)

    query = query.order_by(DropperClaim.created_at.desc())

    if limit:
        query = query.limit(limit)

    if offset:
        query = query.offset(offset)

    return query


def get_claim_admin_pool(
    db_session: Session,
    dropper_claim_id: uuid.UUID,
) -> Any:
    """
    Search for a claimant by address
    """

    query = (
        db_session.query(
            DropperContract.blockchain,
            DropperClaim.terminus_address,
            DropperClaim.terminus_pool_id,
        )
        .join(DropperContract)
        .filter(DropperClaim.id == dropper_claim_id)
    )
    return query.one()


def ensure_admin_token_holder(
    db_session: Session, dropper_claim_id: uuid.UUID, address: ChecksumAddress
) -> bool:
    blockchain, terminus_address, terminus_pool_id = get_claim_admin_pool(
        db_session=db_session, dropper_claim_id=dropper_claim_id
    )
    terminus = Terminus_interface.Contract(
        BLOCKCHAIN_WEB3_PROVIDERS[blockchain], terminus_address
    )
    balance = terminus.balanceOf(address, terminus_pool_id).call()
    if balance == 0:
        raise AuthorizationError(
            f"Address has insufficient balance in Terminus pool: address={address}, blockchain={blockchain}, terminus_address={terminus_address}, terminus_pool_id={terminus_pool_id}"
        )
    return True


def ensure_dropper_contract_owner(
    db_session: Session, dropper_contract_id: uuid.UUID, address: ChecksumAddress
) -> bool:
    dropper_contract_info = get_dropper_contract_by_id(
        db_session=db_session, dropper_contract_id=dropper_contract_id
    )
    dropper = Dropper_interface.Contract(
        BLOCKCHAIN_WEB3_PROVIDERS[dropper_contract_info.blockchain],
        dropper_contract_info.address,
    )
    dropper_owner_address = dropper.owner().call()
    if address != Web3.toChecksumAddress(dropper_owner_address):
        raise AuthorizationError(
            f"Given address is not the owner of the given dropper contract: address={address}, blockchain={dropper_contract_info.blockchain}, dropper_address={dropper_contract_info.address}"
        )
    return True


def delete_claimants(db_session: Session, dropper_claim_id, addresses):
    """
    Delete all claimants for a claim
    """

    normalize_addresses = [Web3.toChecksumAddress(address) for address in addresses]

    was_deleted = []
    deleted_addresses = (
        db_session.query(DropperClaimant)
        .filter(DropperClaimant.dropper_claim_id == dropper_claim_id)
        .filter(DropperClaimant.address.in_(normalize_addresses))
    )
    for deleted_address in deleted_addresses:
        was_deleted.append(deleted_address.address)
        db_session.delete(deleted_address)

    db_session.commit()

    return was_deleted


def refetch_drop_signatures(
    db_session: Session, dropper_claim_id: uuid.UUID, added_by: str
):
    """
    Refetch signatures for drop
    """

    claim = (
        db_session.query(
            DropperClaim.claim_id,
            DropperClaim.claim_block_deadline,
            DropperContract.address,
            DropperContract.blockchain,
        )
        .join(DropperContract, DropperClaim.dropper_contract_id == DropperContract.id)
        .filter(DropperClaim.id == dropper_claim_id)
    ).one()  # type: ignore

    if claim.claim_block_deadline is None:
        raise DropWithNotSettedBlockDeadline(
            f"Claim block deadline is not set for dropper claim: {dropper_claim_id}"
        )

    outdated_signatures = (
        db_session.query(
            DropperClaim.claim_id,
            DropperClaimant.address,
            DropperClaimant.amount,
        )
        .join(DropperClaimant, DropperClaimant.dropper_claim_id == DropperClaim.id)
        .filter(DropperClaim.id == dropper_claim_id)
        .filter(
            or_(
                DropperClaimant.updated_at < DropperClaim.updated_at,
                DropperClaimant.signature == None,
            )
        )
    ).limit(BATCH_SIGNATURE_PAGE_SIZE)

    current_offset = 0

    users_hashes = {}
    users_amount = {}
    hashes_signature = {}

    dropper_contract = Dropper_interface.Contract(
        BLOCKCHAIN_WEB3_PROVIDERS[claim.blockchain], claim.address
    )

    while True:
        signature_requests = []

        page = outdated_signatures.offset(current_offset).all()

        claim_amounts = [outdated_signature.amount for outdated_signature in page]

        transformed_claim_amounts = batch_transform_claim_amounts(
            db_session, dropper_claim_id, claim_amounts
        )

        for outdated_signature, transformed_claim_amount in zip(
            page, transformed_claim_amounts
        ):
            message_hash_raw = dropper_contract.claimMessageHash(
                claim.claim_id,
                outdated_signature.address,
                claim.claim_block_deadline,
                int(transformed_claim_amount),
            ).call()
            message_hash = HexBytes(message_hash_raw).hex()
            signature_requests.append(message_hash)
            users_hashes[outdated_signature.address] = message_hash
            users_amount[outdated_signature.address] = outdated_signature.amount

        message_hashes = [signature_request for signature_request in signature_requests]

        signed_messages = signatures.DROP_SIGNER.batch_sign_message(message_hashes)

        hashes_signature.update(signed_messages)

        if len(page) == 0:
            break

        current_offset += BATCH_SIGNATURE_PAGE_SIZE

    claimant_objects = []

    for address, hash in users_hashes.items():
        claimant_objects.append(
            {
                "dropper_claim_id": dropper_claim_id,
                "address": address,
                "signature": hashes_signature[hash],
                "amount": users_amount[address],
                "added_by": added_by,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        )

    insert_statement = insert(DropperClaimant).values(claimant_objects)

    result_stmt = insert_statement.on_conflict_do_update(
        index_elements=[DropperClaimant.address, DropperClaimant.dropper_claim_id],
        set_=dict(
            signature=insert_statement.excluded.signature,
            updated_at=datetime.now(),
        ),
    )
    db_session.execute(result_stmt)
    db_session.commit()

    return claimant_objects


def leaderboard_version_filter(
    db_session: Session,
    leaderboard_id: uuid.UUID,
    version_number: Optional[int] = None,
) -> Union[Subquery, int]:
    # Subquery to get the latest version number for the given leaderboard
    if version_number is None:
        latest_version = (
            db_session.query(func.max(LeaderboardVersion.version_number)).filter(
                LeaderboardVersion.leaderboard_id == leaderboard_id,
                LeaderboardVersion.published == True,
            )
        ).scalar_subquery()
    else:
        latest_version = version_number

    return latest_version


def mv_pg_name(leaderboard_id: uuid.UUID) -> str:
    return f"mv_leaderboard_{leaderboard_id}".replace("-", "_")


def mv_check(db_session: Session, leaderboard_id: uuid.UUID) -> bool:
    mv_name = mv_pg_name(leaderboard_id)
    exists_query = text(
        f"""
    SELECT EXISTS (
        SELECT FROM pg_matviews WHERE schemaname = 'public' AND matviewname = '{mv_name}'
    );
    """
    )
    result = db_session.execute(exists_query).scalar()

    if result is None:
        return False
    return result


def create_materialized_view(db_session, leaderboard_id):
    # Safely format the view name using the UUID converted to string
    mv_name = mv_pg_name(leaderboard_id)

    sql_command = text(
        f"""
        CREATE MATERIALIZED VIEW IF NOT EXISTS {mv_name} AS
        SELECT
            leaderboard_scores.address AS address,
            leaderboard_scores.score AS score,
            leaderboard_scores.points_data AS points_data,
            rank() OVER (ORDER BY leaderboard_scores.score DESC, address) AS rank,
            row_number() OVER (ORDER BY leaderboard_scores.score DESC, address) AS number
        FROM
            leaderboard_scores
            JOIN leaderboard_versions ON leaderboard_versions.leaderboard_id = leaderboard_scores.leaderboard_id
            AND leaderboard_versions.version_number = leaderboard_scores.leaderboard_version_number
        WHERE
            leaderboard_scores.leaderboard_id = :leaderboard_id
            AND leaderboard_versions.published = true
            AND leaderboard_versions.version_number = (
                SELECT
                    max(leaderboard_versions.version_number)
                FROM
                    leaderboard_versions
                WHERE
                    leaderboard_versions.leaderboard_id = :leaderboard_id
                    AND leaderboard_versions.published = true
            )
        ORDER BY leaderboard_scores.score DESC, address
    """
    )

    # Execute the command with parameters
    db_session.execute(sql_command, {"leaderboard_id": str(leaderboard_id)})
    db_session.commit()


def update_materialized_view(db_session: Session, leaderboard_id: uuid.UUID):

    mv_name = mv_pg_name(leaderboard_id)

    if not mv_check(db_session, leaderboard_id):
        try:
            create_materialized_view(db_session, leaderboard_id)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            logger.error(f"Error creating materialized view: {e}")
            raise  # Re-raise exception after logging
    else:
        db_session.execute(text(f"REFRESH MATERIALIZED VIEW {mv_name}"))
        db_session.commit()


def get_leaderboard_materialized_view(
    db_session: Session, leaderboard_id: uuid.UUID, with_numerator: bool = False
) -> Query:
    ### materialized view name
    mv_name = mv_pg_name(leaderboard_id)

    if not mv_check(db_session, leaderboard_id):
        try:
            create_materialized_view(db_session, leaderboard_id)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            logger.error(f"Error creating materialized view: {e}")
            raise  # Re-raise exception after logging

    ### construct the query
    # Directly query the materialized view using text
    # Define the materialized view as a table object

    columns = [
        column("address"),
        column("score"),
        column("points_data"),
        column("rank"),
    ]

    if with_numerator:
        columns.append(column("number"))

    leaderboard_table = table(
        mv_name,
        *columns,
    )

    # Construct the select statement
    query = db_session.query(leaderboard_table)
    return query


def generate_ranking_query(
    db_session: Session,
    leaderboard_id: uuid.UUID,
    version_number: Optional[int] = None,
    with_numerator: bool = False,
) -> Query:
    """
    Generate a query to get the ranking of the leaderboard
    """

    if version_number is None:

        query = get_leaderboard_materialized_view(
            db_session, leaderboard_id, with_numerator
        )

    else:

        latest_version = leaderboard_version_filter(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            version_number=version_number,
        )

        query = (
            db_session.query(
                LeaderboardScores.address,
                LeaderboardScores.score,
                LeaderboardScores.points_data,
                func.rank().over(order_by=LeaderboardScores.score.desc()).label("rank"),
            )
            .join(
                LeaderboardVersion,
                and_(
                    LeaderboardVersion.leaderboard_id
                    == LeaderboardScores.leaderboard_id,
                    LeaderboardVersion.version_number
                    == LeaderboardScores.leaderboard_version_number,
                ),
            )
            .filter(LeaderboardScores.leaderboard_id == leaderboard_id)
            .filter(
                LeaderboardVersion.published == True,
                LeaderboardVersion.version_number == latest_version,
            )
        )

    return query


def get_leaderboard_total_count(
    db_session: Session, leaderboard_id, version_number: Optional[int] = None
) -> int:
    """
    Get the total number of position in the leaderboard
    """

    if version_number is None:

        query = get_leaderboard_materialized_view(db_session, leaderboard_id)

        total_count = query.count()
    else:
        latest_version = leaderboard_version_filter(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            version_number=version_number,
        )

        total_count = (
            db_session.query(func.count(LeaderboardScores.id))
            .join(
                LeaderboardVersion,
                and_(
                    LeaderboardVersion.leaderboard_id
                    == LeaderboardScores.leaderboard_id,
                    LeaderboardVersion.version_number
                    == LeaderboardScores.leaderboard_version_number,
                ),
            )
            .filter(
                LeaderboardVersion.published == True,
                LeaderboardVersion.version_number == latest_version,
            )
            .filter(LeaderboardScores.leaderboard_id == leaderboard_id)
        ).scalar()

    return total_count


def get_leaderboard_info(
    db_session: Session, leaderboard_id: uuid.UUID, version_number: Optional[int] = None
) -> Row[Tuple[uuid.UUID, str, str, int, Optional[datetime]]]:
    """
    Get the leaderboard from the database with users count
    """

    latest_version = leaderboard_version_filter(
        db_session=db_session,
        leaderboard_id=leaderboard_id,
        version_number=version_number,
    )

    query = (
        db_session.query(
            Leaderboard.id,
            Leaderboard.title,
            Leaderboard.description,
            func.count(LeaderboardScores.id).label("users_count"),
            func.max(LeaderboardScores.updated_at).label("last_update"),
        )
        .join(
            LeaderboardVersion,
            and_(
                LeaderboardVersion.leaderboard_id == Leaderboard.id,
                LeaderboardVersion.published == True,
            ),
            isouter=True,
        )
        .join(
            LeaderboardScores,
            and_(
                LeaderboardScores.leaderboard_id == Leaderboard.id,
                LeaderboardScores.leaderboard_version_number
                == LeaderboardVersion.version_number,
            ),
            isouter=True,
        )
        .filter(
            or_(
                LeaderboardVersion.published == None,
                LeaderboardVersion.version_number == latest_version,
            )
        )
        .filter(Leaderboard.id == leaderboard_id)
        .group_by(Leaderboard.id, Leaderboard.title, Leaderboard.description)
    )

    leaderboard = query.one()

    return leaderboard


def get_leaderboard_scores_changes(
    db_session: Session, leaderboard_id: uuid.UUID
) -> List[Row[Tuple[int, datetime]]]:
    """
    Return the leaderboard scores changes timeline changes of leaderboard scores
    """

    leaderboard_scores_changes = (
        db_session.query(
            func.count(LeaderboardScores.address).label("players_count"),
            # func.extract("epoch", LeaderboardScores.updated_at).label("timestamp"),
            LeaderboardScores.updated_at.label("date"),
        )
        .filter(LeaderboardScores.leaderboard_id == leaderboard_id)
        .group_by(LeaderboardScores.updated_at)
        .order_by(LeaderboardScores.updated_at.desc())
    ).all()

    return leaderboard_scores_changes


def get_leaderboard_scores_by_timestamp(
    db_session: Session,
    leaderboard_id: uuid.UUID,
    date: datetime,
    limit: int,
    offset: int,
) -> List[LeaderboardScores]:
    """
    Return the leaderboard scores by timestamp
    """

    leaderboard_scores = (
        db_session.query(
            LeaderboardScores.leaderboard_id,
            LeaderboardScores.address,
            LeaderboardScores.score,
            LeaderboardScores.points_data,
        )
        .filter(LeaderboardScores.leaderboard_id == leaderboard_id)
        .filter(LeaderboardScores.updated_at == date)
        .order_by(LeaderboardScores.score.desc())
        .limit(limit)
        .offset(offset)
    )

    return leaderboard_scores


def get_leaderboards(
    db_session: Session,
    token: Union[str, uuid.UUID],
) -> List[Leaderboard]:
    """
    Get the leaderboards resources
    """

    user_resources = bc.list_resources(
        token=token,
        params={"type": "leaderboard"},
    )

    if len(user_resources.resources) == 0:
        raise LeaderboardsResourcesNotFound(f"Leaderboard not found for token")

    leaderboards_ids = []

    for resource in user_resources.resources:
        leaderboard_id = resource.resource_data["leaderboard_id"]

        leaderboards_ids.append(leaderboard_id)

    leaderboards = (
        db_session.query(Leaderboard).filter(Leaderboard.id.in_(leaderboards_ids)).all()
    )

    return leaderboards


def get_position(
    db_session: Session,
    leaderboard_id,
    address,
    window_size,
    limit: int,
    offset: int,
    version_number: Optional[int] = None,
) -> List[Row[Tuple[str, int, int, int, Any]]]:
    """
    Return position by address with window size
    """

    if version_number is None:

        query = get_leaderboard_materialized_view(db_session, leaderboard_id, True)

    else:

        latest_version = leaderboard_version_filter(
            db_session=db_session,
            leaderboard_id=leaderboard_id,
            version_number=version_number,
        )

        query = (
            db_session.query(
                LeaderboardScores.address,
                LeaderboardScores.score,
                LeaderboardScores.points_data.label("points_data"),
                func.rank().over(order_by=LeaderboardScores.score.desc()).label("rank"),
                func.row_number()
                .over(order_by=LeaderboardScores.score.desc())
                .label("number"),
            )
            .join(
                LeaderboardVersion,
                and_(
                    LeaderboardVersion.leaderboard_id
                    == LeaderboardScores.leaderboard_id,
                    LeaderboardVersion.version_number
                    == LeaderboardScores.leaderboard_version_number,
                ),
            )
            .filter(
                LeaderboardVersion.published == True,
                LeaderboardVersion.version_number == latest_version,
            )
            .filter(LeaderboardScores.leaderboard_id == leaderboard_id)
        )

    ranked_leaderboard = query.cte(name="ranked_leaderboard")

    query = db_session.query(
        ranked_leaderboard.c.address,
        ranked_leaderboard.c.score,
        ranked_leaderboard.c.rank,
        ranked_leaderboard.c.number,
    ).filter(
        ranked_leaderboard.c.address == address,
    )

    my_position = query.cte(name="my_position")

    # get the position with the window size

    query = db_session.query(
        ranked_leaderboard.c.address,
        ranked_leaderboard.c.score,
        ranked_leaderboard.c.rank,
        ranked_leaderboard.c.number,
        ranked_leaderboard.c.points_data,
    ).filter(
        ranked_leaderboard.c.number.between(  # taking off my hat!
            my_position.c.number - window_size,
            my_position.c.number + window_size,
        )
    )

    if limit:
        query = query.limit(limit)

    if offset:
        query = query.offset(offset)

    return query.all()


def get_leaderboard_score(
    db_session: Session,
    leaderboard_id,
    address,
    version_number: Optional[int] = None,
) -> Optional[LeaderboardScores]:
    """
    Return address score
    """

    latest_version = leaderboard_version_filter(
        db_session=db_session,
        leaderboard_id=leaderboard_id,
        version_number=version_number,
    )

    query = (
        db_session.query(LeaderboardScores)
        .join(
            LeaderboardVersion,
            and_(
                LeaderboardVersion.leaderboard_id == LeaderboardScores.leaderboard_id,
                LeaderboardVersion.version_number
                == LeaderboardScores.leaderboard_version_number,
            ),
        )
        .filter(
            LeaderboardVersion.published == True,
            LeaderboardVersion.version_number == latest_version,
        )
        .filter(LeaderboardScores.leaderboard_id == leaderboard_id)
        .filter(LeaderboardScores.address == address)
    )

    return query.one_or_none()


def get_leaderboard_positions(
    db_session: Session,
    leaderboard_id: uuid.UUID,
    limit: int,
    offset: int,
    poitns_data: Dict[str, str],
    version_number: Optional[int] = None,
) -> List[Row[Tuple[uuid.UUID, str, int, str, int]]]:
    """
    Get the leaderboard positions
    """

    # get public leaderboard scores with max version

    query = generate_ranking_query(db_session, leaderboard_id, version_number)

    if len(poitns_data) > 0:

        query = query.filter(
            or_(
                *[
                    LeaderboardScores.points_data[point_key].astext == point_value
                    for point_key, point_value in poitns_data.items()
                ]
            )
        )

    if limit:
        query = query.limit(limit)

    if offset:
        query = query.offset(offset)

    return query


def get_qurtiles(
    db_session: Session, leaderboard_id, version_number: Optional[int] = None
) -> Tuple[Row[Tuple[str, float, int]], ...]:
    """
    Get the leaderboard qurtiles
    https://docs.sqlalchemy.org/en/14/core/functions.html#sqlalchemy.sql.functions.percentile_disc
    """

    query = generate_ranking_query(db_session, leaderboard_id, version_number)

    ranked_leaderboard = query.cte(name="ranked_leaderboard")

    current_count = db_session.query(ranked_leaderboard).count()

    if current_count == 0:
        raise LeaderboardIsEmpty(f"Leaderboard {leaderboard_id} is empty")

    index_75 = int(current_count / 4)

    index_50 = int(current_count / 2)

    index_25 = int(current_count * 3 / 4)

    q1 = db_session.query(ranked_leaderboard).limit(1).offset(index_25).first()

    q2 = db_session.query(ranked_leaderboard).limit(1).offset(index_50).first()

    q3 = db_session.query(ranked_leaderboard).limit(1).offset(index_75).first()

    return q1, q2, q3


def get_ranks(
    db_session: Session, leaderboard_id, version_number: Optional[int] = None
) -> List[Row[Tuple[int, int, int]]]:
    """
    Get the leaderboard rank buckets(rank, size, score)
    """

    query = generate_ranking_query(db_session, leaderboard_id, version_number)

    ranked_leaderboard = query.cte(name="ranked_leaderboard")

    ranks = db_session.query(
        ranked_leaderboard.c.rank,
        func.count(ranked_leaderboard.c.id).label("size"),
        ranked_leaderboard.c.score,
    ).group_by(ranked_leaderboard.c.rank, ranked_leaderboard.c.score)
    return ranks


def get_rank(
    db_session: Session,
    leaderboard_id: uuid.UUID,
    rank: int,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    version_number: Optional[int] = None,
) -> List[Row[Tuple[uuid.UUID, str, int, str, int]]]:
    """
    Get bucket in leaderboard by rank
    """

    query = generate_ranking_query(db_session, leaderboard_id, version_number)

    query.order_by(text("rank asc, id asc"))

    ranked_leaderboard = query.cte(name="ranked_leaderboard")

    positions = db_session.query(ranked_leaderboard).filter(
        ranked_leaderboard.c.rank == rank
    )

    if limit:
        positions = positions.limit(limit)

    if offset:
        positions = positions.offset(offset)

    return positions


def create_leaderboard(
    db_session: Session,
    title: str,
    description: Optional[str],
    token: Optional[Union[uuid.UUID, str]] = None,
    wallet_connect: bool = False,
    blockchain_ids: List[int] = [],
    columns_names: ColumnsNames = None,
) -> Leaderboard:
    """
    Create a leaderboard
    """

    if columns_names is not None:
        columns_names = columns_names.dict()

    if not token:
        token = uuid.UUID(MOONSTREAM_ADMIN_ACCESS_TOKEN)
    try:
        # deduplicate and sort
        blockchain_ids = sorted(list(set(blockchain_ids)))

        leaderboard = Leaderboard(
            title=title,
            description=description,
            wallet_connect=wallet_connect,
            blockchain_ids=blockchain_ids,
            columns_names=columns_names,
        )
        db_session.add(leaderboard)
        db_session.commit()

        user = None
        if token is not None:
            user = bc.get_user(token=token)

        resource = create_leaderboard_resource(
            leaderboard_id=str(leaderboard.id),
            user_id=str(user.id) if user is not None else None,
        )
        leaderboard.resource_id = resource.id
        try:
            create_materialized_view(db_session, leaderboard.id)
        except Exception as e:
            logger.error(f"Error creating materialized view: {e}")
            raise LeaderboardCreateError(f"Error creating materialized view: {e}")

        db_session.commit()
    except Exception as e:
        db_session.rollback()
        logger.error(f"Error creating leaderboard: {e}")
        raise LeaderboardCreateError(f"Error creating leaderboard: {e}")
    return leaderboard


def delete_leaderboard(
    db_session: Session, leaderboard_id: uuid.UUID, token: uuid.UUID
) -> Leaderboard:
    """
    Delete a leaderboard
    """
    try:
        leaderboard = (
            db_session.query(Leaderboard).filter(Leaderboard.id == leaderboard_id).one()  # type: ignore
        )

        if leaderboard.resource_id is not None:
            try:
                bc.delete_resource(
                    token=token,
                    resource_id=leaderboard.resource_id,
                )
            except Exception as e:
                logger.error(f"Error deleting leaderboard resource: {e}")
        else:
            logger.error(
                f"Leaderboard {leaderboard_id} has no resource id. Skipping. Better delete it manually."
            )

        db_session.delete(leaderboard)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        logger.error(e)
        raise LeaderboardDeleteError(f"Error deleting leaderboard: {e}")

    return leaderboard


def update_leaderboard(
    db_session: Session,
    leaderboard_id: uuid.UUID,
    title: Optional[str],
    description: Optional[str],
    wallet_connect: Optional[bool],
    blockchain_ids: Optional[List[int]],
    columns_names: Optional[ColumnsNames],
) -> Leaderboard:
    """
    Update a leaderboard
    """

    leaderboard = (
        db_session.query(Leaderboard).filter(Leaderboard.id == leaderboard_id).one()  # type: ignore
    )

    if title is not None:
        leaderboard.title = title
    if description is not None:
        leaderboard.description = description
    if wallet_connect is not None:
        leaderboard.wallet_connect = wallet_connect
    if blockchain_ids is not None:
        # deduplicate and sort
        blockchain_ids = sorted(list(set(blockchain_ids)))
        leaderboard.blockchain_ids = blockchain_ids

    if columns_names is not None:
        if leaderboard.columns_names is not None:
            current_columns_names = ColumnsNames(**leaderboard.columns_names)

            for key, value in columns_names.dict(exclude_none=True).items():
                setattr(current_columns_names, key, value)
        else:
            current_columns_names = columns_names

        leaderboard.columns_names = current_columns_names.dict()

    db_session.commit()

    return leaderboard


def get_leaderboard_by_id(db_session: Session, leaderboard_id) -> Leaderboard:
    """
    Get the leaderboard by id
    """
    return db_session.query(Leaderboard).filter(Leaderboard.id == leaderboard_id).one()  # type: ignore


def get_leaderboard_by_title(db_session: Session, title) -> Leaderboard:
    """
    Get the leaderboard by title
    """
    return db_session.query(Leaderboard).filter(Leaderboard.title == title).one()  # type: ignore


def list_leaderboards(
    db_session: Session, limit: int, offset: int
) -> List[Row[Tuple[uuid.UUID, str, str]]]:
    """
    List all leaderboards
    """
    query = db_session.query(Leaderboard.id, Leaderboard.title, Leaderboard.description)

    if limit:
        query = query.limit(limit)

    if offset:
        query = query.offset(offset)

    return query.all()


def add_scores(
    db_session: Session,
    leaderboard_id: uuid.UUID,
    scores: List[Score],
    version_number: int,
    normalize_addresses: bool = True,
):
    """
    Add scores to the leaderboard
    """

    leaderboard_scores = []

    normalizer_fn = Web3.toChecksumAddress
    if not normalize_addresses:
        normalizer_fn = lambda x: x  # type: ignore

    addresses = [score.address for score in scores]

    if len(addresses) != len(set(addresses)):
        duplicates = [key for key, value in Counter(addresses).items() if value > 1]

        raise DuplicateLeaderboardAddressError("Dublicated addresses", duplicates)

    # Process each score and append to leaderboard_scores list
    non_normalized_addresses = []
    for index, score in enumerate(scores):
        try:
            normalized_address = normalizer_fn(score.address)
            leaderboard_scores.append(
                {
                    "leaderboard_id": leaderboard_id,
                    "address": normalized_address,
                    "score": score.score,
                    "points_data": score.points_data,
                    "leaderboard_version_number": version_number,
                }
            )
        except Exception as e:
            non_normalized_addresses.append((index + 1, score.address))

    if non_normalized_addresses:
        logger.error(f"Error adding scores to leaderboard failed in normalizing")
        raise LeaderboardNormalizeScoresError(
            f"Error adding scores to leaderboard. Non-normalized addresses",
            non_normalized_addresses,
        )

    insert_statement = insert(LeaderboardScores).values(leaderboard_scores)

    result_stmt = insert_statement.on_conflict_do_update(
        index_elements=[
            LeaderboardScores.address,
            LeaderboardScores.leaderboard_id,
            LeaderboardScores.leaderboard_version_number,
        ],
        set_=dict(
            score=insert_statement.excluded.score,
            points_data=insert_statement.excluded.points_data,
            updated_at=datetime.now(),
        ),
    )

    try:
        db_session.execute(result_stmt)
        db_session.commit()
    except Exception as e:
        logger.error(f"Error adding scores to leaderboard failed on commit: {e}")
        db_session.rollback()
        raise LeaderboardPushScoreError("Error committing scores")

    try:
        update_materialized_view(db_session, leaderboard_id)
    except Exception as e:
        logger.error(f"Error updating materialized view: {e}")

    return leaderboard_scores


# leaderboard access actions


def create_leaderboard_resource(leaderboard_id: str, user_id: Optional[str] = None):
    resource_data: Dict[str, Any] = {
        "type": LEADERBOARD_RESOURCE_TYPE,
        "leaderboard_id": leaderboard_id,
    }

    try:
        resource = bc.create_resource(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            application_id=MOONSTREAM_APPLICATION_ID,
            resource_data=resource_data,
            timeout=10,
        )
    except Exception as e:
        raise LeaderboardCreateError(f"Error creating leaderboard resource: {e}")

    if user_id is not None:
        try:
            bc.add_resource_holder_permissions(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                resource_id=resource.id,
                holder_permissions=BugoutResourceHolder(
                    holder_type=HolderType.user,
                    holder_id=user_id,
                    permissions=[
                        ResourcePermissions.ADMIN,
                        ResourcePermissions.READ,
                        ResourcePermissions.UPDATE,
                        ResourcePermissions.DELETE,
                    ],
                ),
            )
        except Exception as e:
            raise LeaderboardCreateError(
                f"Error adding resource holder permissions: {e}"
            )

    return resource


def assign_resource(
    db_session: Session,
    leaderboard_id: uuid.UUID,
    user_token: Optional[Union[uuid.UUID, str]] = None,
    resource_id: Optional[uuid.UUID] = None,
):
    """
    Assign a resource handler to a leaderboard
    """

    ### get user_name from token

    user = None
    if user_token is not None:
        user = bc.get_user(token=user_token)

    leaderboard = (
        db_session.query(Leaderboard).filter(Leaderboard.id == leaderboard_id).one()  # type: ignore
    )

    if resource_id is not None:
        leaderboard.resource_id = resource_id
    else:
        resource = create_leaderboard_resource(
            leaderboard_id=str(leaderboard_id),
            user_id=user.id if user is not None else None,
        )

        leaderboard.resource_id = resource.id

    db_session.commit()
    db_session.flush()

    return leaderboard.resource_id


def list_leaderboards_resources(
    db_session: Session,
):
    """
    List all leaderboards resources
    """

    query = db_session.query(Leaderboard.id, Leaderboard.title, Leaderboard.resource_id)

    return query.all()


def get_leaderboard_config_entry(
    leaderboard_id: uuid.UUID,
) -> BugoutSearchResult:
    query = f"#leaderboard_id:{leaderboard_id}"
    configs = bc.search(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        journal_id=MOONSTREAM_LEADERBOARD_CONFIGURATION_JOURNAL_ID,
        query=query,
        limit=1,
    )

    results = cast(List[BugoutSearchResult], configs.results)

    if len(configs.results) == 0 or results[0].content is None:
        raise LeaderboardConfigNotFound(
            f"Leaderboard config not found for {leaderboard_id}"
        )

    return results[0]


def get_leaderboard_config(
    leaderboard_id: uuid.UUID,
) -> Dict[str, Any]:
    """
    Return leaderboard config from leaderboard generator journal
    """

    entry = get_leaderboard_config_entry(leaderboard_id)

    content = json.loads(entry.content)  # type: ignore

    if "status:active" not in entry.tags:
        content["leaderboard_auto_update_active"] = False
    else:
        content["leaderboard_auto_update_active"] = True

    return content


def update_leaderboard_config(
    leaderboard_id: uuid.UUID, config: LeaderboardConfigUpdate
) -> Dict[str, Any]:
    """
    Update leaderboard config in leaderboard generator journal

    """

    entry_config = get_leaderboard_config_entry(leaderboard_id)

    current_config = LeaderboardConfig(**json.loads(entry_config.content))  # type: ignore

    new_params = config.params

    for key, value in new_params.items():
        if key not in current_config.params:
            continue

        current_config.params[key] = value

    # we replace values of parameters that are not None

    entry = bc.update_entry_content(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        journal_id=MOONSTREAM_LEADERBOARD_CONFIGURATION_JOURNAL_ID,
        title=entry_config.title,
        entry_id=entry_config.entry_url.split("/")[-1],
        content=json.dumps(current_config.dict()),
    )

    new_config = json.loads(entry.content)

    if "status:active" not in entry.tags:
        new_config["leaderboard_auto_update_active"] = False
    else:
        new_config["leaderboard_auto_update_active"] = True

    return new_config


def activate_leaderboard_config(
    leaderboard_id: uuid.UUID,
):
    """
    Add tag status:active to leaderboard config journal entry
    """

    entry_config = get_leaderboard_config_entry(leaderboard_id)

    if "status:active" in entry_config.tags:
        raise LeaderboardConfigAlreadyActive(
            f"Leaderboard config {leaderboard_id} already active"
        )

    bc.create_tags(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        journal_id=MOONSTREAM_LEADERBOARD_CONFIGURATION_JOURNAL_ID,
        entry_id=entry_config.entry_url.split("/")[-1],
        tags=["status:active"],
    )


def deactivate_leaderboard_config(
    leaderboard_id: uuid.UUID,
):
    """
    Remove tag status:active from leaderboard config journal entry
    """

    entry_config = get_leaderboard_config_entry(leaderboard_id)

    if "status:active" not in entry_config.tags:
        raise LeaderboardConfigAlreadyInactive(
            f"Leaderboard config {leaderboard_id} not active"
        )

    bc.delete_tag(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        journal_id=MOONSTREAM_LEADERBOARD_CONFIGURATION_JOURNAL_ID,
        entry_id=entry_config.entry_url.split("/")[-1],
        tag="status:active",
    )


def revoke_resource(
    db_session: Session, leaderboard_id: uuid.UUID
) -> Optional[uuid.UUID]:
    """
    Revoke a resource handler to a leaderboard
    """

    # TODO(ANDREY): Delete resource via admin token

    leaderboard = (
        db_session.query(Leaderboard).filter(Leaderboard.id == leaderboard_id).one()  # type: ignore
    )

    if leaderboard.resource_id is None:
        raise Exception("Leaderboard does not have a resource")

    leaderboard.resource_id = None

    db_session.commit()
    db_session.flush()

    return leaderboard.resource_id


def check_leaderboard_resource_permissions(
    db_session: Session, leaderboard_id: uuid.UUID, token: uuid.UUID
) -> bool:
    """
    Check if the user has permissions to access the leaderboard
    """
    leaderboard = (
        db_session.query(Leaderboard).filter(Leaderboard.id == leaderboard_id).one()  # type: ignore
    )

    permission_url = f"{bc.brood_url}/resources/{leaderboard.resource_id}/holders"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    # If user don't have at least read permission return 404
    result = requests.get(url=permission_url, headers=headers, timeout=10)

    if result.status_code == 200:
        return True

    return False


def get_leaderboard_version(
    db_session: Session, leaderboard_id: uuid.UUID, version_number: int
) -> LeaderboardVersion:
    """
    Get the leaderboard version by id
    """
    return (
        db_session.query(LeaderboardVersion)
        .filter(LeaderboardVersion.leaderboard_id == leaderboard_id)
        .filter(LeaderboardVersion.version_number == version_number)
        .one()
    )


def create_leaderboard_version(
    db_session: Session,
    leaderboard_id: uuid.UUID,
    version_number: Optional[int] = None,
    publish: bool = False,
) -> LeaderboardVersion:
    """
    Create a leaderboard version
    """

    if version_number is None:
        latest_version_result = (
            db_session.query(func.max(LeaderboardVersion.version_number))
            .filter(LeaderboardVersion.leaderboard_id == leaderboard_id)
            .one()
        )

        latest_version = latest_version_result[0]

        if latest_version is None:
            version_number = 0
        else:
            version_number = latest_version + 1

    leaderboard_version = LeaderboardVersion(
        leaderboard_id=leaderboard_id,
        version_number=version_number,
        published=publish,
    )

    db_session.add(leaderboard_version)
    db_session.commit()

    if publish:
        try:
            update_materialized_view(db_session, leaderboard_id)
        except Exception as e:
            logger.error(f"Error updating materialized view: {e}")

    return leaderboard_version


def change_publish_leaderboard_version_status(
    db_session: Session, leaderboard_id: uuid.UUID, version_number: int, published: bool
) -> LeaderboardVersion:
    """
    Publish a leaderboard version
    """
    leaderboard_version = (
        db_session.query(LeaderboardVersion)
        .filter(LeaderboardVersion.leaderboard_id == leaderboard_id)
        .filter(LeaderboardVersion.version_number == version_number)
        .one()
    )

    leaderboard_version.published = published

    db_session.commit()

    if published:
        try:
            update_materialized_view(db_session, leaderboard_id)
        except Exception as e:
            logger.error(f"Error updating materialized view: {e}")

    return leaderboard_version


def get_leaderboard_versions(
    db_session: Session, leaderboard_id: uuid.UUID
) -> List[LeaderboardVersion]:
    """
    Get all leaderboard versions
    """
    return (
        db_session.query(LeaderboardVersion)
        .filter(LeaderboardVersion.leaderboard_id == leaderboard_id)
        .all()
    )


def delete_leaderboard_version(
    db_session: Session, leaderboard_id: uuid.UUID, version_number: int
) -> LeaderboardVersion:
    """
    Delete a leaderboard version
    """
    leaderboard_version = (
        db_session.query(LeaderboardVersion)
        .filter(LeaderboardVersion.leaderboard_id == leaderboard_id)
        .filter(LeaderboardVersion.version_number == version_number)
        .one()
    )

    db_session.delete(leaderboard_version)
    db_session.commit()

    try:
        update_materialized_view(db_session, leaderboard_id)
    except Exception as e:
        logger.error(f"Error updating materialized view: {e}")

    return leaderboard_version


def get_leaderboard_version_scores(
    db_session: Session,
    leaderboard_id: uuid.UUID,
    version_number: int,
    limit: int,
    offset: int,
) -> List[LeaderboardScores]:
    """
    Get the leaderboard scores by version number
    """

    query = (
        db_session.query(
            LeaderboardScores.id,
            LeaderboardScores.address.label("address"),
            LeaderboardScores.score.label("score"),
            LeaderboardScores.points_data.label("points_data"),
            func.rank().over(order_by=LeaderboardScores.score.desc()).label("rank"),
        )
        .filter(LeaderboardScores.leaderboard_id == leaderboard_id)
        .filter(LeaderboardScores.leaderboard_version_number == version_number)
    )

    if limit:
        query = query.limit(limit)

    if offset:
        query = query.offset(offset)

    return query


def delete_previous_versions(
    db_session: Session,
    leaderboard_id: uuid.UUID,
    threshold_version_number: int,
) -> int:
    """
    Delete old leaderboard versions
    """

    versions_to_delete = (
        db_session.query(LeaderboardVersion)
        .filter(LeaderboardVersion.leaderboard_id == leaderboard_id)
        .filter(LeaderboardVersion.version_number < threshold_version_number)
    )

    num_deleted = versions_to_delete.delete(synchronize_session=False)

    db_session.commit()

    return num_deleted
