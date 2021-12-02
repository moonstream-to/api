import logging

import boto3  # type: ignore
from web3 import Web3

from .settings import (
    MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI,
    MOONSTREAM_INTERNAL_HOSTED_ZONE_ID,
    MOONSTREAM_NODE_ETHEREUM_IPC_PORT,
)

logger = logging.getLogger(__name__)


def fetch_web3_provider_ip():
    r53 = boto3.client("route53")
    r53_response = r53.list_resource_record_sets(
        HostedZoneId=MOONSTREAM_INTERNAL_HOSTED_ZONE_ID,
        StartRecordName=f"{MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI}.",
        StartRecordType="A",
    )
    try:
        r53_records = r53_response["ResourceRecordSets"]
        if r53_records[0]["Name"] != f"{MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI}.":
            return None

        record_value = r53_records[0]["ResourceRecords"][0]["Value"]
    except Exception as e:
        logger.error(e)
        return None

    return record_value


if not MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI.startswith("http"):
    web3_provider_ip = fetch_web3_provider_ip()
    if web3_provider_ip is None:
        raise ValueError("Unable to extract web3 provider IP")
else:
    web3_provider_ip = MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI

moonstream_web3_provider = Web3(
    Web3.HTTPProvider(f"http://{web3_provider_ip}:{MOONSTREAM_NODE_ETHEREUM_IPC_PORT}")
)


def yield_web3_provider() -> Web3:
    return moonstream_web3_provider
