import argparse
import json
import logging
import uuid
from typing import List, cast

import requests  # type: ignore
from bugout.data import BugoutSearchResult

from ..settings import (
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_API_URL,
    MOONSTREAM_ENGINE_URL,
    MOONSTREAM_LEADERBOARD_GENERATOR_BATCH_SIZE,
    MOONSTREAM_LEADERBOARD_GENERATOR_JOURNAL_ID,
    MOONSTREAM_LEADERBOARD_GENERATOR_PUSH_TIMEOUT_SECONDS,
)
from ..settings import bugout_client as bc
from .utils import get_results_for_moonstream_query, leaderboard_push_batch

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

blue_c = "\033[94m"
green_c = "\033[92m"
end_c = "\033[0m"


def handle_leaderboards(args: argparse.Namespace) -> None:
    """
    Run the leaderboard generator.

    Get query from journal and push results to leaderboard API.
    """

    ### get leaderboard journal

    leaderboard_push_batch_size = args.leaderboard_push_batch_size

    leaderboard_push_timeout_seconds = args.leaderboard_push_timeout_seconds

    query = "#leaderboard #status:active"

    if args.leaderboard_id:  # way to run only one leaderboard without status:active
        query = f"#leaderboard #leaderboard_id:{args.leaderboard_id}"

    try:
        leaderboards = bc.search(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            journal_id=MOONSTREAM_LEADERBOARD_GENERATOR_JOURNAL_ID,
            query=query,
            limit=100,
            timeout=10,
        )
        leaderboards_results = cast(List[BugoutSearchResult], leaderboards.results)
    except Exception as e:
        logger.error(f"Could not get leaderboards from journal: {e}")
        return

    if len(leaderboards_results) == 0:
        logger.error("No leaderboard found")
        return

    logger.info(f"Found {len(leaderboards_results)} leaderboards")

    for leaderboard in leaderboards_results:
        logger.info(
            f"Processing leaderboard: {leaderboard.title} with id: {[tag for tag in leaderboard.tags if tag.startswith('leaderboard_id')]}"
        )

        if leaderboard.content is None:
            continue

        try:
            leaderboard_data = json.loads(leaderboard.content)
        except json.JSONDecodeError:
            logger.error(
                f"Could not parse leaderboard content: {[tag for tag in leaderboard.tags if tag.startswith('leaderboard_id')]} in entry {leaderboard.entry_url.split('/')[-1]}"
            )
            continue

        ### get results from query API

        leaderboard_id = leaderboard_data["leaderboard_id"]

        query_name = leaderboard_data["query_name"]

        if args.params:
            params = json.loads(args.params)
        else:
            params = leaderboard_data["params"]

        blockchain = leaderboard_data.get("blockchain", None)
        query_params = {}

        if leaderboard_data.get("customer_id", False):
            query_params["customer_id"] = leaderboard_data["customer_id"]

        if leaderboard_data.get("instance_id", False):
            query_params["instance_id"] = str(leaderboard_data["instance_id"])

        ### execute query
        try:
            query_results = get_results_for_moonstream_query(
                args.query_api_access_token,
                query_name,
                params,
                query_params,
                blockchain,
                MOONSTREAM_API_URL,
                args.max_retries,
                args.interval,
                args.query_api_retries,
            )
        except Exception as e:
            logger.error(f"Could not get results for query {query_name}: error: {e}")
            continue

        ### push results to leaderboard API

        if query_results is None:
            logger.error(f"Could not get results for query {query_name} in time")
            continue

        leaderboard_push_api_url = f"{MOONSTREAM_ENGINE_URL}/leaderboard/{leaderboard_id}/scores?normalize_addresses={leaderboard_data['normalize_addresses']}&overwrite=true"

        leaderboard_api_headers = {
            "Authorization": f"Bearer {args.query_api_access_token}",
            "Content-Type": "application/json",
        }

        if len(query_results["data"]) > leaderboard_push_batch_size:
            logger.info(
                f"Pushing {len(query_results['data'])} scores to leaderboard {leaderboard_id} in batches of {leaderboard_push_batch_size}"
            )
            leaderboard_push_batch(
                leaderboard_id,
                leaderboard_data,
                query_results["data"],
                leaderboard_api_headers,
                leaderboard_push_batch_size,
                timeout=leaderboard_push_timeout_seconds,
            )

        else:
            try:
                leaderboard_api_response = requests.put(
                    leaderboard_push_api_url,
                    json=query_results["data"],
                    headers=leaderboard_api_headers,
                    timeout=leaderboard_push_timeout_seconds,
                )
                leaderboard_api_response.raise_for_status()
            except requests.exceptions.HTTPError as http_error:
                logger.error(
                    f"Could not push results to leaderboard API: {http_error.response.text} with status code {http_error.response.status_code}"
                )
                continue

        ### get leaderboard from leaderboard API

        leaderboard_api_info_url = (
            f"{MOONSTREAM_ENGINE_URL}/leaderboard/info?leaderboard_id={leaderboard_id}"
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
            f"Successfully pushed results to leaderboard {info['id']}:{blue_c} {info['title']} {end_c}"
        )
        logger.info(
            f"can be check on:{green_c} {MOONSTREAM_ENGINE_URL}/leaderboard/?leaderboard_id={leaderboard_id} {end_c}"
        )


def main():
    """
    CLI for generating leaderboards from Moonstream Query API
    """

    parser = argparse.ArgumentParser(description="The Judge: Generate leaderboards")
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers()

    leaderboard_generator_parser = subparsers.add_parser(
        "leaderboards-generate", description="Generate Leaderboard"
    )
    leaderboard_generator_parser.add_argument(
        "--leaderboard-id",
        type=uuid.UUID,
        required=False,
        help="Leaderboard ID on Engine API",
    )
    leaderboard_generator_parser.add_argument(
        "--max-retries",
        type=int,
        default=12,
        help="Number of times to retry requests for Moonstream Query results",
    )
    leaderboard_generator_parser.add_argument(
        "--query-api-retries",
        type=int,
        default=3,
        help="Number of times to retry updating Moonstream Query data",
    )
    leaderboard_generator_parser.add_argument(
        "--interval",
        type=float,
        default=10.0,
        help="Number of seconds to wait between attempts to get results from Moonstream Query API",
    )
    leaderboard_generator_parser.add_argument(
        "--params",
        type=json.loads,
        required=False,
        help="Parameters to pass to Moonstream Query API. Use together with --leaderboard-id",
    )
    leaderboard_generator_parser.add_argument(
        "--query-api-access-token",
        type=str,
        required=True,
        help="Moonstream Access Token to use for Moonstream Query API requests",
    )
    leaderboard_generator_parser.add_argument(
        "--leaderboard-push-batch-size",
        type=int,
        default=MOONSTREAM_LEADERBOARD_GENERATOR_BATCH_SIZE,
        help="Number of scores to push to leaderboard API at once",
    )
    leaderboard_generator_parser.add_argument(
        "--leaderboard-push-timeout-seconds",
        type=int,
        default=MOONSTREAM_LEADERBOARD_GENERATOR_PUSH_TIMEOUT_SECONDS,
        help="Timeout for leaderboard API requests",
    )

    leaderboard_generator_parser.set_defaults(func=handle_leaderboards)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
