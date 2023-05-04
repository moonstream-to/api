import argparse
import sys
import time
from typing import Optional, Union

import requests
from moonstreamdb.models import ESDEventSignature, ESDFunctionSignature
from sqlalchemy.orm import Session

from .db import yield_db_session_ctx

CRAWL_URLS = {
    "functions": "https://www.4byte.directory/api/v1/signatures/",
    "events": "https://www.4byte.directory/api/v1/event-signatures/",
}

DB_MODELS = {
    "functions": ESDFunctionSignature,
    "events": ESDEventSignature,
}


def crawl_step(
    db_session: Session,
    crawl_url: str,
    db_model: Union[ESDEventSignature, ESDFunctionSignature],
) -> Optional[str]:
    attempt = 0
    current_interval = 2
    success = False

    response: Optional[requests.Response] = None
    while (not success) and attempt < 3:
        attempt += 1
        try:
            response = requests.get(crawl_url)
            response.raise_for_status()
            success = True
        except:
            current_interval *= 2
            time.sleep(current_interval)

    if response is None:
        print(f"Could not process URL: {crawl_url}", file=sys.stderr)
        return None

    page = response.json()
    results = page.get("results", [])

    rows = [
        db_model(
            id=row.get("id"),
            text_signature=row.get("text_signature"),
            hex_signature=row.get("hex_signature"),
            created_at=row.get("created_at"),
        )
        for row in results
    ]
    db_session.bulk_save_objects(rows)
    db_session.commit()

    return page.get("next")


def crawl(crawl_type: str, interval: float) -> None:
    crawl_url: Optional[str] = CRAWL_URLS[crawl_type]
    db_model = DB_MODELS[crawl_type]
    with yield_db_session_ctx() as db_session:
        while crawl_url is not None:
            print(f"Crawling: {crawl_url}")
            crawl_url = crawl_step(db_session, crawl_url, db_model)
            time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(
        description="Crawls function and event signatures from the Ethereum Signature Database (https://www.4byte.directory/)"
    )
    parser.add_argument(
        "crawl_type",
        choices=CRAWL_URLS,
        help="Specifies whether to crawl function signatures or event signatures",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.1,
        help="Number of seconds to wait between requests to the Ethereum Signature Database API",
    )
    args = parser.parse_args()

    crawl(args.crawl_type, args.interval)


if __name__ == "__main__":
    main()
