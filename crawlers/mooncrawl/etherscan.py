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
from dataclasses import dataclass
from sqlalchemy.sql.expression import label, text
from .version import MOONCRAWL_VERSION
from moonstreamdb.models import EthereumAddress, EthereumLabel
import requests

from .settings import MOONSTREAM_ETHERSCAN_TOKEN

if MOONSTREAM_ETHERSCAN_TOKEN is None:
    raise Exception("MOONSTREAM_ETHERSCAN_TOKEN environment variable must be set")


BASE_API_URL = "https://api.etherscan.io/api?module=contract&action=getsourcecode"

ETHERSCAN_SMARTCONTRACTS_LABEL_NAME = "etherscan_smartcontract"

bucket = os.environ.get("AWS_S3_SMARTCONTRACT_BUCKET")
if bucket is None:
    raise ValueError("AWS_S3_SMARTCONTRACT_BUCKET must be set")


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


def get_address_id(db_session: Session, contract_address: str) -> int:
    """
    Searches for given address in EthereumAddress table,
    If doesn't find one, creates new.
    Returns id of address
    """
    query = db_session.query(EthereumAddress.id).filter(
        EthereumAddress.address == contract_address
    )
    id = query.one_or_none()
    if id is not None:
        return id[0]

    latest_address_id = (
        db_session.query(EthereumAddress.id).order_by(text("id desc")).limit(1).one()
    )[0]

    id = latest_address_id + 1
    smart_contract = EthereumAddress(
        id=id,
        address=contract_address,
    )
    try:
        db_session.add(smart_contract)
        db_session.commit()
    except:
        db_session.rollback()
    return id


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

    eth_address_id = get_address_id(db_session, contract.address)

    eth_label = EthereumLabel(
        label=ETHERSCAN_SMARTCONTRACTS_LABEL_NAME,
        address_id=eth_address_id,
        label_data={
            "object_uri": f"s3://{bucket}/{object_key}",
            "name": contract.name,
            "tx_hash": contract.tx_hash,
        },
    )
    try:
        db_session.add(eth_label)
        db_session.commit()
    except:
        db_session.rollback()


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
