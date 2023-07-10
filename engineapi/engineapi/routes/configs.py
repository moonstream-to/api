import logging
from typing import Any, Dict, List, Set

from bugout.data import BugoutResource, BugoutResources
from fastapi import (
    BackgroundTasks,
    Body,
    Depends,
    FastAPI,
    Form,
    HTTPException,
    Query,
    Request,
)
from pydantic import AnyHttpUrl

from .. import data
from ..middleware import (
    BroodAuthMiddleware,
    BugoutCORSMiddleware,
    EngineHTTPException,
    create_application_settings_cors_origin,
    fetch_and_set_cors_origins_cache,
    parse_origins_from_resources,
)
from ..settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    BUGOUT_RESOURCE_TYPE_APPLICATION_CONFIG,
    DOCS_TARGET_PATH,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_APPLICATION_ID,
)
from ..settings import bugout_client as bc
from ..version import VERSION

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tags_metadata = [
    {"name": "configs", "description": "Moonstream Engine API configurations"}
]

whitelist_paths: Dict[str, str] = {}
whitelist_paths.update(
    {
        "/configs/docs": "GET",
        "/configs/openapi.json": "GET",
        "/configs/is_origin": "GET",
    }
)

app = FastAPI(
    title=f"Moonstream Engine API configurations",
    description="Moonstream Engine API configurations endpoints.",
    version=VERSION,
    openapi_tags=tags_metadata,
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=f"/{DOCS_TARGET_PATH}",
)


app.add_middleware(BroodAuthMiddleware, whitelist=whitelist_paths)

app.add_middleware(
    BugoutCORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/is_origin", response_model=data.IsCORSResponse)
async def is_cors_origin(origin: str = Query(...)) -> data.IsCORSResponse:
    is_cors_origin = data.IsCORSResponse()
    try:
        resources = bc.list_resources(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            params={
                "application_id": MOONSTREAM_APPLICATION_ID,
                "type": BUGOUT_RESOURCE_TYPE_APPLICATION_CONFIG,
                "setting": "cors",
            },
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )
        cors_origins: data.CORSOrigins = parse_origins_from_resources(
            resources.resources
        )
        if origin in cors_origins.origins_set:
            for resource in cors_origins.resources:
                resource_origin = resource.resource_data.get("origin", "")
                # TODO(kompotkot): There are could be multiple creations by different users.
                # Add logic to show most recent updated_at and oldest created_at.
                if resource_origin == origin:
                    is_cors_origin.origin = resource_origin
                    is_cors_origin.created_at = resource.created_at
                    is_cors_origin.updated_at = resource.updated_at
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    return is_cors_origin


@app.get("/origins", response_model=data.CORSOrigins)
async def get_cors_origins(
    request: Request,
) -> data.CORSOrigins:
    try:
        resources = bc.list_resources(
            token=request.state.token,
            params={
                "application_id": MOONSTREAM_APPLICATION_ID,
                "type": BUGOUT_RESOURCE_TYPE_APPLICATION_CONFIG,
                "setting": "cors",
            },
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )
        cors_origins: data.CORSOrigins = parse_origins_from_resources(
            resources.resources
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    return cors_origins


@app.post("/origin", response_model=data.CORSOrigins)
async def add_cors_origin(
    request: Request,
    background_tasks: BackgroundTasks,
    new_origin: AnyHttpUrl = Form(...),
) -> data.CORSOrigins:
    try:
        resources = bc.list_resources(
            token=request.state.token,
            params={
                "application_id": MOONSTREAM_APPLICATION_ID,
                "type": BUGOUT_RESOURCE_TYPE_APPLICATION_CONFIG,
                "setting": "cors",
            },
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )
    except Exception as err:
        logger.error(f"Unable to fetch resource from Brood, err: {repr(err)}")
        raise EngineHTTPException(status_code=500)

    cors_origins: data.CORSOrigins = parse_origins_from_resources(resources.resources)

    if new_origin in cors_origins.origins_set:
        raise EngineHTTPException(
            status_code=409,
            detail=f"Provided origin {new_origin} already set by user",
        )

    resource = create_application_settings_cors_origin(
        token=request.state.token,
        user_id=request.state.user.id,
        username=request.state.user.username,
        origin=new_origin,
    )
    cors_origins.origins_set.add(new_origin)
    cors_origins.resources.append(resource)

    background_tasks.add_task(
        fetch_and_set_cors_origins_cache,
    )

    return cors_origins
