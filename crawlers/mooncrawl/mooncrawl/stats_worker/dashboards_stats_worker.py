import json
import argparse
from enum import Enum
import hashlib
from datetime import timedelta, datetime
import logging
from typing import Any, Dict, List
import os
import time
import pprint


import boto3
from bugout import data  # type: ignore
from moonstreamdb.db import yield_db_session_ctx
from moonstreamdb.models import EthereumLabel, EthereumTransaction, EthereumBlock
from bugout.app import Bugout
from bugout.data import BugoutResources

from sqlalchemy.orm import Session
from sqlalchemy import func, text, and_, Date, cast
from datetime import date


from web3 import Web3, IPCProvider, HTTPProvider
from web3.types import BlockData


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Bugout


lable_filters = {"Transfer": "nft_transfer"}

BUGOUT_BROOD_URL = os.environ.get("BUGOUT_BROOD_URL", "https://auth.bugout.dev")
BUGOUT_SPIRE_URL = os.environ.get("BUGOUT_SPIRE_URL", "https://spire.bugout.dev")
DATA_BUCKET = ""


class TimeScale(Enum):
    year = "year"
    month = "month"
    week = "week"
    day = "day"


timescales_params: Dict[str, Dict[str, str]] = {
    "year": {"timestep": "1 day", "timeformat": "YYYY-MM-DD"},
    "month": {"timestep": "1 day", "timeformat": "YYYY-MM-DD"},
    "week": {"timestep": "1 day", "timeformat": "YYYY-MM-DD"},
    "day": {"timestep": "1 hours", "timeformat": "YYYY-MM-DD HH24"},
}

timescales_delta: Dict[str, Dict[str, timedelta]] = {
    "year": {"timedelta": timedelta(days=365)},
    "month": {"timedelta": timedelta(days=27)},
    "week": {"timedelta": timedelta(days=6)},
    "day": {"timedelta": timedelta(hours=24)},
}


bc = Bugout(brood_api_url=BUGOUT_BROOD_URL, spire_api_url=BUGOUT_SPIRE_URL)


BUGOUT_RESOURCE_TYPE_SUBSCRIPTION = "subscription"


MOONSTREAM_ADMIN_ACCESS_TOKEN = os.getenv("MOONSTREAM_ADMIN_ACCESS_TOKEN")


AWS_S3_SMARTCONTRACTS_ABI_PREFIX = os.getenv("AWS_S3_SMARTCONTRACTS_ABI_PREFIX")


def push_statistics(
    statistics_data: Dict[str, Any],
    subscription: Any,
    timescale: str,
    bucket: str,
    hash: str,
) -> None:

    # statistics_prefix = os.environ.get(
    #     "AWS_S3_DRONES_BUCKET_STATISTICS_PREFIX", ""
    # ).rstrip("/")
    # if bucket is None:
    #     logger.warning(
    #         "AWS_STATS_S3_BUCKET environment variable not defined, skipping storage of search results"
    #     )
    #     return

    result_bytes = json.dumps(statistics_data).encode("utf-8")
    result_key = f'contracts_data/{subscription.resource_data["address"]}/{hash}/v1/{timescale}.json'

    s3 = boto3.client("s3")
    s3.put_object(
        Body=result_bytes,
        Bucket=bucket,
        Key=result_key,
        ContentType="application/json",
        Metadata={"drone": "statistics"},
    )

    # TODO (Andrey) Understand why logger wont show messages some time and put them beside print
    # without print here exeption wont show.
    print(f"Statistics push to bucket: s3://{bucket}/{result_key}")


# import moonworm


