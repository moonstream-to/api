"""
The Moonstream HTTP API
"""
import logging

from bugout.data import BugoutUser
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

from . import data
from .routes.users import app as users_api
from .settings import ORIGINS, bugout_client as bc, MOONSTREAM_APPLICATION_ID
from .version import MOONSTREAM_VERSION

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(openapi_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping", response_model=data.PingResponse)
async def ping_handler() -> data.PingResponse:
    return data.PingResponse(status="ok")


@app.get("/version", response_model=data.VersionResponse)
async def version_handler() -> data.VersionResponse:
    return data.VersionResponse(version=MOONSTREAM_VERSION)


app.mount("/users", users_api)
