import argparse
import logging
import os

from bugout.app import Bugout

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migration_20230522(
    token_current_owner: str, token_new_owner: str, new_application_id: str
) -> None:
    BUGOUT_BROOD_URL = os.environ.get("BUGOUT_BROOD_URL", "https://auth.bugout.dev")

    bc = Bugout(brood_api_url=BUGOUT_BROOD_URL)

    try:
        resources = bc.list_resources(token=token_current_owner, params={})
    except Exception as err:
        raise Exception(err)

    logger.info(f"Found {len(resources.resources)} resources")

    while input("Do you want to continue [y/n]? ") != "y":
        return

    cnt = 0
    for resource in resources.resources:
        resource_data = resource.resource_data
        resource_data["type"] = "nodebalancer-access"

        try:
            new_resource = bc.create_resource(
                token=token_new_owner,
                application_id=new_application_id,
                resource_data=resource_data,
            )
            cnt += 1
            logger.info(
                f"Created resource with ID {new_resource.id} and copied modified resource data"
            )
        except Exception as err:
            logger.error(f"Unable to copy resource with ID {resource.id}, err: {err}")

        user_id = new_resource.resource_data.get("user_id", "")

        try:
            new_permissions = bc.add_resource_holder_permissions(
                token=token_new_owner,
                resource_id=new_resource.id,
                holder_permissions={
                    "holder_id": user_id,
                    "holder_type": "user",
                    "permissions": ["read", "update", "delete"],
                },
            )
            logger.info(
                f"Granted permissions for resource with ID {new_permissions.resource_id} to user with ID {user_id}"
            )
        except Exception as err:
            logger.error(
                f"Unable grant permissions for resource with ID {resource.id} to user with ID {user_id}, err: {err}"
            )

    logger.info(f"Copied {cnt} resources")


MIGRATIONS_LIST = {
    "20230522": {
        "description": "Modify existing Brood resources to Moonstream resources structure "
        "with `type` key equal to `nodebalancer-access`. And transfer ownership to moonstream admin. "
        "Then create permissions for user access.",
        "exec_func": migration_20230522,
        "required_args": [
            "token-current-owner",
            "token-new-owner",
            "new-application-id",
        ],
    }
}


def list_handler(args: argparse.Namespace) -> None:
    return print(MIGRATIONS_LIST)


def run_handler(args: argparse.Namespace) -> None:
    migration = MIGRATIONS_LIST.get(args.key, None)
    if migration is None:
        logger.error(f"Migration with key '{args.key}' not found")
        return

    migration["exec_func"](
        token_current_owner=args.token_current_owner,
        token_new_owner=args.token_new_owner,
        new_application_id=args.new_application_id,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Moonstream mode balancer migrations CLI"
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Migration commands")

    parser_list = subcommands.add_parser("list", description="List migrations")
    parser_list.set_defaults(func=list_handler)

    parser_run = subcommands.add_parser("run", description="Run migration")
    parser_run.add_argument(
        "-k", "--key", required=True, type=str, help="Key of migration to run"
    )
    parser_run.add_argument(
        "--token-current-owner",
        type=str,
        default=argparse.SUPPRESS,
        help="Bugout access token of current resource owner",
    )
    parser_run.add_argument(
        "--token-new-owner",
        type=str,
        default=argparse.SUPPRESS,
        help="Bugout access token of new resource owner",
    )
    parser_run.add_argument(
        "--new-application-id",
        type=str,
        default=argparse.SUPPRESS,
        help="Bugout application ID to transfer resources",
    )
    parser_run.set_defaults(func=run_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
