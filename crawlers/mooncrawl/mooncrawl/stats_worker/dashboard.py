"""
Generates dashboard.
"""
import argparse
import hashlib
import json
import logging
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List
from uuid import UUID

import boto3  # type: ignore
from bugout.data import BugoutResource, BugoutResources
from moonstreamdb.db import yield_db_session_ctx
from sqlalchemy import Column, and_, distinct, func, text
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql.operators import in_op
from web3 import Web3

from ..blockchain import (
    connect,
    get_label_model,
    get_transaction_model,
)
from ..data import AvailableBlockchainType
from ..reporter import reporter
from ..settings import (
    CRAWLER_LABEL,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX,
)
from ..settings import bugout_client as bc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


subscription_ids_by_blockchain = {
    "ethereum": ["ethereum_blockchain", "ethereum_smartcontract"],
    "polygon": ["polygon_blockchain", "polygon_smartcontract"],
}

blockchain_by_subscription_id = {
    "ethereum_blockchain": "ethereum",
    "polygon_blockchain": "polygon",
    "ethereum_smartcontract": "ethereum",
    "polygon_smartcontract": "polygon",
}


class TimeScale(Enum):
    # TODO(Andrey) Unlock when we be sure about perfomanse of agregation on transactions table.
    # Right now it can be hungs
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


abi_type_to_dashboards_type = {"function": "methods", "event": "events"}

BUGOUT_RESOURCE_TYPE_SUBSCRIPTION = "subscription"
BUGOUT_RESOURCE_TYPE_DASHBOARD = "dashboards"


def push_statistics(
    statistics_data: Dict[str, Any],
    subscription: Any,
    timescale: str,
    bucket: str,
    dashboard_id: UUID,
) -> None:

    result_bytes = json.dumps(statistics_data).encode("utf-8")
    result_key = f'{MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX}/{blockchain_by_subscription_id[subscription.resource_data["subscription_type_id"]]}/contracts_data/{subscription.resource_data["address"]}/{dashboard_id}/v1/{timescale}.json'

    s3 = boto3.client("s3")
    s3.put_object(
        Body=result_bytes,
        Bucket=bucket,
        Key=result_key,
        ContentType="application/json",
        Metadata={"drone": "statistics"},
    )

    logger.info(f"Statistics push to bucket: s3://{bucket}/{result_key}")


