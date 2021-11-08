import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests


def publish_json(
    crawl_type: str,
    humbug_token: str,
    title: str,
    content: Dict[str, Any],
    tags: Optional[List[str]] = None,
    wait: bool = True,
    created_at: Optional[str] = None,
) -> None:
    spire_api_url = os.environ.get(
        "MOONSTREAM_SPIRE_API_URL", "https://spire.bugout.dev"
    ).rstrip("/")
    report_url = f"{spire_api_url}/humbug/reports"

    if tags is None:
        tags = []

    tags.append(f"crawl_type:{crawl_type}")

    headers = {
        "Authorization": f"Bearer {humbug_token}",
    }
    request_body = {
        "title": title,
        "content": json.dumps(content),
        "tags": tags,
    }
    if created_at is not None:
        request_body["created_at"] = created_at

    query_parameters = {"sync": wait}

    response = requests.post(
        report_url, headers=headers, json=request_body, params=query_parameters
    )

    response.raise_for_status()
