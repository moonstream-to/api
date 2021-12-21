"""
Pydantic schemas for the Moonstream HTTP API
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field

USER_ONBOARDING_STATE = "onboarding_state"


class TimeScale(Enum):
    month = "month"
    week = "week"
    day = "day"


class UpdateStats(BaseModel):
    timescales: List[str]


class SubscriptionTypeResourceData(BaseModel):
    id: str
    name: str
    description: str
    choices: List[str] = Field(default_factory=list)
    icon_url: str
    stripe_product_id: Optional[str] = None
    stripe_price_id: Optional[str] = None
    active: bool = False


class SubscriptionTypesListResponse(BaseModel):
    subscription_types: List[SubscriptionTypeResourceData] = Field(default_factory=list)


class SubscriptionResourceData(BaseModel):
    id: str
    address: str
    abi: Optional[str]
    color: Optional[str]
    label: Optional[str]
    user_id: str
    subscription_type_id: str
    created_at: datetime
    updated_at: datetime


class CreateSubscriptionRequest(BaseModel):
    address: str
    color: str
    label: str
    subscription_type_id: str


class PingResponse(BaseModel):
    """
    Schema for ping response
    """

    status: str


class VersionResponse(BaseModel):
    """
    Schema for responses on /version endpoint
    """

    version: str


class NowResponse(BaseModel):
    """
    Schema for responses on /now endpoint
    """

    epoch_time: float


class StatusResponse(BaseModel):
    ethereum_txpool_timestamp: Optional[datetime] = None
    ethereum_trending_timestamp: Optional[datetime] = None


class SubscriptionUpdate(BaseModel):
    update: Dict[str, Any]
    drop_keys: List[str] = Field(default_factory=list)


class SubscriptionsListResponse(BaseModel):
    subscriptions: List[SubscriptionResourceData] = Field(default_factory=list)


class EVMFunctionSignature(BaseModel):
    type = "function"
    hex_signature: str
    text_signature_candidates: List[str] = Field(default_factory=list)


class EVMEventSignature(BaseModel):
    type = "event"
    hex_signature: str
    text_signature_candidates: List[str] = Field(default_factory=list)


class ContractABI(BaseModel):
    functions: List[EVMFunctionSignature]
    events: List[EVMEventSignature]


class EthereumTransaction(BaseModel):
    gas: int
    gas_price: int
    value: int
    from_address: str = Field(alias="from")
    to_address: Optional[str] = Field(alias="to")
    hash: Optional[str] = None
    block_hash: Optional[str] = Field(default=None, alias="blockHash")
    block_number: Optional[int] = Field(default=None, alias="blockNumber")
    input: Optional[str] = None
    nonce: Optional[int] = None
    r: Optional[str] = None
    s: Optional[str] = None
    v: Optional[str] = None
    transaction_index: Optional[int] = Field(default=None, alias="transactionIndex")
    transaction_type: str = Field(default="0x0", alias="type")


class EthereumTransactionItem(BaseModel):
    color: Optional[str]
    from_label: Optional[str] = None
    to_label: Optional[str] = None
    block_number: Optional[int] = None
    gas: int
    gasPrice: int
    value: int
    nonce: Optional[str]
    from_address: Optional[str]  # = Field(alias="from")
    to_address: Optional[str]  # = Field(default=None, alias="to")
    hash: Optional[str] = None
    input: Optional[str] = None
    timestamp: Optional[int] = None
    subscription_type_id: Optional[str] = None


class StreamBoundary(BaseModel):
    """
    StreamBoundary represents a window of time through which an API caller can view a stream.

    This data structure is foundational to our stream rendering, and is used throughout the code
    base.
    """

    start_time: int = 0
    end_time: Optional[int] = None
    include_start: bool = False
    include_end: bool = False
    reversed_time: bool = False


class Event(BaseModel):
    event_type: str
    event_timestamp: int  # Seconds since epoch
    event_data: Dict[str, Any] = Field(default_factory=dict)


class GetEventsResponse(BaseModel):
    stream_boundary: StreamBoundary
    events: List[Event] = Field(default_factory=list)


class TxinfoEthereumBlockchainRequest(BaseModel):
    tx: EthereumTransaction


class EthereumSmartContractSourceInfo(BaseModel):
    name: str
    source_code: str
    abi: str
    compiler_version: str


class EthereumTokenDetails(BaseModel):
    name: Optional[str] = None
    symbol: Optional[str] = None
    external_url: List[str] = Field(default_factory=list)


class EthereumSmartContractDetails(BaseModel):
    name: Optional[str] = None
    external_url: List[str] = Field(default_factory=list)


class EthereumNFTDetails(EthereumTokenDetails):
    total_supply: Optional[int] = None


class EthereumAddressInfo(BaseModel):
    address: str
    ens_name: Optional[str] = None
    token: Optional[EthereumTokenDetails] = None
    smart_contract: Optional[EthereumSmartContractDetails] = None
    nft: Optional[EthereumNFTDetails] = None


class TxinfoEthereumBlockchainResponse(BaseModel):
    tx: EthereumTransaction
    is_smart_contract_deployment: bool = False
    is_smart_contract_call: bool = False
    smart_contract_address: Optional[str] = None
    smart_contract_info: Optional[EthereumSmartContractSourceInfo] = None
    abi: Optional[ContractABI] = None
    errors: List[str] = Field(default_factory=list)


class AddressLabelResponse(BaseModel):
    label: str
    label_data: Optional[Dict[str, Any]] = None


class AddressLabelsResponse(BaseModel):
    address: str
    labels: List[AddressLabelResponse] = Field(default_factory=list)


class AddressListLabelsResponse(BaseModel):
    addresses: List[AddressLabelsResponse] = Field(default_factory=list)


class OnboardingState(BaseModel):
    is_complete: bool
    steps: Dict[str, int]


class SubdcriptionsAbiResponse(BaseModel):
    url: str


class DashboardMeta(BaseModel):
    subscription_id: UUID
    generic: Optional[List[Dict[str, str]]]
    all_methods: bool = True
    all_events: bool = True
    methods: List[Dict[str, Any]]
    events: List[Dict[str, Any]]


class DashboardResource(BaseModel):
    type: str
    user_id: str
    name: str
    subscription_settings: List[DashboardMeta]


class DashboardCreate(BaseModel):
    name: str
    subscription_settings: List[DashboardMeta]


class DashboardUpdate(BaseModel):
    name: Optional[str]
    subscription_settings: List[DashboardMeta] = Field(default_factory=list)
