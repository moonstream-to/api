import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class APISpec:
    url: str
    endpoints: Dict[str, str]


class AuthType(Enum):
    bearer = "Bearer"
    web3 = "Web3"


class Method(Enum):
    DELETE = "delete"
    GET = "get"
    POST = "post"
    PUT = "put"


class OutputType(Enum):
    CSV = "csv"
    JSON = "json"


@dataclass(frozen=True)
class MoonstreamQuery:
    id: uuid.UUID
    name: str
    journal_url: Optional[str] = None
    query: Optional[str] = None
    tags: Optional[List[str]] = None
    user: Optional[str] = None
    user_id: Optional[uuid.UUID] = None
    query_type: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass(frozen=True)
class MoonstreamQueries:
    queries: List[MoonstreamQuery]


@dataclass(frozen=True)
class MoonstreamQueryResultUrl:
    url: str