def add_events_to_database(db_session: Session, contract: str, events: List[Any]):
    """
    Apply events of contract to dataabase

    """

    for event in events:
        try:
            eth_label = EthereumLabel(
                label="mooonworm",
                address=contract,
                label_data={
                    "type": "event",
                    "contract": contract,
                    "tx_hash": event,
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
                f"Failed to add addresss label ${contract} to database\n{str(e)}"
            )


def read_events(contract: str, abi: Dict[str, Any]):
    """
    Read events for provided abi
    """
    # moonworm


def read_functions_calls(contract: str, abi: Dict[str, Any]):
    """
    Read functions for provided abi
    """

    # token of admin

    pass


def generate_data(
    session: Session, address: str, timescale: str, functions: List[str], start: Any
):

    # create empty time series

    time_step = timescales_params[timescale]["timestep"]

    time_format = timescales_params[timescale]["timeformat"]

    # if end is None:
    end = datetime.utcnow()

    time_series_subquery = session.query(
        func.generate_series(
            start,
            end,
            time_step,
        ).label("timeseries_points")
    )

    # print(time_series_subquery.all())

    time_series_subquery = time_series_subquery.subquery(name="time_series_subquery")

    # get distinct tags labels in that range

    label_requested = (
        session.query(EthereumLabel.label.label("label"))
        .filter(EthereumLabel.address == address)
        .filter(EthereumLabel.label.in_(functions))
        .distinct()
    )

    if start is not None:
        label_requested = label_requested.filter(
            cast(EthereumLabel.block_timestamp, Date) > start
        )
    if end is not None:
        label_requested = label_requested.filter(
            cast(EthereumLabel.block_timestamp, Date) < end
        )
    # print(functions)

    # print(label_requested)

    label_requested = label_requested.subquery(name="label_requested")

    # empty timeseries with tags
    empty_time_series_subquery = session.query(
        func.to_char(time_series_subquery.c.timeseries_points, time_format).label(
            "timeseries_points"
        ),
        label_requested.c.label.label("label"),
    )

    print(empty_time_series_subquery)

    print(empty_time_series_subquery.all())

    empty_time_series_subquery = empty_time_series_subquery.subquery(
        name="empty_time_series_subquery"
    )

    # tags count
    label_counts = (
        session.query(
            func.to_char(EthereumLabel.created_at, time_format).label(
                "timeseries_points"
            ),
            func.count(EthereumLabel.id).label("count"),
            EthereumLabel.label.label("label"),
        )
        .filter(EthereumLabel.label.in_(functions))
        .filter(EthereumLabel.address == address)
    )

    if start is not None:
        label_counts = label_counts.filter(EthereumLabel.created_at > start)
    if end is not None:
        label_counts = label_counts.filter(EthereumLabel.created_at < end)

    label_counts_subquery = (
        label_counts.group_by(
            text("timeseries_points"),
            EthereumLabel.label,
        )
        .order_by(text("timeseries_points desc"))
        .subquery(name="label_counts")
    )

    # Join empty tags_time_series with tags count eg apply tags counts to time series.
    labels_time_series = (
        session.query(
            empty_time_series_subquery.c.timeseries_points.label("timeseries_points"),
            empty_time_series_subquery.c.label.label("label"),
            func.coalesce(label_counts_subquery.c.count.label("count"), 0),
        )
        .join(
            label_counts_subquery,
            and_(
                empty_time_series_subquery.c.label == label_counts_subquery.c.label,
                empty_time_series_subquery.c.timeseries_points
                == label_counts_subquery.c.timeseries_points,
            ),
            isouter=True,
        )
        .order_by(text("timeseries_points DESC"))
    )

    response_labels: Dict[Any, Any] = {}

    for created_date, label, count in labels_time_series:

        if not response_labels.get(label):
            response_labels[label] = []
            if time_format == "YYYY-MM-DD HH24":
                created_date, hour = created_date.split(" ")
                response_labels[label].append(
                    {"date": created_date, "hour": hour, "count": count}
                )
            else:
                response_labels[label].append({"date": created_date, "count": count})
        else:
            if time_format == "YYYY-MM-DD HH24":
                created_date, hour = created_date.split(" ")
                response_labels[label].append(
                    {"date": created_date, "hour": hour, "count": count}
                )
            else:
                response_labels[label].append({"date": created_date, "count": count})

    return response_labels


def month_stats(type, abi):
    pass


def week_stats(type, abi):
    pass


def days_stats(type, abi):
    pass


def crawlers_start(db_session):
    token = os.getenv("MOONSTREAM_ADMIN_ACCESS_TOKEN")

    # read all subscriptions
    required_subscriptions: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION, "abi": "true"},
        timeout=10,
    )
    print(f"Subscriptions for processing: {len(required_subscriptions.resources)}")

    s3_client = boto3.client("s3")

    for subscription in required_subscriptions.resources:

        bucket = subscription.resource_data["bucket"]
        key = subscription.resource_data["s3_path"]
        address = subscription.resource_data["address"]

        print(f"Expected bucket: s3://{bucket}/{key}")

        abi = s3_client.get_object(
            Bucket=bucket,
            Key=key,
        )
        abi_json = json.loads(abi["Body"].read())

        # print(abi_json)

        abi_string = json.dumps(abi_json, sort_keys=True, indent=2)

        hash = hashlib.md5(abi_string.encode("utf-8")).hexdigest()

        s3_data_object = {}

        abi_functions = [item for item in abi_json if item["type"] == "function"]
        abi_events = [item for item in abi_json if item["type"] == "event"]

        for timescale in [timescale.value for timescale in TimeScale]:

            start_date = datetime.utcnow() - timescales_delta[timescale]["timedelta"]

            print(f"Timescale: {timescale}")

            functions_metrics = {}

            abi_functions_names = [item["name"] for item in abi_functions]

            data = generate_data(
                db_session, address, timescale, abi_functions_names, start=start_date
            )
            print(data)

            print()

            functions_metrics[timescale] = data

            s3_data_object["functions"] = functions_metrics
            # generate data

            events_metrics = {}

            abi_events_names = [
                item["name"]
                if item["name"] not in lable_filters
                else lable_filters[item["name"]]
                for item in abi_events
            ]

            data = generate_data(
                db_session,
                address,
                timescale,
                abi_events_names,
                start=start_date,
            )

            events_metrics[timescale] = data

            s3_data_object["events"] = events_metrics

            push_statistics(
                statistics_data=s3_data_object,
                subscription=subscription,
                timescale=timescale,
                bucket=bucket,
                hash=hash,
            )

    time.sleep(10)


def main():

    with yield_db_session_ctx() as db_session:
        crawlers_start(db_session)


if __name__ == "__main__":
    main()
