"""
Generates dashboard.
"""
import argparse
import hashlib
import json
import logging
from os import name
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List

import boto3  # type: ignore
from bugout.data import BugoutResources
from moonstreamdb.db import yield_db_session_ctx
from sqlalchemy import Column, Date, and_, func, text
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql.operators import in_op

from ..blockchain import (
    get_block_model,
    get_label_model,
    get_transaction_model,
    connect,
)
from ..data import AvailableBlockchainType
from ..settings import (
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX,
    CRAWLER_LABEL,
)
from ..settings import bugout_client as bc

from web3 import Web3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


subscription_id_by_blockchain = {
    "ethereum": "ethereum_blockchain",
    "polygon": "polygon_blockchain",
}

blockchain_by_subscription_id = {
    "ethereum_blockchain": "ethereum",
    "polygon_blockchain": "polygon",
}


class TimeScale(Enum):
    # year = "year"
    month = "month"
    week = "week"
    day = "day"


timescales_params: Dict[str, Dict[str, str]] = {
    "year": {"timestep": "1 day", "timeformat": "YYYY-MM-DD"},
    "month": {"timestep": "1 hours", "timeformat": "YYYY-MM-DD HH24"},
    "week": {"timestep": "1 hours", "timeformat": "YYYY-MM-DD HH24"},
    "day": {"timestep": "1 minutes", "timeformat": "YYYY-MM-DD HH24 MI"},
}

timescales_delta: Dict[str, Dict[str, timedelta]] = {
    "year": {"timedelta": timedelta(days=365)},
    "month": {"timedelta": timedelta(days=27)},
    "week": {"timedelta": timedelta(days=6)},
    "day": {"timedelta": timedelta(hours=24)},
}

BUGOUT_RESOURCE_TYPE_SUBSCRIPTION = "subscription"
BUGOUT_RESOURCE_TYPE_DASHBOARD = "dashboards"


def push_statistics(
    statistics_data: Dict[str, Any],
    subscription: Any,
    timescale: str,
    bucket: str,
    hash: str,
) -> None:

    result_bytes = json.dumps(statistics_data).encode("utf-8")
    result_key = f'{MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX}/{blockchain_by_subscription_id[subscription.resource_data["subscription_type_id"]]}/contracts_data/{subscription.resource_data["address"]}/{hash}/v1/{timescale}.json'

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
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    address: str,
    timescale: str,
    metrics: List[str],
    start: Any,
):
    """
    Generage metrics
    """
    block_model = get_block_model(blockchain_type)
    transaction_model = get_transaction_model(blockchain_type)

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
        aggregate_func: Callable,
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
                aggregate_func(statistic_column).label("count"),
                func.to_char(
                    func.to_timestamp(block_model.timestamp), time_format
                ).label("timeseries_points"),
            )
            .join(
                block_model,
                transaction_model.block_number == block_model.block_number,
            )
            .filter(identifying_column == address)
            .filter(block_model.timestamp >= start_timestamp)
            .filter(block_model.timestamp <= end_timestamp)
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

            if not isinstance(count, int):
                count = int(count)
            response_metric.append({"date": created_date, "count": count})

        return response_metric

    try:
        start_time = time.time()

        results["transactions_out"] = make_query(
            db_session,
            transaction_model.from_address,
            transaction_model.hash,
            func.count,
        )

        print("--- transactions_out %s seconds ---" % (time.time() - start_time))

        start_time = time.time()
        results["transactions_in"] = make_query(
            db_session,
            transaction_model.to_address,
            transaction_model.hash,
            func.count,
        )

        print("--- transactions_in %s seconds ---" % (time.time() - start_time))

        start_time = time.time()
        results["value_out"] = make_query(
            db_session,
            transaction_model.from_address,
            transaction_model.value,
            func.sum,
        )
        print("--- value_out %s seconds ---" % (time.time() - start_time))

        start_time = time.time()
        results["value_in"] = make_query(
            db_session,
            transaction_model.to_address,
            transaction_model.value,
            func.sum,
        )

        print("--- value_in %s seconds ---" % (time.time() - start_time))

    except Exception as err:
        print(err)
        pass

    return results


