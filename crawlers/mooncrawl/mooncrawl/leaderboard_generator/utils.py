import datetime
import json
import logging
import os
import time
from typing import Any, Dict, Optional


import requests  # type: ignore


logging.basicConfig()
logger = logging.getLogger(__name__)


def get_results_for_moonstream_query(
    moonstream_access_token: str,
    query_name: str,
    params: Dict[str, Any],
    api_url: str = "https://api.moonstream.to",
    max_retries: int = 100,
    interval: float = 30.0,
) -> Optional[Dict[str, Any]]:
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

    request_body = {"params": params}

    success = False
    attempts = 0

    while not success and attempts < max_retries:
        attempts += 1
        response = requests.post(
            request_url, json=request_body, headers=headers, timeout=10
        )
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
