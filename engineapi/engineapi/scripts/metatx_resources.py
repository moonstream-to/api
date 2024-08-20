import argparse
import sys
import time
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy.sql import delete, distinct, func, insert, update

from .. import db, models
from ..contracts_actions import (
    create_resource_for_registered_contract,
    delete_resource_for_registered_contract,
)


def update_to_resource_handler(args: argparse.Namespace):
    """
    Loop:
    1. Fetch all registered contracts
    2. Generate resource
    3. Grant permissions for resource to metatx requesters
    4. Replace metatx requester in registered contracts table with uuid of resource
    """
    with db.yield_db_session_ctx() as db_session:
        call_request_subquery = (
            db_session.query(
                models.CallRequest.registered_contract_id,
                func.count(models.CallRequest.id).label("call_requests_cnt"),
            )
            .group_by(models.CallRequest.registered_contract_id)
            .subquery()
        )

        query = (
            db_session.query(
                models.RegisteredContract.id,
                models.MetatxRequester.id,
                func.coalesce(call_request_subquery.c.call_requests_cnt, 0).label(
                    "call_requests_cnt"
                ),
            )
            .outerjoin(
                models.MetatxRequester,
                models.RegisteredContract.metatx_requester_id
                == models.MetatxRequester.id,
            )
            .outerjoin(
                call_request_subquery,
                models.RegisteredContract.id
                == call_request_subquery.c.registered_contract_id,
            )
            .group_by(
                models.RegisteredContract.id,
                models.MetatxRequester.id,
                call_request_subquery.c.call_requests_cnt,
            )
        )

        result = query.all()

        print(
            "RegisteredContract.id                 |   MetatxRequester.id                    |   call_requests_cnt"
        )
        print(
            "                                      |                                         |   "
        )
        for rc in result:
            print(f"{rc[0]}  |   {rc[1]}  |   {rc[2]}")
        print("\n")

        print(f"There are {len(result)} total results")

        response = input(f"Continue? (yes/y): ").strip().lower()
        if response != "yes" and response != "y":
            sys.exit(0)
        print("\n")

        for (
            registered_contract_id,
            metatx_requester_id,
            call_requests_cnt,
        ) in result:
            print(
                f"Processing registered_contract_id: {registered_contract_id} with metatx_requester_id: {metatx_requester_id} and call_requests_cnt: {call_requests_cnt}"
            )

            # Create Brood resource and grant permissions to user
            try:
                resource_id = create_resource_for_registered_contract(
                    registered_contract_id=registered_contract_id,
                    user_id=metatx_requester_id,
                )
            except Exception as e:
                print(
                    f"Failed to create resource for registered_contract_id: {registered_contract_id} for user_id: metatx_requester_id, err: {e}"
                )

                response = input(f"Continue? (yes/y): ").strip().lower()
                if response != "yes" and response != "y":
                    sys.exit(0)

                continue

            try:
                # Create new metatx_requester_id equal to resource ID
                metatx_requester_stmt = insert(models.MetatxRequester).values(
                    id=str(resource_id)
                )
                db_session.execute(metatx_requester_stmt)

                # Update RegisteredContract table with metatx_requester_id set to resource ID
                update_registered_contract = (
                    update(models.RegisteredContract)
                    .where(models.RegisteredContract.id == registered_contract_id)
                    .values(metatx_requester_id=str(resource_id))
                )
                db_session.execute(update_registered_contract)

                # Update CallRequest table with metatx_requester_id set to resource ID
                update_call_request = (
                    update(models.CallRequest)
                    .where(
                        models.CallRequest.registered_contract_id
                        == str(registered_contract_id)
                    )
                    .values(metatx_requester_id=str(resource_id))
                )
                db_session.execute(update_call_request)

                db_session.commit()
                print(
                    f"Updated all metatx_requester_id for registered_contract_id: {str(registered_contract_id)} and belonging call_requests to resource_id: {str(resource_id)} successfully in each table"
                )
            except Exception as e:
                db_session.rollback()
                delete_resource_for_registered_contract(resource_id=resource_id)
                print(
                    f"Failed to update metatx_requester_id in database, reverted changes, err: {e}"
                )

                response = input(f"Continue? (yes/y): ").strip().lower()
                if response != "yes" and response != "y":
                    sys.exit(0)

            print("\n")
            time.sleep(1)


def clean_metatx_requesters_handler(args: argparse.Namespace):
    """
    Search for all metatx requesters in the metatx_requesters table that are
    not associated with any registered contract or call request, and delete them one by one.
    """
    with db.yield_db_session_ctx() as db_session:
        query = (
            db_session.query(models.MetatxRequester.id)
            .outerjoin(
                models.RegisteredContract,
                models.MetatxRequester.id
                == models.RegisteredContract.metatx_requester_id,
            )
            .outerjoin(
                models.CallRequest,
                models.MetatxRequester.id == models.CallRequest.metatx_requester_id,
            )
            .filter(
                models.RegisteredContract.id.is_(None),
                models.CallRequest.id.is_(None),
            )
            .group_by(models.MetatxRequester.id)
        )

        result = query.all()
        if len(result) == 0:
            print(
                "There are no metatx requesters that are not associated with any registered contract or call request"
            )
            sys.exit(0)

        print("MetatxRequester.id")
        print("\n")
        for rc in result:
            print(f"{rc[0]}")
        print("\n")

        print(f"There are {len(result)} total results")

        response = input(f"Continue? (yes/y): ").strip().lower()
        if response != "yes" and response != "y":
            sys.exit(0)
        print("\n")

        for metatx_requester_id in result:
            print(
                f"Processing deletion of metatx_requester_id: {metatx_requester_id[0]}"
            )

            try:
                delete_metatx_requester = delete(models.MetatxRequester).where(
                    models.MetatxRequester.id == str(metatx_requester_id[0])
                )
                db_session.execute(delete_metatx_requester)
                db_session.commit()
            except Exception as e:
                db_session.rollback()
                print(
                    f"Failed to delete metatx_requester_id: {metatx_requester_id}, err: {e}"
                )

                response = input(f"Continue? (yes/y): ").strip().lower()
                if response != "yes" and response != "y":
                    sys.exit(0)

                continue


def main():
    parser = argparse.ArgumentParser(
        description="Generates for Metatx requesters Brood resources"
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers()

    update_to_resource_parser = subparsers.add_parser(
        "update-to-resource", help="Generate resource and update metatx with it's ID"
    )

    update_to_resource_parser.set_defaults(func=update_to_resource_handler)

    clean_metatx_requesters_parser = subparsers.add_parser(
        "clean-metatx-requesters",
        help="Clean metatx requesters not belong to any registered contract or call request",
    )

    clean_metatx_requesters_parser.set_defaults(func=clean_metatx_requesters_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