def generate_data(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    address: str,
    timescale: str,
    functions: List[str],
    start: Any,
    metric_type: str,
    crawler_label: str,
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
        .filter(label_model.label == crawler_label)
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
        .filter(label_model.label == crawler_label)
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

    # split grafics

    label_counts_subquery = (
        label_counts.group_by(
            text("timeseries_points"), label_model.label_data["name"].astext
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
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    address: str,
    crawler_label: str,
):
    label_model = get_label_model(blockchain_type)

    return (
        db_session.query(label_model.label_data["args"]["to"])
        .filter(label_model.address == address)
        .filter(label_model.label == crawler_label)
        .filter(label_model.label_data["type"].astext == "event")
        .filter(label_model.label_data["name"].astext == "Transfer")
        .distinct()
        .count()
    )


def get_blocks_state(
    db_session: Session, blockchain_type: AvailableBlockchainType
) -> Dict[str, int]:

    """
    Generate meta information about
    """

    blocks_state = {
        "latest_stored_block": 0,
        "latest_labelled_block": 0,
        "earliest_labelled_block": 0,
    }

    label_model = get_label_model(blockchain_type)

    transactions_model = get_transaction_model(blockchain_type)

    max_transactions_number = db_session.query(
        func.max(transactions_model.block_number).label("block_number")
    ).scalar()

    result = (
        db_session.query(
            func.min(label_model.block_number).label("earliest_labelled_block"),
            func.max(label_model.block_number).label("latest_labelled_block"),
            max_transactions_number,
        ).filter(label_model.label == CRAWLER_LABEL)
    ).one_or_none()

    if result:
        earliest_labelled_block, latest_labelled_block, latest_stored_block = result
        blocks_state = {
            "latest_stored_block": latest_stored_block,
            "latest_labelled_block": latest_labelled_block,
            "earliest_labelled_block": earliest_labelled_block,
        }
    return blocks_state


def generate_list_of_names(
    type: str, subscription_filters: Dict[str, Any], read_abi: bool, abi_json: Any
):

    """
    Generate list of names for select from database by name field
    """

    if read_abi:
        names = [item["name"] for item in abi_json if item["type"] == type]
    else:

        names = [
            item["name"]
            for item in subscription_filters[abi_type_to_dashboards_type[type]]
        ]

    return names


def process_external(
    abi_external_calls: List[Dict[str, Any]], blockchain: AvailableBlockchainType
):
    """
    Request all required external data
    TODO:(Andrey) Check posibility do it via AsyncHttpProvider(not supported for some of middlewares).
    """

    extention_data = []

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
            logger.error(f"Error processing external call: {e}")

    if external_calls:
        web3_client = connect(blockchain)

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
            logger.error(f"Failed to call {extcall['name']} error: {e}")

    return extention_data


def get_count(
    name: str,
    type: str,
    db_session: Session,
    select_expression: Any,
    blockchain_type: AvailableBlockchainType,
    address: str,
    crawler_label: str,
):
    """
    Return count of event from database.
    """
    label_model = get_label_model(blockchain_type)

    return (
        db_session.query(select_expression)
        .filter(label_model.address == address)
        .filter(label_model.label == crawler_label)
        .filter(label_model.label_data["type"].astext == type)
        .filter(label_model.label_data["name"].astext == name)
        .count()
    )


def generate_web3_metrics(
    db_session: Session,
    events: List[str],
    blockchain_type: AvailableBlockchainType,
    address: str,
    crawler_label: str,
    abi_json: Any,
) -> List[Any]:
    """
    Generate stats for cards components
    """

    extention_data = []

    abi_external_calls = [item for item in abi_json if item["type"] == "external_call"]

    extention_data = process_external(
        abi_external_calls=abi_external_calls,
        blockchain=blockchain_type,
    )

    extention_data.append(
        {
            "display_name": "Overall unique token owners.",
            "value": get_unique_address(
                db_session=db_session,
                blockchain_type=blockchain_type,
                address=address,
                crawler_label=crawler_label,
            ),
        }
    )

    # TODO: Remove it if ABI already have correct web3_call signature.

    if "HatchStartedEvent" in events:

        extention_data.append(
            {
                "display_name": "Number of hatches started.",
                "value": get_count(
                    name="HatchStartedEvent",
                    type="event",
                    db_session=db_session,
                    select_expression=get_label_model(blockchain_type),
                    blockchain_type=blockchain_type,
                    address=address,
                    crawler_label=crawler_label,
                ),
            }
        )

    if "HatchFinishedEvent" in events:

        extention_data.append(
            {
                "display_name": "Number of hatches finished.",
                "value": get_count(
                    name="HatchFinishedEvent",
                    type="event",
                    db_session=db_session,
                    select_expression=distinct(
                        get_label_model(blockchain_type).label_data["args"]["tokenId"]
                    ),
                    blockchain_type=blockchain_type,
                    address=address,
                    crawler_label=crawler_label,
                ),
            }
        )
    return extention_data


def stats_generate_handler(args: argparse.Namespace):
    """
    Start crawler with generate.
    """
    blockchain_type = AvailableBlockchainType(args.blockchain)

    with yield_db_session_ctx() as db_session:

        start_time = time.time()

        dashboard_resources: BugoutResources = bc.list_resources(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            params={"type": BUGOUT_RESOURCE_TYPE_DASHBOARD},
            timeout=10,
        )

        logger.info(f"Amount of dashboards: {len(dashboard_resources.resources)}")

        # get all subscriptions
        available_subscriptions: List[BugoutResource] = []

        for subscription_type in subscription_ids_by_blockchain[args.blockchain]:

            # Create subscriptions dict for get subscriptions by id.
            blockchain_subscriptions: BugoutResources = bc.list_resources(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                params={
                    "type": BUGOUT_RESOURCE_TYPE_SUBSCRIPTION,
                    "subscription_type_id": subscription_type,
                },
                timeout=10,
            )
            available_subscriptions.extend(blockchain_subscriptions.resources)

        subscription_by_id = {
            str(blockchain_subscription.id): blockchain_subscription
            for blockchain_subscription in available_subscriptions
        }

        logger.info(f"Amount of blockchain subscriptions: {len(subscription_by_id)}")

        s3_client = boto3.client("s3")

        subscriptions_count = 0

        for dashboard in dashboard_resources.resources:

            for dashboard_subscription_filters in dashboard.resource_data[
                "subscription_settings"
            ]:

                try:
                    subscription_id = dashboard_subscription_filters["subscription_id"]

                    if subscription_id not in subscription_by_id:
                        # Meen it's are different blockchain type
                        continue

                    subscriptions_count += 1
                    extention_data = []

                    # The resulting object whivh be pushed to S3
                    s3_data_object: Dict[str, Any] = {}

                    address = subscription_by_id[subscription_id].resource_data[
                        "address"
                    ]

                    crawler_label = CRAWLER_LABEL

                    if address in ("0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",):
                        crawler_label = "moonworm"

                    # Read required events, functions and web3_call form ABI
                    if not subscription_by_id[subscription_id].resource_data["abi"]:
                        methods = []
                        events = []
                        abi_json = {}

                    else:
                        bucket = subscription_by_id[subscription_id].resource_data[
                            "bucket"
                        ]
                        key = subscription_by_id[subscription_id].resource_data[
                            "s3_path"
                        ]
                        abi = s3_client.get_object(
                            Bucket=bucket,
                            Key=key,
                        )
                        abi_json = json.loads(abi["Body"].read())
                        methods = generate_list_of_names(
                            type="function",
                            subscription_filters=dashboard_subscription_filters,
                            read_abi=dashboard_subscription_filters["all_methods"],
                            abi_json=abi_json,
                        )
                        events = generate_list_of_names(
                            type="event",
                            subscription_filters=dashboard_subscription_filters,
                            read_abi=dashboard_subscription_filters["all_events"],
                            abi_json=abi_json,
                        )

                    extention_data = generate_web3_metrics(
                        db_session=db_session,
                        events=events,
                        blockchain_type=blockchain_type,
                        address=address,
                        crawler_label=crawler_label,
                        abi_json=abi_json,
                    )

                    # Generate blocks state information
                    current_blocks_state = get_blocks_state(
                        db_session=db_session, blockchain_type=blockchain_type
                    )

                    for timescale in [timescale.value for timescale in TimeScale]:

                        start_date = (
                            datetime.utcnow() - timescales_delta[timescale]["timedelta"]
                        )

                        logger.info(f"Timescale: {timescale}")

                        s3_data_object["web3_metric"] = extention_data

                        # Write state of blocks in database
                        s3_data_object["blocks_state"] = current_blocks_state

                        # TODO(Andrey): Remove after https://github.com/bugout-dev/moonstream/issues/524
                        s3_data_object["generic"] = {}

                        # Generate functions call timeseries
                        functions_calls_data = generate_data(
                            db_session=db_session,
                            blockchain_type=blockchain_type,
                            address=address,
                            timescale=timescale,
                            functions=methods,
                            start=start_date,
                            metric_type="tx_call",
                            crawler_label=crawler_label,
                        )
                        s3_data_object["methods"] = functions_calls_data

                        # Generte events timeseries
                        events_data = generate_data(
                            db_session=db_session,
                            blockchain_type=blockchain_type,
                            address=address,
                            timescale=timescale,
                            functions=events,
                            start=start_date,
                            metric_type="event",
                            crawler_label=crawler_label,
                        )
                        s3_data_object["events"] = events_data

                        # Push data to S3 bucket
                        push_statistics(
                            statistics_data=s3_data_object,
                            subscription=subscription_by_id[subscription_id],
                            timescale=timescale,
                            bucket=bucket,
                            dashboard_id=dashboard.id,
                        )
                except Exception as err:
                    db_session.rollback()
                    reporter.error_report(
                        err,
                        [
                            "dashboard",
                            "statistics",
                            f"blockchain:{args.blockchain}"
                            f"subscriptions:{subscription_id}",
                            f"dashboard:{dashboard.id}",
                        ],
                    )
                    logger.error(err)

        reporter.custom_report(
            title=f"Dashboard stats generated.",
            content=f"Generate statistics for {args.blockchain}. \n Generation time: {time.time() - start_time}. \n Total amount of dashboards: {len(dashboard_resources.resources)}. Generate stats for {subscriptions_count}.",
            tags=["dashboard", "statistics", f"blockchain:{args.blockchain}"],
        )


def stats_generate_api_task(
    timescales: List[str],
    dashboard: BugoutResource,
    subscription_by_id: Dict[str, BugoutResource],
):
    """
    Start crawler with generate.
    """

    with yield_db_session_ctx() as db_session:

        logger.info(f"Amount of blockchain subscriptions: {len(subscription_by_id)}")

        s3_client = boto3.client("s3")

        for dashboard_subscription_filters in dashboard.resource_data[
            "subscription_settings"
        ]:

            try:

                subscription_id = dashboard_subscription_filters["subscription_id"]

                blockchain_type = AvailableBlockchainType(
                    blockchain_by_subscription_id[
                        subscription_by_id[subscription_id].resource_data[
                            "subscription_type_id"
                        ]
                    ]
                )

                s3_data_object: Dict[str, Any] = {}

                extention_data = []

                address = subscription_by_id[subscription_id].resource_data["address"]

                crawler_label = CRAWLER_LABEL

                if address in ("0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f",):
                    crawler_label = "moonworm"

                # Read required events, functions and web3_call form ABI
                if not subscription_by_id[subscription_id].resource_data["abi"]:

                    methods = []
                    events = []
                    abi_json = {}

                else:

                    bucket = subscription_by_id[subscription_id].resource_data["bucket"]
                    key = subscription_by_id[subscription_id].resource_data["s3_path"]
                    abi = s3_client.get_object(
                        Bucket=bucket,
                        Key=key,
                    )
                    abi_json = json.loads(abi["Body"].read())

                    methods = generate_list_of_names(
                        type="function",
                        subscription_filters=dashboard_subscription_filters,
                        read_abi=dashboard_subscription_filters["all_methods"],
                        abi_json=abi_json,
                    )

                    events = generate_list_of_names(
                        type="event",
                        subscription_filters=dashboard_subscription_filters,
                        read_abi=dashboard_subscription_filters["all_events"],
                        abi_json=abi_json,
                    )

                # Data for cards components
                extention_data = generate_web3_metrics(
                    db_session=db_session,
                    events=events,
                    blockchain_type=blockchain_type,
                    address=address,
                    crawler_label=crawler_label,
                    abi_json=abi_json,
                )

                # Generate blocks state information
                current_blocks_state = get_blocks_state(
                    db_session=db_session, blockchain_type=blockchain_type
                )

                for timescale in timescales:

                    start_date = (
                        datetime.utcnow() - timescales_delta[timescale]["timedelta"]
                    )

                    logger.info(f"Timescale: {timescale}")

                    s3_data_object["web3_metric"] = extention_data

                    # Write state of blocks in database
                    s3_data_object["blocks_state"] = current_blocks_state

                    # TODO(Andrey): Remove after https://github.com/bugout-dev/moonstream/issues/524
                    s3_data_object["generic"] = {}

                    # Generate functions call timeseries
                    functions_calls_data = generate_data(
                        db_session=db_session,
                        blockchain_type=blockchain_type,
                        address=address,
                        timescale=timescale,
                        functions=methods,
                        start=start_date,
                        metric_type="tx_call",
                        crawler_label=crawler_label,
                    )
                    s3_data_object["methods"] = functions_calls_data

                    # Generate events timeseries
                    events_data = generate_data(
                        db_session=db_session,
                        blockchain_type=blockchain_type,
                        address=address,
                        timescale=timescale,
                        functions=events,
                        start=start_date,
                        metric_type="event",
                        crawler_label=crawler_label,
                    )
                    s3_data_object["events"] = events_data

                    # push data to S3 bucket
                    push_statistics(
                        statistics_data=s3_data_object,
                        subscription=subscription_by_id[subscription_id],
                        timescale=timescale,
                        bucket=bucket,
                        dashboard_id=dashboard.id,
                    )
            except Exception as err:
                reporter.error_report(
                    err,
                    [
                        "dashboard",
                        "statistics",
                        f"subscriptions:{subscription_id}",
                        f"dashboard:{dashboard.id}",
                    ],
                )
                logger.error(err)


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
