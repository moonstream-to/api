"""
Convert all addresses in user subscriptions 
and ethereum_labels column to checksum address.
"""
import logging
from typing import List

from bugout.data import BugoutResources
from bugout.exceptions import BugoutResponseException

from ...settings import BUGOUT_REQUEST_TIMEOUT_SECONDS, MOONSTREAM_ADMIN_ACCESS_TOKEN
from ...settings import bugout_client as bc

logger = logging.getLogger(__name__)


BUGOUT_RESOURCE_TYPE_DASHBOARD = "dashboards"


def update_dashboard_resources_key() -> None:
    """
    Parse all existing dashboards at Brood resource
    and replace key to correct one.
    Schema can use for rename first level keys
    """
    search_by_key = BUGOUT_RESOURCE_TYPE_DASHBOARD
    old_key = "dashboard_subscriptions"
    new_key = "subscription_settings"

    resources: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": search_by_key},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )
    for resource in resources.resources:
        resource_data = resource.resource_data
        try:
            if old_key not in resource_data:
                continue
            data = resource_data[old_key]
            resource_data[new_key] = data
            updated_resource = bc.update_resource(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                resource_id=resource.id,
                resource_data={"update": resource_data, "drop_keys": [old_key]},
                timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
            )
            logger.info(f"Resource id: {updated_resource.id} updated")
        except BugoutResponseException as e:
            logger.info(f"Bugout error: {e.status_code} with details: {e.detail}")
        except Exception as e:
            logger.info(f"Unexpected error: {repr(e)}")
            continue
