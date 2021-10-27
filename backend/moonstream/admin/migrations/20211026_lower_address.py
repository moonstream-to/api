"""
Convert all addresses in user subscriptions to lowercase.

- Fetch all possible subscriptions in Brood resources
with admin access token
- Lowercase it
"""
from bugout.data import BugoutResource, BugoutResources

from ...settings import BUGOUT_REQUEST_TIMEOUT_SECONDS, MOONSTREAM_ADMIN_ACCESS_TOKEN
from ...settings import bugout_client as bc


def main() -> None:
    resources: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": "subscription_type"},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )
    for resource in resources:
        resource_data_updated = resource.resource_data
        print(resource.resource_data)
        # bc.update_resource(token=MOONSTREAM_ADMIN_ACCESS_TOKEN, resource_id=resource.id, )


if __name__ == "__main__":
    main()
