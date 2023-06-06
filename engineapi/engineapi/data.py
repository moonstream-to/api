from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, root_validator, validator
from web3 import Web3


class PingResponse(BaseModel):
    """
    Schema for ping response
    """

    status: str


class NowResponse(BaseModel):
    """
    Schema for responses on /now endpoint
    """

    epoch_time: float


class SignerListResponse(BaseModel):
    instances: List[Any] = Field(default_factory=list)


class SignerSleepResponse(BaseModel):
    instances: List[str] = Field(default_factory=list)


class SignerWakeupResponse(BaseModel):
    instances: List[str] = Field(default_factory=list)


class DropperContractResponse(BaseModel):
    id: UUID
    address: str
    blockchain: str
    title: Optional[str]
    description: Optional[str]
    image_uri: Optional[str]


class DropperTerminusResponse(BaseModel):
    terminus_address: str
    terminus_pool_id: int
    blockchain: str


class DropperBlockchainResponse(BaseModel):
    blockchain: str


class DropRegisterRequest(BaseModel):
    dropper_contract_id: UUID
    title: Optional[str] = None
    description: Optional[str] = None
    claim_block_deadline: Optional[int] = None
    terminus_address: Optional[str] = None
    terminus_pool_id: Optional[int] = None
    claim_id: Optional[int] = None


class DropCreatedResponse(BaseModel):
    dropper_claim_id: UUID
    dropper_contract_id: UUID
    title: str
    description: str
    claim_block_deadline: Optional[int] = None
    terminus_address: Optional[str] = None
    terminus_pool_id: Optional[int] = None
    claim_id: Optional[int] = None


class Claimant(BaseModel):
    address: str
    amount: int
    raw_amount: Optional[str] = None


class BatchAddClaimantsRequest(BaseModel):
    claimants: List[Claimant] = Field(default_factory=list)


class BatchRemoveClaimantsRequest(BaseModel):
    claimants: List[str] = Field(default_factory=list)


class DropAddClaimantsRequest(BaseModel):
    dropper_claim_id: UUID
    claimants: List[Claimant] = Field(default_factory=list)


class ClaimantsResponse(BaseModel):
    claimants: List[Claimant] = Field(default_factory=list)


class DropRemoveClaimantsRequest(BaseModel):
    dropper_claim_id: UUID
    addresses: List[str] = Field(default_factory=list)


class RemoveClaimantsResponse(BaseModel):
    addresses: List[str] = Field(default_factory=list)


class DropperClaimResponse(BaseModel):
    id: UUID
    dropper_contract_id: UUID
    title: str
    description: str
    active: bool
    claim_block_deadline: Optional[int] = None
    terminus_address: Optional[str] = None
    terminus_pool_id: Optional[int] = None
    claim_id: Optional[int] = None


class DropResponse(BaseModel):
    claimant: str
    claim_id: int
    amount: str
    block_deadline: int
    signature: str
    title: str
    description: str


class DropBatchResponseItem(BaseModel):
    claimant: str
    claim_id: int
    title: str
    description: str
    amount: int
    amount_string: str
    block_deadline: int
    signature: str
    dropper_claim_id: UUID
    dropper_contract_address: str
    blockchain: str


class DropListResponse(BaseModel):
    drops: List[Any] = Field(default_factory=list)


class DropClaimant(BaseModel):
    amount: Optional[int]
    added_by: Optional[str]
    address: Optional[str]


class DropActivateRequest(BaseModel):
    dropper_claim_id: UUID


class DropUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    claim_block_deadline: Optional[int] = None
    terminus_address: Optional[str] = None
    terminus_pool_id: Optional[int] = None
    claim_id: Optional[int] = None


class DropUpdatedResponse(BaseModel):
    dropper_claim_id: UUID
    dropper_contract_id: UUID
    title: str
    description: str
    claim_block_deadline: Optional[int] = None
    terminus_address: Optional[str] = None
    terminus_pool_id: Optional[int] = None
    claim_id: Optional[int] = None
    active: bool = True


class ContractType(Enum):
    raw = "raw"
    dropper = "dropper-v0.2.0"


class RegisterContractRequest(BaseModel):
    blockchain: str
    address: str
    contract_type: ContractType
    title: Optional[str] = None
    description: Optional[str] = None
    image_uri: Optional[str] = None


class UpdateContractRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_uri: Optional[str] = None
    ignore_nulls: bool = True


class RegisteredContract(BaseModel):
    id: UUID
    blockchain: str
    address: str
    contract_type: str
    moonstream_user_id: UUID
    title: Optional[str] = None
    description: Optional[str] = None
    image_uri: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    @validator("id", "moonstream_user_id")
    def validate_uuids(cls, v):
        return str(v)

    @validator("created_at", "updated_at")
    def validate_datetimes(cls, v):
        return v.isoformat()

    class Config:
        orm_mode = True


class CallSpecification(BaseModel):
    caller: str
    method: str
    parameters: Dict[str, Any]

    @validator("caller")
    def validate_web3_addresses(cls, v):
        return Web3.toChecksumAddress(v)


class CreateCallRequestsAPIRequest(BaseModel):
    contract_id: Optional[UUID] = None
    contract_address: Optional[str] = None
    specifications: List[CallSpecification] = Field(default_factory=list)
    ttl_days: Optional[int] = None

    # Solution found thanks to https://github.com/pydantic/pydantic/issues/506
    @root_validator
    def at_least_one_of_contract_id_and_contract_address(cls, values):
        if values.get("contract_id") is None and values.get("contract_address") is None:
            raise ValueError(
                "At least one of contract_id and contract_address must be provided"
            )
        return values


class CallRequest(BaseModel):
    id: UUID
    contract_id: UUID = Field(alias="registered_contract_id")
    contract_address: Optional[str] = None
    moonstream_user_id: UUID
    caller: str
    method: str
    parameters: Dict[str, Any]
    expires_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

    @validator("id", "contract_id", "moonstream_user_id")
    def validate_uuids(cls, v):
        return str(v)

    @validator("created_at", "updated_at", "expires_at")
    def validate_datetimes(cls, v):
        if v is not None:
            return v.isoformat()

    @validator("contract_address", "caller")
    def validate_web3_adresses(cls, v):
        return Web3.toChecksumAddress(v)


class QuartilesResponse(BaseModel):
    percentile_25: Dict[str, Any]
    percentile_50: Dict[str, Any]
    percentile_75: Dict[str, Any]


class CountAddressesResponse(BaseModel):
    count: int = Field(default_factory=int)


class Score(BaseModel):
    address: str
    score: int
    points_data: Dict[str, Any]


class LeaderboardPosition(BaseModel):
    address: str
    rank: int
    score: int
    points_data: Dict[str, Any]


class RanksResponse(BaseModel):
    rank: int
    score: int
    size: int
