"""
Pydantic schemas for the Moonstream HTTP API
"""
from enum import Enum
from typing import List, Optional


from pydantic import BaseModel, Field


class SubscriptionTypeResourceData(BaseModel):
    id: str
    name: str
    description: str
    subscription_plan_id: Optional[str] = None
    active: bool = False


class SubscriptionTypesListResponce(BaseModel):
    subscriptions: List[SubscriptionTypeResourceData] = Field(default_factory=list)


class SubscriptionResourceData(BaseModel):
    id: str
    address: str
    color: str
    label: str
    user_id: str
    subscription_type_id: str


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


class SubscriptionRequest(BaseModel):
    """
    Schema for data retrieving from frontend about subscription.
    """

    blockchain: str


class SubscriptionResponse(BaseModel):
    """
    User subscription storing in Bugout resources.
    """

    user_id: str
    blockchain: str


class SubscriptionsListResponse(BaseModel):
    subscriptions: List[SubscriptionResponse] = Field(default_factory=list)


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
    gasPrice: int
    value: int
    from_address: str = Field(alias="from")
    to_address: Optional[str] = Field(default=None, alias="to")
    hash: Optional[str] = None
    input: Optional[str] = None


class TxinfoEthereumBlockchainRequest(BaseModel):
    tx: EthereumTransaction


class TxinfoEthereumBlockchainResponse(BaseModel):
    tx: EthereumTransaction
    abi: Optional[ContractABI] = None
    errors: List[str] = Field(default_factory=list)

