import argparse
from datetime import timedelta, datetime
from enum import Enum
import hashlib
import logging
import json
import os
from typing import Any, Dict, List, Callable
import time

import boto3
from moonstreamdb.db import yield_db_session_ctx
from moonstreamdb.models import EthereumLabel, EthereumTransaction, EthereumBlock
from bugout.app import Bugout
from bugout.data import BugoutResources

from sqlalchemy.orm import Session, Query
from sqlalchemy import func, text, and_, Date, Column


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

BUGOUT_RESOURCE_TYPE_DASHBOARD = "dashboards"

MOONSTREAM_ADMIN_ACCESS_TOKEN = os.getenv("MOONSTREAM_ADMIN_ACCESS_TOKEN")


AWS_S3_SMARTCONTRACTS_ABI_PREFIX = os.getenv("AWS_S3_SMARTCONTRACTS_ABI_PREFIX")


def push_statistics(
    statistics_data: Dict[str, Any],
    subscription: Any,
    timescale: str,
    bucket: str,
    hash: str,
) -> None:

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

    print(f"Statistics push to bucket: s3://{bucket}/{result_key}")


def generate_metrics(
    db_session: Session, address: str, timescale: str, metrics: List[str], start: Any
):
    """

    Generage metrics
    """

    start = start
    end = datetime.utcnow()

    start_timestamp = int(start.timestamp())
    end_timestamp = int(end.timestamp())

    results: Dict[str, Any] = {}

    time_step = timescales_params[timescale]["timestep"]

    time_format = timescales_params[timescale]["timeformat"]

    def make_query(
        db_session: Session,
        identifying_column: Column,
        statistic_column: Column,
    ) -> Query:

        unformated_time_series_subquery = db_session.query(
            func.generate_series(
                start,
                end,
                time_step,
            ).label("timeseries_points")
        ).subquery(name="unformated_time_series_subquery")

        time_series_formated = db_session.query(
            func.to_char(
                unformated_time_series_subquery.c.timeseries_points, time_format
            ).label("timeseries_points")
        )

        time_series_formated_subquery = time_series_formated.subquery(
            name="time_series_subquery"
        )

        metric_count_subquery = (
            db_session.query(
                func.count(statistic_column).label("count"),
                func.to_char(
                    func.to_timestamp(EthereumBlock.timestamp).cast(Date), time_format
                ).label("timeseries_points"),
            )
            .join(
                EthereumBlock,
                EthereumTransaction.block_number == EthereumBlock.block_number,
            )
            .filter(identifying_column == address)
            .filter(EthereumBlock.timestamp >= start_timestamp)
            .filter(EthereumBlock.timestamp <= end_timestamp)
            .group_by(text("timeseries_points"))
        ).subquery(name="metric_counts")

        metrics_time_series = (
            db_session.query(
                time_series_formated_subquery.c.timeseries_points.label(
                    "timeseries_points"
                ),
                func.coalesce(metric_count_subquery.c.count.label("count"), 0),
            )
            .join(
                metric_count_subquery,
                time_series_formated_subquery.c.timeseries_points
                == metric_count_subquery.c.timeseries_points,
                isouter=True,
            )
            .order_by(text("timeseries_points DESC"))
        )

        response_metric: List[Any] = []

        for created_date, count in metrics_time_series:

            if time_format == "YYYY-MM-DD HH24":
                created_date, hour = created_date.split(" ")
                response_metric.append(
                    {"date": created_date, "hour": hour, "count": count}
                )
            else:
                response_metric.append({"date": created_date, "count": count})

        return response_metric

    try:
        start_time = time.time()

        results["transactions_out"] = make_query(
            db_session,
            EthereumTransaction.from_address,
            EthereumTransaction.hash,
        )

        print("--- transactions_out %s seconds ---" % (time.time() - start_time))

        start_time = time.time()
        results["transactions_in"] = make_query(
            db_session,
            EthereumTransaction.to_address,
            EthereumTransaction.hash,
        )

        print("--- transactions_in %s seconds ---" % (time.time() - start_time))

        start_time = time.time()
        results["value_out"] = make_query(
            db_session,
            EthereumTransaction.from_address,
            EthereumTransaction.value,
        )
        print("--- value_out %s seconds ---" % (time.time() - start_time))

        start_time = time.time()
        results["value_in"] = make_query(
            db_session,
            EthereumTransaction.to_address,
            EthereumTransaction.value,
        )

        print("--- value_in %s seconds ---" % (time.time() - start_time))

    except Exception as err:
        print(err)
        pass

    return results


