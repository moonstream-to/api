"""
Convert all addresses in user subscriptions to checksum address.
"""
from bugout.data import BugoutResources
from bugout.exceptions import BugoutResponseException
from sqlalchemy.orm.session import Session
from web3 import Web3

from ...settings import BUGOUT_REQUEST_TIMEOUT_SECONDS, MOONSTREAM_ADMIN_ACCESS_TOKEN
from ...settings import bugout_client as bc


def checksum_all_subscription_addresses(web3: Web3) -> None:
    resources: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": "subscription"},
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )
    for resource in resources.resources:
        resource_data = resource.resource_data
        try:
            address = resource_data["address"]
            resource_data["address"] = web3.toChecksumAddress(address)
            updated_resource = bc.update_resource(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                resource_id=resource.id,
                resource_data={"update": resource_data},
                timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
            )
            print(f"Resource id: {updated_resource.id} updated")
        except ValueError as e:
            print(
                f"Not valid checksum address: {address}, probably "
                "txpool or whalewatch subscription"
            )
            continue
        except BugoutResponseException as e:
            print(f"Bugout error: {e.status_code} with details: {e.detail}")
        except Exception as e:
            print(f"Unexpected error: {repr(e)}")
            continue


def checksum_all_labels_addresses(db_session: Session) -> None:
    pass
