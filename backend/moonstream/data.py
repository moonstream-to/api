"""
Pydantic schemas for the Moonstream HTTP API
"""
import uuid
from typing import List

from pydantic import BaseModel


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
    blockchain: str


class SubscriptionResponse(BaseModel):
    user_id: str
    blockchain: str


class SubscriptionsListResponse(BaseModel):
    subscriptions: List[SubscriptionResponse]
