import unittest
import uuid
from datetime import datetime

from bugout.data import BugoutResource, BugoutResources, BugoutUser
from pydantic import AnyHttpUrl, parse_obj_as

from .middleware import parse_origins_from_resources
from .settings import BUGOUT_RESOURCE_TYPE_APPLICATION_CONFIG

TEST_ALLOW_ORIGINS = ["http://localhost:3000", "http://localhost:4000", "wrong one"]


class TestInit(unittest.TestCase):
    def setUp(self):
        utc_now = datetime.utcnow()
        self.resources: BugoutResources = BugoutResources(
            resources=[
                BugoutResource(
                    id=uuid.uuid4(),
                    application_id=str(uuid.uuid4()),
                    resource_data={
                        "type": BUGOUT_RESOURCE_TYPE_APPLICATION_CONFIG,
                        "setting": "cors",
                        "user_id": str(uuid.uuid4()),
                        "cors": TEST_ALLOW_ORIGINS,
                    },
                    created_at=utc_now,
                    updated_at=utc_now,
                )
            ]
        )

    def test_parse_origins_from_resources(self):
        cnt = 0
        for o in TEST_ALLOW_ORIGINS:
            try:
                parse_obj_as(AnyHttpUrl, o)
                cnt += 1
            except Exception:
                continue
        cors_origins = parse_origins_from_resources(self.resources)
        self.assertEqual(cnt, len(cors_origins))
