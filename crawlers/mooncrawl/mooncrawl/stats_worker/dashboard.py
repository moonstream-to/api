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
from typing import Any, Callable, cast, Dict, List, Optional, Union
from uuid import UUID

import boto3  # type: ignore
from bugout.data import (
    BugoutJournalEntity,
    BugoutResource,
    BugoutResources,
    BugoutSearchResultAsEntity,
)
from moonstreamdb.blockchain import (
    AvailableBlockchainType,
    get_label_model,
    get_transaction_model,
)
from sqlalchemy import and_, distinct, extract, func, text
from sqlalchemy import cast as sqlalchemy_cast
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import in_op
from web3 import Web3

from ..blockchain import connect
from ..db import yield_db_read_only_session_ctx
from ..reporter import reporter
from ..settings import (
    BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
    CRAWLER_LABEL,
    MOONSTREAM_ADMIN_ACCESS_TOKEN,
    MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET,
    MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX,
    NB_CONTROLLER_ACCESS_ID,
)
from ..settings import bugout_client as bc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


subscription_id_by_blockchain = {
    "ethereum": "ethereum_smartcontract",
    "polygon": "polygon_smartcontract",
    "mumbai": "mumbai_smartcontract",
    "xdai": "xdai_smartcontract",
    "wyrm": "wyrm_smartcontract",
    "zksync_era_testnet": "zksync_era_testnet_smartcontract",
}

