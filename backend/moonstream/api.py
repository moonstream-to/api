"""
The Moonstream HTTP API
"""
import logging
from typing import Any, Dict, List, Optional
import uuid

from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    Form,
    HTTPException,
    Path,
    Query,
    Request,
    Response,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from . import data
from .settings import DOCS_TARGET_PATH, ORIGINS
from .version import MOONSTREAM_VERSION

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tags_metadata = [{"name": "users", "description": "Operations with users."}]

app = FastAPI(
    title=f"Moonstream API.",
    description="The Bugout blockchain inspector API.",
    version=MOONSTREAM_VERSION,
    openapi_tags=tags_metadata,
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=f"/{DOCS_TARGET_PATH}",
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping", response_model=data.PingResponse)
async def ping() -> data.PingResponse:
    return data.PingResponse(status="ok")


@app.get("/version", response_model=data.VersionResponse)
async def version() -> data.VersionResponse:
    return data.VersionResponse(version=MOONSTREAM_VERSION)