def generate_data(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    address: str,
    timescale: str,
    functions: List[str],
    start: Any,
    metric_type: str,
):
    label_model = get_label_model(blockchain_type)

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

    time_series_subquery = time_series_subquery.subquery(name="time_series_subquery")

    # get distinct tags labels in that range

    label_requested = (
        db_session.query(label_model.label_data["name"].astext.label("label"))
        .filter(label_model.address == address)
        .filter(label_model.label == CRAWLER_LABEL)
        .filter(
            and_(
                label_model.label_data["type"].astext == metric_type,
                in_op(label_model.label_data["name"].astext, functions),
            )
        )
        .distinct()
    )

    if start is not None:
        label_requested = label_requested.filter(
            func.to_timestamp(label_model.block_timestamp) > start
        )
    if end is not None:
        label_requested = label_requested.filter(
            func.to_timestamp(label_model.block_timestamp) < end
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
                func.to_timestamp(label_model.block_timestamp), time_format
            ).label("timeseries_points"),
            func.count(label_model.id).label("count"),
            label_model.label_data["name"].astext.label("label"),
        )
        .filter(label_model.address == address)
        .filter(label_model.label == CRAWLER_LABEL)
        .filter(
            and_(
                label_model.label_data["type"].astext == metric_type,
                in_op(label_model.label_data["name"].astext, functions),
            )
        )
    )

    if start is not None:
        label_counts = label_counts.filter(
            func.to_timestamp(label_model.block_timestamp) > start
        )
    if end is not None:
        label_counts = label_counts.filter(
            func.to_timestamp(label_model.block_timestamp) < end
        )

    label_counts_subquery = (
        label_counts.group_by(
            text("timeseries_points"),
            label_model.label_data["name"].astext,
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

        response_labels[label].append({"date": created_date, "count": count})

    return response_labels


def cast_to_python_type(evm_type: str) -> Callable:
    if evm_type.startswith(("uint", "int")):
        return int
    elif evm_type.startswith("bytes"):
        return bytes
    elif evm_type == "string":
        return str
    elif evm_type == "address":
        return Web3.toChecksumAddress
    elif evm_type == "bool":
        return bool
    else:
        raise ValueError(f"Cannot convert to python type {evm_type}")


def get_unique_address(
    db_session: Session, blockchain_type: AvailableBlockchainType, address: str
):
    label_model = get_label_model(blockchain_type)

    return (
        db_session.query(label_model.label_data["args"]["to"])
        .filter(label_model.address == address)
        .filter(label_model.label == CRAWLER_LABEL)
        .filter(label_model.label_data["type"].astext == "event")
        .filter(label_model.label_data["name"].astext == "Transfer")
        .distinct()
        .count()
    )


def get_count(
    name: str,
    type: str,
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    address: str,
):
    """
    Return count of event from database.
    """
    label_model = get_label_model(blockchain_type)

    return (
        db_session.query(label_model)
        .filter(label_model.address == address)
        .filter(label_model.label == CRAWLER_LABEL)
        .filter(label_model.label_data["type"].astext == type)
        .filter(label_model.label_data["name"].astext == name)
        .count()
    )


def stats_generate_handler(args: argparse.Namespace):
    """
    Start crawler with generate.
    """
    blockchain_type = AvailableBlockchainType(args.blockchain)

    with yield_db_session_ctx() as db_session:
        # read all subscriptions
        required_subscriptions: BugoutResources = bc.list_resources(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            params={
                "type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION,
                "abi": "true",
                "subscription_type_id": subscription_id_by_blockchain[args.blockchain],
            },
            timeout=10,
        )

        print(f"Subscriptions for processing: {len(required_subscriptions.resources)}")

        s3_client = boto3.client("s3")

        # Already processed
        already_processed = []

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

            abi_string = json.dumps(abi_json, sort_keys=True, indent=2)

            hash = hashlib.md5(abi_string.encode("utf-8")).hexdigest()

            if f"{address}/{hash}" in already_processed:
                continue

            s3_data_object = {}

            abi_functions = [item for item in abi_json if item["type"] == "function"]
            abi_events = [item for item in abi_json if item["type"] == "event"]

            abi_external_calls = [
                item for item in abi_json if item["type"] == "external_call"
            ]

            external_calls = []

            for external_call in abi_external_calls:
                try:
                    func_input_abi = []
                    input_args = []
                    for func_input in external_call["inputs"]:
                        func_input_abi.append(
                            {"name": func_input["name"], "type": func_input["type"]}
                        )
                        input_args.append(
                            cast_to_python_type(func_input["type"])(func_input["value"])
                        )

                    func_abi = [
                        {
                            "name": external_call["name"],
                            "inputs": func_input_abi,
                            "outputs": external_call["outputs"],
                            "type": "function",
                            "stateMutability": "view",
                        }
                    ]

                    external_calls.append(
                        {
                            "display_name": external_call["display_name"],
                            "address": Web3.toChecksumAddress(external_call["address"]),
                            "name": external_call["name"],
                            "abi": func_abi,
                            "input_args": input_args,
                        }
                    )
                except Exception as e:
                    print(f"Error processing external call: {e}")

            web3_client = connect(blockchain_type)
            # {
            #   "type": "external_call"
            #   "display_name": "Total weth earned"
            #   "address": "0xdf2811b6432cae65212528f0a7186b71adaec03a",
            #   "name": "balanceOf",
            #   "inputs": [
            #     {
            #       "name": "owner",
            #       "type": "address"
            #       "value": "0xA993c4759B731f650dfA011765a6aedaC91a4a88"
            #     }
            #   ],
            #   "outputs": [
            #   {
            #       "internalType": "uint256",
            #       "name": "",
            #       "type": "uint256"
            #   }
            # }

            extention_data = []
            for extcall in external_calls:
                try:
                    contract = web3_client.eth.contract(
                        address=extcall["address"], abi=extcall["abi"]
                    )
                    response = contract.functions[extcall["name"]](
                        *extcall["input_args"]
                    ).call()

                    extention_data.append(
                        {"display_name": extcall["display_name"], "value": response}
                    )
                except Exception as e:
                    print(f"Failed to call {extcall['name']} error: {e}")

            extention_data.append(
                {
                    "display_name": "Overall unique token owners.",
                    "value": get_unique_address(
                        db_session=db_session,
                        blockchain_type=blockchain_type,
                        address=address,
                    ),
                }
            )

            abi_functions_names = [item["name"] for item in abi_functions]

            abi_events_names = [item["name"] for item in abi_events]

            if "HatchStartedEvent" in abi_events_names:

                extention_data.append(
                    {
                        "display_name": "Number of hatches started.",
                        "value": get_count(
                            name="HatchStartedEvent",
                            type="event",
                            db_session=db_session,
                            blockchain_type=blockchain_type,
                            address=address,
                        ),
                    }
                )

            if "HatchFinishedEvent" in abi_events_names:

                extention_data.append(
                    {
                        "display_name": "Number of hatches finished.",
                        "value": get_count(
                            name="HatchFinishedEvent",
                            type="event",
                            db_session=db_session,
                            blockchain_type=blockchain_type,
                            address=address,
                        ),
                    }
                )

            for timescale in [timescale.value for timescale in TimeScale]:

                start_date = (
                    datetime.utcnow() - timescales_delta[timescale]["timedelta"]
                )

                print(f"Timescale: {timescale}")

                s3_data_object["web3_metric"] = extention_data

                functions_calls_data = generate_data(
                    db_session=db_session,
                    blockchain_type=blockchain_type,
                    address=address,
                    timescale=timescale,
                    functions=abi_functions_names,
                    start=start_date,
                    metric_type="tx_call",
                )

                s3_data_object["functions"] = functions_calls_data
                # generate data

                events_data = generate_data(
                    db_session=db_session,
                    blockchain_type=blockchain_type,
                    address=address,
                    timescale=timescale,
                    functions=abi_events_names,
                    start=start_date,
                    metric_type="event",
                )

                s3_data_object["events"] = events_data

                s3_data_object["generic"] = generate_metrics(
                    db_session=db_session,
                    blockchain_type=blockchain_type,
                    address=address,
                    timescale=timescale,
                    metrics=abi_events_names,
                    start=start_date,
                )

                push_statistics(
                    statistics_data=s3_data_object,
                    subscription=subscription,
                    timescale=timescale,
                    bucket=bucket,
                    hash=hash,
                )
            already_processed.append(f"{address}/{hash}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Command Line Interface")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(
        description="Drone dashboard statistics commands"
    )

    # Statistics parser
    parser_generate = subcommands.add_parser(
        "generate", description="Generate statistics"
    )
    parser_generate.set_defaults(func=lambda _: parser_generate.print_help())
    parser_generate.add_argument(
        "--blockchain",
        required=True,
        help=f"Available blockchain types: {[member.value for member in AvailableBlockchainType]}",
    )
    parser_generate.set_defaults(func=stats_generate_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