def generate_data(
    db_session: Session, address: str, timescale: str, functions: List[str], start: Any
):

    # create empty time series

    time_step = timescales_params[timescale]["timestep"]

    time_format = timescales_params[timescale]["timeformat"]

    # if end is None:
    end = datetime.utcnow()

    time_series_subquery = db_session.query(
        func.generate_series(
            start,
            end,
            time_step,
        ).label("timeseries_points")
    )

    print(time_series_subquery.all())

    time_series_subquery = time_series_subquery.subquery(name="time_series_subquery")

    # get distinct tags labels in that range

    label_requested = (
        db_session.query(EthereumLabel.label.label("label"))
        .filter(EthereumLabel.address == address)
        .filter(EthereumLabel.label.in_(functions))
        .distinct()
    )

    if start is not None:
        label_requested = label_requested.filter(
            func.to_timestamp(EthereumLabel.block_timestamp).cast(Date) > start
        )
    if end is not None:
        label_requested = label_requested.filter(
            func.to_timestamp(EthereumLabel.block_timestamp).cast(Date) < end
        )

    label_requested = label_requested.subquery(name="label_requested")

    # empty timeseries with tags
    empty_time_series_subquery = db_session.query(
        func.to_char(time_series_subquery.c.timeseries_points, time_format).label(
            "timeseries_points"
        ),
        label_requested.c.label.label("label"),
    )

    empty_time_series_subquery = empty_time_series_subquery.subquery(
        name="empty_time_series_subquery"
    )

    # tags count
    label_counts = (
        db_session.query(
            func.to_char(
                func.to_timestamp(EthereumLabel.block_timestamp).cast(Date), time_format
            ).label("timeseries_points"),
            func.count(EthereumLabel.id).label("count"),
            EthereumLabel.label.label("label"),
        )
        .filter(EthereumLabel.label.in_(functions))
        .filter(EthereumLabel.address == address)
    )

    if start is not None:
        label_counts = label_counts.filter(
            func.to_timestamp(EthereumLabel.block_timestamp).cast(Date) > start
        )
    if end is not None:
        label_counts = label_counts.filter(
            func.to_timestamp(EthereumLabel.block_timestamp).cast(Date) < end
        )

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
        db_session.query(
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


def crawlers_start(db_session):

    # read all subscriptions
    required_subscriptions: BugoutResources = bc.list_resources(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        params={"type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION, "abi": "true"},
        timeout=10,
    )

    print(f"Subscriptions for processing: {len(required_subscriptions.resources)}")

    s3_client = boto3.client("s3")

    # already proccessd

    already_proccessd = []

    for subscription in required_subscriptions.resources:

        if (
            subscription.resource_data["address"]
            != "0x06012c8cf97BEaD5deAe237070F9587f8E7A266d"
        ):
            continue

        bucket = subscription.resource_data["bucket"]
        key = subscription.resource_data["s3_path"]
        address = subscription.resource_data["address"]

        print(f"Expected bucket: s3://{bucket}/{key}")

        abi = s3_client.get_object(
            Bucket=bucket,
            Key=key,
        )
        abi_json = json.loads(abi["Body"].read())

        abi_string = json.dumps(abi_json, sort_keys=True, indent=2)

        hash = hashlib.md5(abi_string.encode("utf-8")).hexdigest()

        if f"{address}/{hash}" in already_proccessd:
            continue

        s3_data_object = {}

        abi_functions = [item for item in abi_json if item["type"] == "function"]
        abi_events = [item for item in abi_json if item["type"] == "event"]

        for timescale in [timescale.value for timescale in TimeScale]:

            start_date = datetime.utcnow() - timescales_delta[timescale]["timedelta"]

            print(f"Timescale: {timescale}")

            abi_functions_names = [item["name"] for item in abi_functions]

            functions_calls_data = generate_data(
                db_session, address, timescale, abi_functions_names, start=start_date
            )

            s3_data_object["functions"] = functions_calls_data
            # generate data

            abi_events_names = [
                item["name"]
                if item["name"] not in lable_filters
                else lable_filters[item["name"]]
                for item in abi_events
            ]

            events_data = generate_data(
                db_session,
                address,
                timescale,
                abi_events_names,
                start=start_date,
            )

            s3_data_object["events"] = events_data

            s3_data_object["metrics"] = generate_metrics(
                db_session,
                address,
                timescale,
                abi_events_names,
                start=start_date,
            )

            push_statistics(
                statistics_data=s3_data_object,
                subscription=subscription,
                timescale=timescale,
                bucket=bucket,
                hash=hash,
            )
        already_proccessd.append(f"{address}/{hash}")

    time.sleep(10)


def stats_generate_handler(args: argparse.Namespace):

    with yield_db_session_ctx() as db_session:
        crawlers_start(db_session)


def main() -> None:

    parser = argparse.ArgumentParser(description="Command Line Interface")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Dashboard worker commands")

    # Statistics parser
    parser_statistics = subcommands.add_parser(
        "statistics", description="Drone statistics"
    )
    parser_statistics.set_defaults(func=lambda _: parser_statistics.print_help())
    subcommands_statistics = parser_statistics.add_subparsers(
        description="Drone dashboard statistics commands"
    )
    parser_statistics_generate = subcommands_statistics.add_parser(
        "generate", description="Generate statistics"
    )

    parser_statistics_generate.set_defaults(func=stats_generate_handler)


if __name__ == "__main__":
    main()
