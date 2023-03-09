import argparse
import codecs
import csv
import json
import logging
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

import boto3  # type: ignore
import requests
from moonstreamdb.models import EthereumLabel
from sqlalchemy.orm import Session

from .db import yield_db_session_ctx
from .settings import MOONSTREAM_ETHERSCAN_TOKEN
from .version import MOONCRAWL_VERSION

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if MOONSTREAM_ETHERSCAN_TOKEN is None:
    raise Exception("MOONSTREAM_ETHERSCAN_TOKEN environment variable must be set")


BASE_API_URL = "https://api.etherscan.io/api?module=contract&action=getsourcecode"

ETHERSCAN_SMARTCONTRACTS_LABEL_NAME = "etherscan_smartcontract"

bucket = os.environ.get("MOONSTREAM_S3_SMARTCONTRACTS_BUCKET")
if bucket is None:
    raise ValueError("MOONSTREAM_S3_SMARTCONTRACTS_BUCKET must be set")


@dataclass
class VerifiedSmartContract:
    name: str
    address: str
    tx_hash: str


def push_to_bucket(contract_data: Dict[str, Any], contract_file: str):
    result_bytes = json.dumps(contract_data).encode("utf-8")
    result_key = contract_file

    s3 = boto3.client("s3")
    s3.put_object(
        Body=result_bytes,
        Bucket=bucket,
        Key=result_key,
        ContentType="application/json",
        Metadata={"source": "etherscan", "crawler_version": MOONCRAWL_VERSION},
    )


def crawl_step(db_session: Session, contract: VerifiedSmartContract, crawl_url: str):
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
    result = page["result"][0]
    contract_info = {
        "data": result,
        "crawl_version": MOONCRAWL_VERSION,
        "crawled_at": f"{datetime.now()}",
    }
    object_key = f"/etherscan/v1/{contract.address}.json"
    push_to_bucket(contract_info, object_key)

    try:
        eth_label = EthereumLabel(
            label=ETHERSCAN_SMARTCONTRACTS_LABEL_NAME,
            address=contract.address,
            label_data={
                "object_uri": f"s3://{bucket}/{object_key}",
                "name": contract.name,
                "tx_hash": contract.tx_hash,
            },
        )
        try:
            db_session.add(eth_label)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e
    except Exception as e:
        logger.error(
            f"Failed to add addresss label ${contract.address} to database\n{str(e)}"
        )


def crawl(
    db_session: Session,
    smart_contracts: List[VerifiedSmartContract],
    interval: float,
    start_step=0,
):
    for i in range(start_step, len(smart_contracts)):
        contract = smart_contracts[i]
        print(f"Crawling {i}/{len(smart_contracts)} : {contract.address}")
        query_url = (
            BASE_API_URL
            + f"&address={contract.address}&apikey={MOONSTREAM_ETHERSCAN_TOKEN}"
        )
        crawl_step(db_session, contract, query_url)
        time.sleep(interval)


def load_smart_contracts() -> List[VerifiedSmartContract]:
    smart_contracts: List[VerifiedSmartContract] = []
    s3 = boto3.client("s3")
    data = s3.get_object(Bucket=bucket, Key="util/verified-contractaddress.csv")
    for row in csv.DictReader(codecs.getreader("utf-8")(data["Body"])):
        smart_contracts.append(
            VerifiedSmartContract(
                tx_hash=row["Txhash"],
                address=row["ContractAddress"],
                name=row["ContractName"],
            )
        )
    return smart_contracts


def main():
    parser = argparse.ArgumentParser(
        description="Crawls smart contract sources from etherscan.io"
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=0.2,
        help="Number of seconds to wait between requests to the etherscan.io (default: 0.2)",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Number of smart contract to skip for crawling from smart contracts .csv file",
    )

    args = parser.parse_args()
    with yield_db_session_ctx() as db_session:
        crawl(
            db_session,
            load_smart_contracts(),
            interval=args.interval,
            start_step=args.offset,
        )


if __name__ == "__main__":
    main()
