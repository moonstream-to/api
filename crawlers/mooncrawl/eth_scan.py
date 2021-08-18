import argparse
import boto3
import csv
import codecs
import json
import os
from sqlalchemy.orm import Session
from moonstreamdb.db import yield_db_session_ctx
import sys
import time
from datetime import datetime
from typing import Any, List, Optional, Tuple, Dict

from sqlalchemy.sql.expression import label
from .version import MOONCRAWL_VERSION
from moonstreamdb.models import EthereumAddress, EthereumLabel
import requests


ETH_SCAN_TOKEN = os.environ.get("ETH_SCAN_TOKEN")
if ETH_SCAN_TOKEN is None:
    raise ValueError("ETH_SCAN_TOKEN environment variable must be set")

BASE_API_URL = "https://api.etherscan.io/api?module=contract&action=getsourcecode"

ETHERSCAN_SMARTCONTRACTS_LABEL_NAME = "etherscan_smartcontract"

bucket = os.environ.get("AWS_S3_SMARTCONTRACT_BUCKET")
if bucket is None:
    raise ValueError("AWS_S3_SMARTCONTRACT_BUCKET must be set")


def push_to_bucket(contract_data: Dict[str, Any], contract_file: str):
    result_bytes = json.dumps(contract_data).encode("utf-8")
    result_key = contract_file

    s3 = boto3.client("s3")
    s3.put_object(
        Body=result_bytes,
        Bucket=bucket,
        Key=result_key,
        ContentType="application/json",
        Metadata={"source": "etherscan", "crawler_version": ""},
    )


def crawl_step(db_session: Session, contract_address: str, crawl_url: str):
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
    object_key = f"/v1/etherscan/{contract_address}.json"
    push_to_bucket(contract_info, object_key)

    # TODO
    eth_token_id = 0
    # make it const
    eth_label = EthereumLabel(
        label=ETHERSCAN_SMARTCONTRACTS_LABEL_NAME,
        address_id=eth_token_id,
        labeldata={"key": object_key},
    )


def crawl(
    smart_contracts: List[Tuple[str, str]],
    interval: float,
    start_step=0,
):
    with yield_db_session_ctx() as db_session:
        for i in range(start_step, len(smart_contracts)):
            _, address = smart_contracts[i]
            print(address)
            querry_url = BASE_API_URL + f"&address={address}&apikey={ETH_SCAN_TOKEN}"
            crawl_step(db_session, address, querry_url)
            time.sleep(interval)
        pass


def load_smart_contracts() -> List[Tuple[str, str]]:
    smart_contracts: List[Tuple[str, str]] = []
    s3 = boto3.client("s3")
    data = s3.get_object(Bucket=bucket, Key="util/verified-contractaddress.csv")
    for row in csv.DictReader(codecs.getreader("utf-8")(data["Body"])):
        smart_contracts.append((row["Txhash"], row["ContractAddress"]))
    return smart_contracts


def main():
    parser = argparse.ArgumentParser(
        description="Crawls smart contract sources from ethersan.io"
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
    crawl(
        load_smart_contracts(),
        interval=args.interval,
        start_step=args.offset,
    )


if __name__ == "__main__":
    main()
