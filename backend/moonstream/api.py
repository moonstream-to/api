"""
The Moonstream HTTP API
"""
import logging
import time
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import data
from .routes.address_info import router as addressinfo_router
from .routes.streams import router as streams_router
from .routes.subscriptions import router as subscriptions_router
from .routes.txinfo import router as txinfo_router
from .routes.users import router as users_router

from .middleware import BroodAuthMiddleware
from .settings import DOCS_TARGET_PATH, ORIGINS
from .version import MOONSTREAM_VERSION

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


tags_metadata = [
    {"name": "addressinfo", "description": "Address public information."},
    {"name": "labels", "description": "Addresses label information."},
    {"name": "streams", "description": "Operations with data stream and filters."},
    {"name": "subscriptions", "description": "Operations with subscriptions."},
    {"name": "time", "description": "Timestamp endpoints."},
    {"name": "tokens", "description": "Operations with user tokens."},
    {"name": "txinfo", "description": "Ethereum transactions info."},
    {"name": "users", "description": "Operations with users."},
]

app = FastAPI(
    title=f"Moonstream API",
    description="Moonstream API endpoints.",
    version=MOONSTREAM_VERSION,
    openapi_tags=tags_metadata,
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=f"/{DOCS_TARGET_PATH}",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
whitelist_paths: Dict[str, str] = {}
whitelist_paths.update(
    {
        "/ping": "GET",
        "/version": "GET",
        "/now": "GET",
        "/docs": "GET",
        "/openapi.json": "GET",
        "/streams/info": "GET",
        "/subscriptions/types": "GET",
        "/users": "POST",
        "/users/token": "POST",
        "/users/password/reset_initiate": "POST",
        "/users/password/reset_complete": "POST",
    }
)
app.add_middleware(BroodAuthMiddleware, whitelist=whitelist_paths)


@app.get("/ping", response_model=data.PingResponse)
async def ping_handler() -> data.PingResponse:
    return data.PingResponse(status="ok")


@app.get("/version", response_model=data.VersionResponse)
async def version_handler() -> data.VersionResponse:
    return data.VersionResponse(version=MOONSTREAM_VERSION)


@app.get("/now", tags=["time"])
async def now_handler() -> data.NowResponse:
    return data.NowResponse(epoch_time=time.time())


app.include_router(addressinfo_router)
app.include_router(streams_router)
app.include_router(subscriptions_router)
app.include_router(txinfo_router)
app.include_router(users_router)

# app.mount("/address_info", addressinfo_api)
