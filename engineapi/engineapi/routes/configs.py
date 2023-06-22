import logging
from typing import Any, Dict, List, Set

from bugout.data import BugoutResource
from fastapi import (
    BackgroundTasks,
    Body,
    Depends,
    FastAPI,
    HTTPException,
    Query,
    Request,
)
from pydantic import AnyHttpUrl

from .. import actions, data
from ..middleware import (
    BroodAuthMiddleware,
    BugoutCORSMiddleware,
    EngineHTTPException,
    check_default_origins,
    fetch_and_set_cors_origins_cache,
    parse_origins_from_resources,
)
from ..settings import (
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
    BUGOUT_RESOURCE_TYPE_APPLICATION_CONFIG,
    DOCS_TARGET_PATH,
    MOONSTREAM_ADMIN_USER,
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


@app.get("/cors", response_model=data.CORSResponse)
async def get_cors(
    request: Request,
) -> data.CORSResponse:
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
        resource_origins_set: Set[str] = parse_origins_from_resources(
            resources.resources
        )
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    return data.CORSResponse(cors=list(resource_origins_set))


@app.put("/cors", response_model=data.CORSResponse)
async def update_cors(
    request: Request,
    background_tasks: BackgroundTasks,
    new_origins: List[AnyHttpUrl] = Body(...),
) -> data.CORSResponse:
    new_origins = set(new_origins)

    try:
        target_resource: BugoutResource

        resources = bc.list_resources(
            token=request.state.token,
            params={
                "application_id": MOONSTREAM_APPLICATION_ID,
                "type": BUGOUT_RESOURCE_TYPE_APPLICATION_CONFIG,
                "setting": "cors",
            },
            timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
        )
        if len(resources.resources) == 0:
            target_resource = bc.create_resource(
                token=request.state.token,
                application_id=MOONSTREAM_APPLICATION_ID,
                resource_data={
                    "type": BUGOUT_RESOURCE_TYPE_APPLICATION_CONFIG,
                    "setting": "cors",
                    "user_id": str(request.state.user.id),
                    "origins": list(new_origins),
                },
            )
            bc.add_resource_holder_permissions(
                token=request.state.token,
                resource_id=target_resource.id,
                holder_permissions={
                    "holder_id": str(MOONSTREAM_ADMIN_USER.id),
                    "holder_type": "user",
                    "permissions": ["admin", "create", "read", "update", "delete"],
                },
            )
        elif len(resources.resources) == 1:
            target_resource = resources.resources[0]
            resource_origins_set: Set[str] = parse_origins_from_resources(
                [target_resource]
            )
            resource_origins_set.update(new_origins)

            target_resource = bc.update_resource(
                token=request.state.token,
                resource_id=target_resource.id,
                resource_data={
                    "update": {"origins": list(resource_origins_set)},
                    "drop_keys": [],
                },
            )
        elif len(resources.resources) > 1:
            # TODO(kompotkot): Remove all resource and save only one
            raise EngineHTTPException(status_code=500)
    except Exception as err:
        logger.error(repr(err))
        raise EngineHTTPException(status_code=500)

    background_tasks.add_task(
        fetch_and_set_cors_origins_cache,
    )

    return data.CORSResponse(cors=target_resource.resource_data["origins"])
