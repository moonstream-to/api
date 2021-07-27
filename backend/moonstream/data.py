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
    subscriptions: List[SubscriptionResourceData] = Field(default_factory=list)
