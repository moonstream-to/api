import argparse
import sys
import time
from typing import Any, Dict, List, Optional

from bugout.data import BugoutResourceHolder
from sqlalchemy.sql import delete, distinct, func, insert, update

from .. import db, models
from ..settings import (
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_APPLICATION_ID,
    bugout_client,
)


def generate_handler(args: argparse.Namespace):
    """
    Loop:
    1. Fetch metatx requester
    2. Generate resource
    3. Grant permissions for resource to metatx requester
    4. Replace metatx requester table with uuid of resource
    """
    resource_data = {"type": "metatx_requester"}

    with db.yield_db_session_ctx() as db_session:
        query = (
            db_session.query(
                models.MetatxRequester.id,
                func.count(distinct(models.RegisteredContract.id)).label(
                    "registered_contracts_cnt"
                ),
                func.count(distinct(models.CallRequest.id)).label("call_requests_cnt"),
            )
            .outerjoin(
                models.RegisteredContract,
                models.RegisteredContract.metatx_requester_id
                == models.MetatxRequester.id,
            )
            .outerjoin(
                models.CallRequest,
                models.CallRequest.metatx_requester_id == models.MetatxRequester.id,
            )
            .group_by(models.MetatxRequester.id)
        )

        result = query.all()

        print(f"There are {len(result)} total results")

        response = input(f"Continue? (yes/y): ").strip().lower()
        if response != "yes" and response != "y":
            sys.exit(0)
        print("\n")

        for mr_id, registered_contracts_cnt, call_requests_cnt in query.all():
            print(
                f"Processing metatx_requester_id: {mr_id} with registered_contracts_cnt: {registered_contracts_cnt} and call_requests_cnt: {call_requests_cnt}"
            )

            # Create Brood resource
            try:
                resource = bugout_client.create_resource(
                    token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                    application_id=MOONSTREAM_APPLICATION_ID,
                    resource_data=resource_data,
                )
                print(f"Created resource with ID: {resource.id}")
            except Exception as e:
                print(str(e))
                continue

            # Grant access for resource to metatx requester
            try:
                resource_holder = bugout_client.add_resource_holder_permissions(
                    token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                    resource_id=resource.id,
                    holder_permissions=BugoutResourceHolder(
                        holder_id=str(mr_id),
                        holder_type="user",
                        permissions=["create", "read", "update", "delete"],
                    ),
                )
                print("Granted permissions for resource to metatx requester")
            except Exception as e:
                print(str(e))
                continue

            try:
                # Create new metatx_requester_id equal to resource ID
                metatx_requester_stmt = insert(models.MetatxRequester).values(
                    id=str(resource.id)
                )
                db_session.execute(metatx_requester_stmt)

                # Update RegisteredContract table
                update_registered_contract = (
                    update(models.RegisteredContract)
                    .where(models.RegisteredContract.metatx_requester_id == str(mr_id))
                    .values(metatx_requester_id=str(resource.id))
                )
                db_session.execute(update_registered_contract)

                # Update CallRequest table
                update_call_request = (
                    update(models.CallRequest)
                    .where(models.CallRequest.metatx_requester_id == str(mr_id))
                    .values(metatx_requester_id=str(resource.id))
                )
                db_session.execute(update_call_request)

                # Delete old metatx_requester_id
                delete_metatx_requester = delete(models.MetatxRequester).where(
                    models.MetatxRequester.id == str(mr_id)
                )
                db_session.execute(delete_metatx_requester)

                db_session.commit()
                print(
                    f"Updated all metatx_requester_id from {str(mr_id)} to {str(resource.id)} successfully in each table"
                )

            except Exception as e:
                db_session.rollback()
                print(f"Failed to update metatx_requester_id: {e}")

                response = input(f"Continue? (yes/y): ").strip().lower()
                if response != "yes" and response != "y":
                    sys.exit(0)

            print("\n")
            time.sleep(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generates for Metatx requesters Brood resources"
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers()

    generate_parser = subparsers.add_parser("generate", help="Generate resources")

    generate_parser.set_defaults(func=generate_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
