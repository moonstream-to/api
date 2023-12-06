import argparse
import json
import os
import sys
from typing import Optional
import uuid

import requests

LEADERBOARD_API_URL = os.environ.get(
    "LEADERBOARD_API_URL", "http://localhost:7191/leaderboard/"
)


def moonstream_access_token(value: Optional[str]) -> uuid.UUID:
    if value is None:
        value = os.environ.get("MOONSTREAM_ACCESS_TOKEN")

    if value is None:
        raise ValueError(
            "Moonstream access token is required: either via -A/--authorization, or via the MOONSTREAM_ACCESS_TOKEN environment variable"
        )

    try:
        value_uuid = uuid.UUID(value)
    except Exception:
        raise ValueError("Moonstream access token must be a valid UUID")

    return value_uuid


def requires_authorization(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-A",
        "--authorization",
        type=moonstream_access_token,
        required=False,
        default=os.environ.get("MOONSTREAM_ACCESS_TOKEN"),
        help="Moonstream API access token (if not provided, must be specified using the MOONSTREAM_ACCESS_TOKEN environment variable)",
    )


def handle_get(args: argparse.Namespace) -> None:
    url = LEADERBOARD_API_URL
    params = {
        "leaderboard_id": str(args.id),
        "limit": str(args.limit),
        "offset": str(args.offset),
    }
    if args.version is not None:
        params["version"] = str(args.version)

    response = requests.get(url, params=params)
    response.raise_for_status()

    print(json.dumps(response.json()))


def handle_create(args: argparse.Namespace) -> None:
    url = LEADERBOARD_API_URL

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {str(args.authorization)}",
    }

    body = {
        "title": args.title,
        "description": args.description,
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    print(json.dumps(response.json()))


def handle_versions(args: argparse.Namespace) -> None:
    url = f"{LEADERBOARD_API_URL}{args.id}/versions"

    headers = {
        "Authorization": f"Bearer {str(args.authorization)}",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print(json.dumps(response.json()))


def handle_create_version(args: argparse.Namespace) -> None:
    url = f"{LEADERBOARD_API_URL}{args.id}/versions"

    headers = {
        "Authorization": f"Bearer {str(args.authorization)}",
        "Content-Type": "application/json",
    }

    body = {
        "publish": args.publish,
    }

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    print(json.dumps(response.json()))


def handle_publish(args: argparse.Namespace) -> None:
    url = f"{LEADERBOARD_API_URL}{args.id}/versions/{args.version}"

    headers = {
        "Authorization": f"Bearer {str(args.authorization)}",
        "Content-Type": "application/json",
    }

    body = {
        "publish": args.publish,
    }

    response = requests.put(url, headers=headers, json=body)
    response.raise_for_status()
    print(json.dumps(response.json()))


def handle_upload_scores(args: argparse.Namespace) -> None:
    url = f"{LEADERBOARD_API_URL}{args.id}/scores"
    if args.version is not None:
        url = f"{LEADERBOARD_API_URL}{args.id}/versions/{args.version}/scores"

    params = {
        "overwrite": "true",
        "normalize_addresses": "false",
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {str(args.authorization)}",
    }

    if args.scores is None:
        args.scores = sys.stdin

    with args.scores as ifp:
        body = json.load(ifp)

    response = requests.put(url, headers=headers, params=params, json=body)
    response.raise_for_status()
    print(json.dumps(response.json()))


def generate_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="HTTP client for Leaderboard API")
    parser.set_defaults(func=lambda _: parser.print_help())

    subparsers = parser.add_subparsers()

    # GET /leaderboard/?leaderboard_id=<id>&limit=<limit>&offset=<offset>&version=<version>
    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("-i", "--id", type=uuid.UUID, required=True)
    get_parser.add_argument("-l", "--limit", type=int, default=10)
    get_parser.add_argument("-o", "--offset", type=int, default=0)
    get_parser.add_argument("-v", "--version", type=int, default=None)
    get_parser.set_defaults(func=handle_get)

    # POST /leaderboard/
    create_parser = subparsers.add_parser("create")
    create_parser.add_argument(
        "-t", "--title", type=str, required=True, help="Title for leaderboard"
    )
    create_parser.add_argument(
        "-d",
        "--description",
        type=str,
        required=False,
        default="",
        help="Description for leaderboard",
    )
    requires_authorization(create_parser)
    create_parser.set_defaults(func=handle_create)

    # GET /leaderboard/<id>/versions
    versions_parser = subparsers.add_parser("versions")
    versions_parser.add_argument("-i", "--id", type=uuid.UUID, required=True)
    requires_authorization(versions_parser)
    versions_parser.set_defaults(func=handle_versions)

    # POST /leaderboard/<id>/versions
    create_version_parser = subparsers.add_parser("create-version")
    create_version_parser.add_argument("-i", "--id", type=uuid.UUID, required=True)
    create_version_parser.add_argument(
        "--publish",
        action="store_true",
        help="Set this flag to publish the version immediately upon creation",
    )
    requires_authorization(create_version_parser)
    create_version_parser.set_defaults(func=handle_create_version)

    # PUT /leaderboard/<id>/versions/<version>
    publish_parser = subparsers.add_parser("publish")
    publish_parser.add_argument("-i", "--id", type=uuid.UUID, required=True)
    publish_parser.add_argument("-v", "--version", type=int, required=True)
    publish_parser.add_argument(
        "--publish", action="store_true", help="Set to publish, leave to unpublish"
    )
    requires_authorization(publish_parser)
    publish_parser.set_defaults(func=handle_publish)

    # PUT /leaderboard/<id>/scores and PUT /leaderboard/<id>/versions/<version>/scores
    upload_scores_parser = subparsers.add_parser("upload-scores")
    upload_scores_parser.add_argument("-i", "--id", type=uuid.UUID, required=True)
    upload_scores_parser.add_argument(
        "-v",
        "--version",
        type=int,
        required=False,
        default=None,
        help="Specify a version to upload scores to (if not specified a new version is created)",
    )
    upload_scores_parser.add_argument(
        "-s",
        "--scores",
        type=argparse.FileType("r"),
        required=False,
        default=None,
        help="Path to scores file. If not provided, reads from stdin.",
    )
    upload_scores_parser.set_defaults(func=handle_upload_scores)
    requires_authorization(upload_scores_parser)

    return parser


if __name__ == "__main__":
    parser = generate_cli()
    args = parser.parse_args()
    args.func(args)