blockchain_by_subscription_id = {
    "ethereum_blockchain": "ethereum",
    "polygon_blockchain": "polygon",
    "mumbai_blockchain": "mumbai",
    "xdai_blockchain": "xdai",
    "wyrm_blockchain": "wyrm",
    "zksync_era_testnet_blockchain": "zksync_era_testnet",
    "ethereum_smartcontract": "ethereum",
    "polygon_smartcontract": "polygon",
    "mumbai_smartcontract": "mumbai",
    "xdai_smartcontract": "xdai",
    "wyrm_smartcontract": "wyrm",
    "zksync_era_testnet_smartcontract": "zksync_era_testnet",
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
    subscription_type_id: str,
    address: str,
    timescale: str,
    bucket: str,
    dashboard_id: Union[UUID, str],
) -> None:
    result_bytes = json.dumps(statistics_data).encode("utf-8")
    result_key = f"{MOONSTREAM_S3_SMARTCONTRACTS_ABI_PREFIX}/{blockchain_by_subscription_id[subscription_type_id]}/contracts_data/{address}/{dashboard_id}/v1/{timescale}.json"

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
    # end = datetime.utcnow()

    # Get data in selected timerage

    query_data = (
        db_session.query(
            func.to_char(
                func.to_timestamp(label_model.block_timestamp), time_format
            ).label("timeseries_points"),
            func.count(label_model.id).label("count"),
            label_model.label_data["name"].astext.label("label"),
        )
        .filter(label_model.address == address)
        .filter(label_model.label == crawler_label)
        .filter(label_model.label_data["type"].astext == metric_type)
        .filter(in_op(label_model.label_data["name"].astext, functions))
        .filter(
            label_model.block_timestamp
            >= sqlalchemy_cast(
                extract("epoch", start), label_model.block_timestamp.type
            )
        )
        .filter(
            label_model.block_timestamp
            < sqlalchemy_cast(
                extract("epoch", (start + timescales_delta[timescale]["timedelta"])),
                label_model.block_timestamp.type,
            )
        )
        .group_by(text("timeseries_points"), label_model.label_data["name"].astext)
        .order_by(text("timeseries_points DESC"))
    )

    with_timetrashold_data = query_data.cte(name="timetrashold_data")

    # Get availabel labels

    requested_labels = db_session.query(
        with_timetrashold_data.c.label.label("label")
    ).distinct()

    with_requested_labels = requested_labels.cte(name="requested_labels")

    # empty time series

    time_series = db_session.query(
        func.generate_series(
            start,
            start + timescales_delta[timescale]["timedelta"],
            time_step,
        ).label("timeseries_points")
    )

    with_time_series = time_series.cte(name="time_series")
    # empty_times_series_with_tags

    empty_times_series_with_tags = db_session.query(
        func.to_char(with_time_series.c.timeseries_points, time_format).label(
            "timeseries_points"
        ),
        with_requested_labels.c.label.label("label"),
    )

    with_empty_times_series_with_tags = empty_times_series_with_tags.cte(
        name="empty_times_series_with_tags"
    )

    # fill time series with data

    labels_time_series = (
        db_session.query(
            with_empty_times_series_with_tags.c.timeseries_points.label(
                "timeseries_points"
            ),
            with_empty_times_series_with_tags.c.label.label("label"),
            with_timetrashold_data.c.count.label("count"),
        )
        .join(
            with_empty_times_series_with_tags,
            and_(
                with_empty_times_series_with_tags.c.label
                == with_timetrashold_data.c.label,
                with_empty_times_series_with_tags.c.timeseries_points
                == with_timetrashold_data.c.timeseries_points,
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

    max_transactions_number = (
        db_session.query(transactions_model.block_number)
        .order_by(transactions_model.block_number.desc())
        .limit(1)
    ).subquery("max_transactions_number")

    max_label_number = (
        db_session.query(label_model.block_number)
        .order_by(label_model.block_number.desc())
        .filter(label_model.label == CRAWLER_LABEL)
        .limit(1)
    ).subquery("max_label_models_number")

    min_label_number = (
        db_session.query(label_model.block_number)
        .order_by(label_model.block_number.asc())
        .filter(label_model.label == CRAWLER_LABEL)
        .limit(1)
    ).subquery("min_label_models_number")

    result = (
        db_session.query(
            max_label_number.c.block_number.label("latest_labelled_block"),
            min_label_number.c.block_number.label("earliest_labelled_block"),
            max_transactions_number.c.block_number,
        )
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


def process_external_merged(
    external_calls: Dict[str, Dict[str, Any]],
    blockchain: AvailableBlockchainType,
    access_id: Optional[UUID] = None,
):
    """
    Process external calls
    """

    external_calls_normalized = []

    result: Dict[str, Any] = {}

    for external_call_hash, external_call in external_calls.items():
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

            external_calls_normalized.append(
                {
                    "external_call_hash": external_call_hash,
                    "address": Web3.toChecksumAddress(external_call["address"]),
                    "name": external_call["name"],
                    "abi": func_abi,
                    "input_args": input_args,
                }
            )
        except Exception as e:
            logger.error(f"Error processing external call: {e}")

    if external_calls_normalized:
        web3_client = connect(blockchain, access_id=access_id)

    for extcall in external_calls_normalized:
        try:
            contract = web3_client.eth.contract(
                address=extcall["address"], abi=extcall["abi"]
            )
            response = contract.functions[extcall["name"]](
                *extcall["input_args"]
            ).call()

            result[extcall["external_call_hash"]] = response
        except Exception as e:
            logger.error(f"Failed to call {extcall['external_call_hash']} error: {e}")

    return result


def process_external(
    abi_external_calls: List[Dict[str, Any]],
    blockchain: AvailableBlockchainType,
    access_id: Optional[UUID] = None,
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
        web3_client = connect(blockchain, access_id=access_id)

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
    access_id: Optional[UUID] = None,
) -> List[Any]:
    """
    Generate stats for cards components
    """

    extention_data = []

    abi_external_calls = [item for item in abi_json if item["type"] == "external_call"]

    extention_data = process_external(
        abi_external_calls=abi_external_calls,
        blockchain=blockchain_type,
        access_id=access_id,
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

    with yield_db_read_only_session_ctx() as db_session:
        start_time = time.time()

        dashboard_resources: BugoutResources = bc.list_resources(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            params={"type": BUGOUT_RESOURCE_TYPE_DASHBOARD},
            timeout=10,
        )

        dashboards_by_subscription: Dict[str, List[BugoutResource]] = {}

        for dashboard in dashboard_resources.resources:
            dashboard_subscription_settings = dashboard.resource_data.get(
                "subscription_settings"
            )

            if dashboard_subscription_settings:
                for dashboard_setting in dashboard_subscription_settings:
                    subscription_id = dashboard_setting.get("subscription_id")

                    if subscription_id:
                        if subscription_id not in dashboards_by_subscription:
                            dashboards_by_subscription[subscription_id] = []
                        dashboards_by_subscription[subscription_id].append(dashboard)

        logger.info(f"Amount of dashboards: {len(dashboard_resources.resources)}")

        # Get all users entity collections

        user_entity_collections: BugoutResources = bc.list_resources(
            token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
            params={
                "type": BUGOUT_RESOURCE_TYPE_ENTITY_SUBSCRIPTION,
            },
        )

        user_collection_by_id = {
            str(collection.resource_data["user_id"]): collection.resource_data[
                "collection_id"
            ]
            for collection in user_entity_collections.resources
            if collection.resource_data.get("collection_id")
        }

        subscriptions_count = 0

        # generate merged events and functions calls for all subscriptions

        merged_events: Dict[str, Any] = {}

        merged_functions: Dict[str, Any] = {}

        merged_external_calls: Dict[str, Any] = {}

        merged_external_calls["merged"] = {}

        """
        {
            address: {
                "subscription_id": []
            }
            ...
            "merdged": {
        }
        
        """

        address_dashboard_id_subscription_id_tree: Dict[str, Any] = {}

        for user_id, journal_id in user_collection_by_id.items():
            # request all subscriptions for user

            user_subscriptions = bc.search(
                token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
                journal_id=journal_id,
                query=f"tag:subscription_type_id:{subscription_id_by_blockchain[args.blockchain]}",
                representation="entity",
            )

            user_subscriptions_results = cast(
                List[BugoutSearchResultAsEntity], user_subscriptions.results
            )
            logger.info(
                f"Amount of user subscriptions: {len(user_subscriptions_results)}"
            )

            for subscription in user_subscriptions_results:
                entity_url_list = subscription.entity_url.split("/")
                subscription_id = entity_url_list[len(entity_url_list) - 1]

                if subscription_id not in dashboards_by_subscription:
                    logger.info(
                        f"Subscription {subscription_id} has no dashboard. Skipping."
                    )
                    continue

                dashboards = dashboards_by_subscription[subscription_id]

                for dashboard in dashboards:
                    for dashboard_subscription_filters in dashboard.resource_data[
                        "subscription_settings"
                    ]:
                        try:
                            subscription_id = dashboard_subscription_filters[
                                "subscription_id"
                            ]

                            try:
                                UUID(subscription_id)
                            except Exception as err:
                                logger.error(
                                    f"Subscription id {subscription_id} is not valid UUID: {err}"
                                )
                                continue

                            address = subscription.address

                            if address not in address_dashboard_id_subscription_id_tree:
                                address_dashboard_id_subscription_id_tree[address] = {}

                            if (
                                str(dashboard.id)
                                not in address_dashboard_id_subscription_id_tree
                            ):
                                address_dashboard_id_subscription_id_tree[address][
                                    str(dashboard.id)
                                ] = []

                            if (
                                subscription_id
                                not in address_dashboard_id_subscription_id_tree[
                                    address
                                ][str(dashboard.id)]
                            ):
                                address_dashboard_id_subscription_id_tree[address][
                                    str(dashboard.id)
                                ].append(subscription_id)

                            abi = None
                            if "abi" in subscription.secondary_fields:
                                abi = subscription.secondary_fields["abi"]

                            # Read required events, functions and web3_call form ABI
                            if abi is None:
                                methods = []
                                events = []
                                abi_json = {}

                            else:
                                abi_json = json.loads(abi)

                                methods = generate_list_of_names(
                                    type="function",
                                    subscription_filters=dashboard_subscription_filters,
                                    read_abi=dashboard_subscription_filters[
                                        "all_methods"
                                    ],
                                    abi_json=abi_json,
                                )

                                events = generate_list_of_names(
                                    type="event",
                                    subscription_filters=dashboard_subscription_filters,
                                    read_abi=dashboard_subscription_filters[
                                        "all_events"
                                    ],
                                    abi_json=abi_json,
                                )

                            if address not in merged_events:
                                merged_events[address] = {}
                                merged_events[address]["merged"] = set()

                            if address not in merged_functions:
                                merged_functions[address] = {}
                                merged_functions[address]["merged"] = set()

                            if str(dashboard.id) not in merged_events[address]:
                                merged_events[address][str(dashboard.id)] = {}

                            if str(dashboard.id) not in merged_functions[address]:
                                merged_functions[address][str(dashboard.id)] = {}

                            merged_events[address][str(dashboard.id)][
                                subscription_id
                            ] = events
                            merged_functions[address][str(dashboard.id)][
                                subscription_id
                            ] = methods

                            # Get external calls from ABI.
                            # external_calls merging required direct hash of external_call object.
                            # or if more correct hash of address and function call signature.
                            # create external_call selectors.

                            external_calls = [
                                external_call
                                for external_call in abi_json
                                if external_call["type"] == "external_call"
                            ]
                            if len(external_calls) > 0:
                                for external_call in external_calls:
                                    # create external_call selectors.
                                    # display_name not included in hash
                                    external_call_without_display_name = {
                                        "type": "external_call",
                                        "address": external_call["address"],
                                        "name": external_call["name"],
                                        "inputs": external_call["inputs"],
                                        "outputs": external_call["outputs"],
                                    }

                                    external_call_hash = hashlib.md5(
                                        json.dumps(
                                            external_call_without_display_name
                                        ).encode("utf-8")
                                    ).hexdigest()

                                    if str(dashboard.id) not in merged_external_calls:
                                        merged_external_calls[str(dashboard.id)] = {}

                                    if (
                                        subscription_id
                                        not in merged_external_calls[str(dashboard.id)]
                                    ):
                                        merged_external_calls[str(dashboard.id)][
                                            subscription_id
                                        ] = {}

                                    if (
                                        external_call_hash
                                        not in merged_external_calls[str(dashboard.id)][
                                            subscription_id
                                        ]
                                    ):
                                        merged_external_calls[str(dashboard.id)][
                                            subscription_id
                                        ] = {
                                            external_call_hash: external_call[
                                                "display_name"
                                            ]
                                        }
                                    if (
                                        external_call_hash
                                        not in merged_external_calls["merged"]
                                    ):
                                        merged_external_calls["merged"][
                                            external_call_hash
                                        ] = external_call_without_display_name

                            # Fill merged events and functions calls for all subscriptions

                            for event in events:
                                merged_events[address]["merged"].add(event)

                            for method in methods:
                                merged_functions[address]["merged"].add(method)

                        except Exception as e:
                            logger.error(f"Error while merging subscriptions: {e}")

        # Request contracts for external calls.
        # result is a {call_hash: value} dictionary.

        external_calls_results = process_external_merged(
            external_calls=merged_external_calls["merged"],
            blockchain=blockchain_type,
            access_id=args.access_id,
        )

        for address in address_dashboard_id_subscription_id_tree.keys():
            current_blocks_state = get_blocks_state(
                db_session=db_session, blockchain_type=blockchain_type
            )

            s3_data_object_for_contract: Dict[str, Any] = {}

            crawler_label = CRAWLER_LABEL

            for timescale in [timescale.value for timescale in TimeScale]:
                try:
                    start_date = (
                        datetime.utcnow() - timescales_delta[timescale]["timedelta"]
                    )

                    logger.info(f"Timescale: {timescale}")

                    # Write state of blocks in database
                    s3_data_object_for_contract["blocks_state"] = current_blocks_state

                    # TODO(Andrey): Remove after https://github.com/bugout-dev/moonstream/issues/524
                    s3_data_object_for_contract["generic"] = {}

                    # Generate functions call timeseries
                    functions_calls_data = generate_data(
                        db_session=db_session,
                        blockchain_type=blockchain_type,
                        address=address,
                        timescale=timescale,
                        functions=merged_functions[address]["merged"],
                        start=start_date,
                        metric_type="tx_call",
                        crawler_label=crawler_label,
                    )
                    s3_data_object_for_contract["methods"] = functions_calls_data

                    # Generte events timeseries
                    events_data = generate_data(
                        db_session=db_session,
                        blockchain_type=blockchain_type,
                        address=address,
                        timescale=timescale,
                        functions=merged_events[address]["merged"],
                        start=start_date,
                        metric_type="event",
                        crawler_label=crawler_label,
                    )
                    s3_data_object_for_contract["events"] = events_data

                    for dashboard_id in address_dashboard_id_subscription_id_tree[
                        address
                    ]:  # Dashboards loop for address
                        for (
                            subscription_id
                        ) in address_dashboard_id_subscription_id_tree[address][
                            dashboard_id
                        ]:
                            try:
                                extention_data = []

                                s3_subscription_data_object: Dict[str, Any] = {}

                                s3_subscription_data_object[
                                    "blocks_state"
                                ] = s3_data_object_for_contract["blocks_state"]

                                if dashboard_id in merged_external_calls:
                                    for (
                                        external_call_hash,
                                        display_name,
                                    ) in merged_external_calls[dashboard_id][
                                        subscription_id
                                    ].items():
                                        if external_call_hash in external_calls_results:
                                            extention_data.append(
                                                {
                                                    "display_name": display_name,
                                                    "value": external_calls_results[
                                                        external_call_hash
                                                    ],
                                                }
                                            )

                                s3_subscription_data_object[
                                    "web3_metric"
                                ] = extention_data

                                # list of user defined events

                                events_list = merged_events[address][dashboard_id][
                                    subscription_id
                                ]

                                s3_subscription_data_object["events"] = {}

                                for event in events_list:
                                    if event in events_data:
                                        s3_subscription_data_object["events"][
                                            event
                                        ] = events_data[event]

                                # list of user defined functions

                                functions_list = merged_functions[address][
                                    dashboard_id
                                ][subscription_id]

                                s3_subscription_data_object["methods"] = {}

                                for function in functions_list:
                                    if function in functions_calls_data:
                                        s3_subscription_data_object["methods"][
                                            function
                                        ] = functions_calls_data[function]

                                # Push data to S3 bucket
                                push_statistics(
                                    statistics_data=s3_subscription_data_object,
                                    subscription_type_id=subscription_id_by_blockchain[
                                        args.blockchain
                                    ],
                                    address=address,
                                    timescale=timescale,
                                    bucket=MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET,  # type: ignore
                                    dashboard_id=dashboard_id,
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
                                        f"dashboard:{dashboard}",
                                    ],
                                )
                                logger.error(err)
                except Exception as err:
                    db_session.rollback()
                    reporter.error_report(
                        err,
                        [
                            "dashboard",
                            "statistics",
                            f"blockchain:{args.blockchain}" f"timescale:{timescale}",
                            f"data_generation_failed",
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
    subscription_by_id: Dict[str, BugoutJournalEntity],
    access_id: Optional[UUID] = None,
):
    """
    Start crawler with generate.
    """

    with yield_db_read_only_session_ctx() as db_session:
        logger.info(f"Amount of blockchain subscriptions: {len(subscription_by_id)}")

        for dashboard_subscription_filters in dashboard.resource_data[
            "subscription_settings"
        ]:
            try:
                subscription_id = dashboard_subscription_filters["subscription_id"]

                subscription_type_id = None
                for required_field in subscription_by_id[
                    subscription_id
                ].required_fields:
                    if "subscription_type_id" in required_field:
                        subscription_type_id = required_field["subscription_type_id"]

                if not subscription_type_id:
                    logger.warning(
                        f"Subscription type not found for subscription: {subscription_id}"
                    )
                    continue

                blockchain_type = AvailableBlockchainType(
                    blockchain_by_subscription_id[subscription_type_id]
                )

                s3_data_object: Dict[str, Any] = {}

                extention_data = []

                address = subscription_by_id[subscription_id].address

                crawler_label = CRAWLER_LABEL

                abi = None
                if "abi" in subscription_by_id[subscription_id].secondary_fields:
                    abi = subscription_by_id[subscription_id].secondary_fields["abi"]

                # Read required events, functions and web3_call form ABI
                if abi is None:
                    methods = []
                    events = []
                    abi_json = {}

                else:
                    abi_json = json.loads(abi)

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
                    access_id=access_id,
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
                        subscription_type_id=subscription_type_id,
                        address=address,
                        timescale=timescale,
                        bucket=MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET,  # type: ignore
                        dashboard_id=dashboard.id,
                    )
            except Exception as err:
                reporter.error_report(
                    err,
                    [
                        "dashboard",
                        "statistics",
                        f"subscriptions:{subscription_id}",
                        f"dashboard:{str(dashboard.id)}",
                    ],
                )
                logger.error(err)


def main() -> None:
    parser = argparse.ArgumentParser(description="Command Line Interface")
    parser.set_defaults(func=lambda _: parser.print_help())

    parser.add_argument(
        "--access-id",
        default=NB_CONTROLLER_ACCESS_ID,
        type=UUID,
        help="User access ID",
    )

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
