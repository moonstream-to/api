import datetime
import json
import logging
import os
import time
from typing import Any, Dict, List, Optional

import requests  # type: ignore

from ..settings import (
    MOONSTREAM_API_URL,
    MOONSTREAM_ENGINE_URL,
    MOONSTREAM_LEADERBOARD_GENERATOR_BATCH_SIZE,
    MOONSTREAM_LEADERBOARD_GENERATOR_PUSH_TIMEOUT_SECONDS,
)

logging.basicConfig()
logger = logging.getLogger(__name__)


def get_results_for_moonstream_query(
    moonstream_access_token: str,
    query_name: str,
    params: Dict[str, Any],
    blockchain: Optional[str] = None,
    api_url: str = MOONSTREAM_API_URL,
    max_retries: int = 100,
    interval: float = 30.0,
    query_api_retries: int = 3,
) -> Optional[Dict[str, Any]]:
    """

    Run update of query data and waiting update of query result on S3.
    TODO: Move to moonstream-client.

    :param moonstream_access_token: Moonstream access token.

    :param query_name: Name of the query to run.

    :param params: Parameters to pass to the query.

    :param api_url: URL of the Moonstream API.

    :param max_retries: Maximum number of times to retry getting results from the Moonstream Query API.

    :param interval: Number of seconds to wait between attempts to get results from the Moonstream Query API.

    :return: Results of the query.

    """

    result: Optional[Dict[str, Any]] = None

    api_url = api_url.rstrip("/")
    request_url = f"{api_url}/queries/{query_name}/update_data"
    headers = {
        "Authorization": f"Bearer {moonstream_access_token}",
        "Content-Type": "application/json",
    }
    # Assume our clock is not drifting too much from AWS clocks.
    if_modified_since_datetime = datetime.datetime.utcnow()
    if_modified_since = if_modified_since_datetime.strftime("%a, %d %b %Y %H:%M:%S GMT")

    request_body: Dict[str, Any] = {"params": params}

    if blockchain is not None:
        request_body["blockchain"] = blockchain

    success = False
    attempts = 0

    while not success and attempts < query_api_retries:
        response = requests.post(
            request_url, json=request_body, headers=headers, timeout=10
        )
        attempts += 1
        response.raise_for_status()
        response_body = response.json()
        data_url = response_body["url"]

        keep_going = True
        num_retries = 0

        logging.debug(f"If-Modified-Since: {if_modified_since}")
        while keep_going:
            time.sleep(interval)
            num_retries += 1
            try:
                data_response = requests.get(
                    data_url,
                    headers={"If-Modified-Since": if_modified_since},
                    timeout=10,
                )
            except:
                logger.error(f"Failed to get data from {data_url}")
                continue
            logger.debug(f"Status code: {data_response.status_code}")
            logger.debug(f"Last-Modified: {data_response.headers['Last-Modified']}")
            if data_response.status_code == 200:
                result = data_response.json()
                keep_going = False
                success = True
            if keep_going and max_retries > 0:
                keep_going = num_retries <= max_retries

    return result


def list_queries(
    moonstream_access_token: str,
    api_url: str = MOONSTREAM_API_URL,
) -> List[Dict[str, Any]]:
    """
    Return a list of queries available in account.
    """

    api_url = api_url.rstrip("/")
    request_url = f"{api_url}/queries/list"
    headers = {
        "Authorization": f"Bearer {moonstream_access_token}",
        "Content-Type": "application/json",
    }

    response = requests.get(request_url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()


def get_query_by_name(
    moonstream_access_token: str,
    query_name: str,
    api_url: str = MOONSTREAM_API_URL,
) -> Dict[str, Any]:
    """
    Return a query by name.
    """

    api_url = api_url.rstrip("/")
    request_url = f"{api_url}/queries/{query_name}/query"
    headers = {
        "Authorization": f"Bearer {moonstream_access_token}",
        "Content-Type": "application/json",
    }

    response = requests.get(request_url, headers=headers, timeout=10)

    response.raise_for_status()
    return response.json()


def get_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get data: HTTP {response.status_code}")


def send_data_to_endpoint(chunks, endpoint_url, headers, timeout=10):
    for index, chunk in enumerate(chunks):
        try:
            logger.info(f"Pushing chunk {index} to leaderboard API")
            response = requests.put(
                endpoint_url, headers=headers, json=chunk, timeout=timeout
            )

            response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            logger.error(
                f"Could not push results to leaderboard API: {http_error.response.text} with status code {http_error.response.status_code}"
            )
            raise http_error


def leaderboard_push_batch(
    leaderboard_id: str,
    leaderboard_config: Dict[str, Any],
    data: List[Dict[str, Any]],
    headers: Dict[str, str],
    batch_size: int = MOONSTREAM_LEADERBOARD_GENERATOR_BATCH_SIZE,
    timeout: int = 10,
) -> None:
    """
    Push leaderboard data to the leaderboard API in batches.
    """

    ## first step create leaderboard version

    leaderboard_version_api_url = (
        f"{MOONSTREAM_ENGINE_URL}/leaderboard/{leaderboard_id}/versions"
    )

    json_data = {
        "publish": False,
    }

    leaderboard_api_response = requests.post(
        leaderboard_version_api_url, json=json_data, headers=headers, timeout=10
    )

    try:
        leaderboard_api_response.raise_for_status()
    except requests.exceptions.HTTPError as http_error:
        logger.error(
            f"Could not create leaderboard version: {http_error.response.text} with status code {http_error.response.status_code}"
        )
        return

    leaderboard_version_id = leaderboard_api_response.json()["version"]

    ## second step push data to leaderboard version

    leaderboard_version_push_api_url = f"{MOONSTREAM_ENGINE_URL}/leaderboard/{leaderboard_id}/versions/{leaderboard_version_id}/scores?normalize_addresses={leaderboard_config['normalize_addresses']}&overwrite=false"

    chunks = [data[x : x + batch_size] for x in range(0, len(data), batch_size)]

    send_data_to_endpoint(
        chunks, leaderboard_version_push_api_url, headers, timeout=timeout
    )

    ## third step publish leaderboard version

    leaderboard_version_publish_api_url = f"{MOONSTREAM_ENGINE_URL}/leaderboard/{leaderboard_id}/versions/{leaderboard_version_id}"

    json_data = {
        "publish": True,
    }

    try:
        leaderboard_api_response = requests.put(
            leaderboard_version_publish_api_url,
            json=json_data,
            headers=headers,
            timeout=10,
        )

        leaderboard_api_response.raise_for_status()
    except requests.exceptions.HTTPError as http_error:
        logger.error(
            f"Could not publish leaderboard version: {http_error.response.text} with status code {http_error.response.status_code}"
        )
        return

    ## delete leaderboard version -1

    try:
        leaderboard_version_delete_api_url = f"{MOONSTREAM_ENGINE_URL}/leaderboard/{leaderboard_id}/versions/{leaderboard_version_id - 1}"

        leaderboard_api_response = requests.delete(
            leaderboard_version_delete_api_url,
            headers=headers,
            timeout=timeout,
        )

        leaderboard_api_response.raise_for_status()
    except requests.exceptions.HTTPError as http_error:
        logger.error(
            f"Could not delete leaderboard version: {http_error.response.text} with status code {http_error.response.status_code}"
        )
        return
