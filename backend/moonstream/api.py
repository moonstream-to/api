"""
The Moonstream HTTP API
"""
import logging
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import data
from .routes.subscriptions import app as subscriptions_api
from .routes.users import app as users_api
from .routes.txinfo import app as txinfo_api
from .routes.streams import app as streams_api
from .routes.address_info import app as addressinfo_api

from .settings import ORIGINS
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


@app.get("/now", tags=["time"])
async def now_handler() -> data.NowResponse:
    return data.NowResponse(epoch_time=time.time())


app.mount("/subscriptions", subscriptions_api)
app.mount("/users", users_api)
app.mount("/streams", streams_api)
app.mount("/txinfo", txinfo_api)
app.moount("/addressinfo", addressinfo_api)
