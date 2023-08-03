"""
Pydantic schemas for the Moonstream HTTP API
"""
import json
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union
from uuid import UUID
from xmlrpc.client import Boolean

from fastapi import Form
from pydantic import BaseModel, Field, validator
from sqlalchemy import false

USER_ONBOARDING_STATE = "onboarding_state"

BUGOUT_RESOURCE_QUERY_RESOLVER = "query_name_resolver"


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
    blockchain: Optional[str] = None
    stripe_product_id: Optional[str] = None
    stripe_price_id: Optional[str] = None
    active: bool = False


class SubscriptionTypesListResponse(BaseModel):
    subscription_types: List[SubscriptionTypeResourceData] = Field(default_factory=list)


class SubscriptionResourceData(BaseModel):
    id: str
    address: Optional[str]
    abi: Optional[Union[str, bool]]
    color: Optional[str]
    label: Optional[str]
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    user_id: str
    subscription_type_id: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


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


class SubscriptionsAbiResponse(BaseModel):
    abi: str


class UpdateSubscriptionRequest(BaseModel):
    color: Optional[str] = Form(None)
    label: Optional[str] = Form(None)
    abi: Optional[str] = Form(None)
    description: Optional[str] = Form(None)
    tags: Optional[List[Dict[str, str]]] = Form(None)

    @validator("tags", pre=True, always=True)
    def transform_to_dict(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        elif isinstance(v, list):
            return v
        return []


class CreateSubscriptionRequest(BaseModel):
    address: str = Form(...)
    subscription_type_id: str = Form(...)
    color: str = Form(...)
    label: str = Form(...)
    abi: Optional[str] = Form(None)
    description: Optional[str] = Form(None)
    tags: Optional[List[Dict[str, str]]] = Form(None)

    @validator("tags", pre=True, always=True)
    def transform_to_dict(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        elif isinstance(v, list):
            return v
        return []


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


class UpdateDataRequest(BaseModel):
    params: Dict[str, Any] = Field(default_factory=dict)
    blockchain: Optional[str] = None


class UpdateQueryRequest(BaseModel):
    query: str


class PreapprovedQuery(BaseModel):
    query: str
    name: str
    public: bool = False


class QueryPresignUrl(BaseModel):
    url: str


class QueryInfoResponse(BaseModel):
    query: str
    query_id: str
    public: bool = False
    preapprove: bool = False
    approved: bool = False
    parameters: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class SuggestedQueriesResponse(BaseModel):
    interfaces: Dict[str, Any] = Field(default_factory=dict)
    queries: List[Any] = Field(default_factory=list)


class ContractInfoResponse(BaseModel):
    contract_info: Dict[str, Any] = Field(default_factory=dict)


class ContractInterfacesResponse(BaseModel):
    interfaces: Dict[str, Any] = Field(default_factory=dict)
