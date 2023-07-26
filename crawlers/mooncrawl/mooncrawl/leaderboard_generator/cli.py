import argparse
import json
import logging
import os
from typing import Any, Dict
import uuid

import requests  # type: ignore


from .utils import get_results_for_moonstream_query
from ..settings import (
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_LEADERBOARD_GENERATOR_JOURNAL_ID,
    BUGOUT_REQUEST_TIMEOUT_SECONDS,
)

from ..settings import bugout_client as bc


logging.basicConfig()
logger = logging.getLogger(__name__)


def handle_leaderboards(args: argparse.Namespace) -> None:
    """
    Run the leaderboard generator.

    Get query from journal and push results to leaderboard API.
    """

    ### get leaderboard journal

    query = "#leaderboard"

    if args.leaderboard_id:
        query += f" #cleaderboard_id:{args.leaderboard_id}"

    leaderboards = bc.search(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        journal_id=MOONSTREAM_LEADERBOARD_GENERATOR_JOURNAL_ID,
        query=query,
        limit=1,
        timeout=BUGOUT_REQUEST_TIMEOUT_SECONDS,
    )

    if len(leaderboards.results) == 0:
        raise ValueError("No leaderboard found")

    for leaderboard in leaderboards.results:
        if leaderboard.content is None:
            continue

        try:
            leaderboard_data = json.loads(leaderboard.content)
        except json.JSONDecodeError:
            logger.error(
                f"Could not parse leaderboard content: {[tag for tag in leaderboard.tags if tag.startswith('leaderboard_id')]}"
            )
            continue

        ### get results from query API

        leaderboard_id = leaderboard_data["leaderboard_id"]

        query_name = leaderboard_data["query_name"]

        if args.params:
            params = json.loads(args.params)
        else:
            params = leaderboard_data["params"]

        ### execute query

        query_results = get_results_for_moonstream_query(
            args.query_api_access_token,
            query_name,
            params,
            args.query_api,
            args.max_retries,
            args.interval,
        )

        ### push results to leaderboard API

        if query_results is None:
            logger.error(f"Could not get results for query {query_name}")
            continue

        leaderboard_push_api_url = (
            f"{args.engine_api}/leaderboard/{leaderboard_id}/scores"
        )

        leaderboard_api_headers = {
            "Authorization": f"Bearer {args.query_api_access_token}",
            "Content-Type": "application/json",
        }

        leaderboard_api_response = requests.put(
            leaderboard_push_api_url,
            json=query_results["data"],
            headers=leaderboard_api_headers,
            timeout=10,
        )

        try:
            leaderboard_api_response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            logger.error(
                f"Could not push results to leaderboard API: {http_error.response.text} with status code {http_error.response.status_code}"
            )
            continue

        ### get leaderboard from leaderboard API

        leaderboard_api_info_url = (
            f"{args.engine_api}/leaderboard/info?leaderboard_id={leaderboard_id}"
        )

        leaderboard_api_response = requests.get(
            leaderboard_api_info_url, headers=leaderboard_api_headers, timeout=10
        )

        try:
            leaderboard_api_response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            logger.error(
                f"Could not get leaderboard info from leaderboard API: {http_error.response.text} with status code {http_error.response.status_code}"
            )
            continue

        info = leaderboard_api_response.json()

        logger.info(
            f"Successfully pushed results to leaderboard {info['id']}: {info['title']}"
        )


def main():
    """
    Generates an argument parser for the "autocorns judge" command.
    """

    parser = argparse.ArgumentParser(description="The Judge: Generate leaderboards")
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers()

    shadowcorns_throwing_shade_parser = subparsers.add_parser(
        "leaderboards-generate", description="Generate Leaderboard"
    )
    shadowcorns_throwing_shade_parser.add_argument(
        "--query-api",
        default="https://api.moonstream.to",
        help="Moonstream API URL. Access token expected to be set as MOONSTREAM_ACCESS_TOKEN environment variable.",
    )
    shadowcorns_throwing_shade_parser.add_argument(
        "--engine-api",
        default="https://engineapi.moonstream.to",
        help="Moonstream Engine API URL. Access token expected to be set as MOONSTREAM_ACCESS_TOKEN environment variable.",
    )
    shadowcorns_throwing_shade_parser.add_argument(
        "--leaderboard-id",
        type=uuid.UUID,
        required=False,
        help="Leaderboard ID on Engine API",
    )
    shadowcorns_throwing_shade_parser.add_argument(
        "--max-retries",
        type=int,
        default=100,
        help="Number of times to retry requests for Moonstream Query results",
    )
    shadowcorns_throwing_shade_parser.add_argument(
        "--interval",
        type=float,
        default=30.0,
        help="Number of seconds to wait between attempts to get results from Moonstream Query API",
    )
    shadowcorns_throwing_shade_parser.add_argument(
        "--params",
        type=json.loads,
        required=False,
        help="Parameters to pass to Moonstream Query API",
    )
    shadowcorns_throwing_shade_parser.add_argument(
        "--query-api-access-token",
        type=str,
        required=True,
        help="Moonstream Access Token to use for Moonstream Query API requests",
    )

    shadowcorns_throwing_shade_parser.set_defaults(func=handle_leaderboards)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
