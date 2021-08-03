"""
Pydantic schemas for the Moonstream HTTP API
"""
from enum import Enum
from typing import List, Optional

from sqlalchemy.sql.operators import notendswith_op


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
    gasPrice: int
    value: int
    from_address: str
    to_address: Optional[str]
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


class EthereumTransactionResponse(BaseModel):
    stream: List[EthereumTransactionItem]


class TxinfoEthereumBlockchainRequest(BaseModel):
    tx: EthereumTransaction


class TxinfoEthereumBlockchainResponse(BaseModel):
    tx: EthereumTransaction
    is_smart_contract_deployment: bool = False
    is_smart_contract_call: bool = False
    smart_contract_address: Optional[str] = None
    abi: Optional[ContractABI] = None
    errors: List[str] = Field(default_factory=list)
