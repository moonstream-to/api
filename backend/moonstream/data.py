"""
Pydantic schemas for the Moonstream HTTP API
"""
from typing import List, Optional

from pydantic import BaseModel, Field


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
    text_signature_candidates: Optional[List[str]] = None


class EVMEventSignature(BaseModel):
    type = "event"
    hex_signature: str
    text_signature_candidates: Optional[List[str]] = None

class ContractABI(BaseModel):
    functions: List[EVMFunctionSignature]
    events: List[EVMEventSignature]