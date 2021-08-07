from datetime import datetime
import logging


from typing import Dict, Any, List, Optional, Union
from moonstreamdb.models import (
    EthereumBlock,
    EthereumTransaction,
    EthereumPendingTransaction,
)
from sqlalchemy import or_, and_, text
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc, false

from . import data

from .settings import DEFAULT_STREAM_TIMEINTERVAL


logger = logging.getLogger(__name__)


async def get_transaction_in_blocks(
    db_session: Session,
    query: str,
    user_subscriptions_resources_by_address: Dict[str, Any],
    start_time: Optional[int] = 0,
    end_time: Optional[int] = 0,
) -> List[data.EthereumTransactionItem]:

    subscriptions_addresses = list(user_subscriptions_resources_by_address.keys())

    if start_time < 1438215988:  # first block
        start_time = False

    if end_time < 1438215988:  # first block
        end_time = False

    if query == "" or query == " ":

        filters = [
            or_(
                EthereumTransaction.to_address == address,
                EthereumTransaction.from_address == address,
            )
            for address in subscriptions_addresses
        ]
        filters = or_(*filters)

    else:
        filters = database_search_query(
            query, allowed_addresses=subscriptions_addresses
        )
        if not filters:
            return [], None, None
        filters = and_(*filters)

    # Get start point
    if start_time is False and end_time is False:
        ethereum_transaction_start_point = (
            db_session.query(
                EthereumTransaction.hash,
                EthereumTransaction.block_number,
                EthereumTransaction.from_address,
                EthereumTransaction.to_address,
                EthereumTransaction.gas,
                EthereumTransaction.gas_price,
                EthereumTransaction.input,
                EthereumTransaction.nonce,
                EthereumTransaction.value,
                EthereumBlock.timestamp.label("timestamp"),
            )
            .join(EthereumBlock)
            .filter(filters)
            .order_by(text("timestamp desc"))
            .limit(1)
        ).one_or_none()
        start_time = False
        print(ethereum_transaction_start_point)
        end_time = ethereum_transaction_start_point[-1]

    ethereum_transactions = (
        db_session.query(
            EthereumTransaction.hash,
            EthereumTransaction.block_number,
            EthereumTransaction.from_address,
            EthereumTransaction.to_address,
            EthereumTransaction.gas,
            EthereumTransaction.gas_price,
            EthereumTransaction.input,
            EthereumTransaction.nonce,
            EthereumTransaction.value,
            EthereumBlock.timestamp.label("timestamp"),
        )
        .join(EthereumBlock)
        .filter(filters)
    )

    print(f"last record: {end_time}")

    if start_time and end_time:
        if start_time < end_time:
            start_time, end_time = end_time, start_time

    if start_time:
        ethereum_transactions = ethereum_transactions.filter(
            EthereumBlock.timestamp <= start_time
        )

        print(start_time)

        future_last_transaction = (
            db_session.query(
                EthereumTransaction.hash,
                EthereumTransaction.block_number,
                EthereumTransaction.from_address,
                EthereumTransaction.to_address,
                EthereumTransaction.gas,
                EthereumTransaction.gas_price,
                EthereumTransaction.input,
                EthereumTransaction.nonce,
                EthereumTransaction.value,
                EthereumBlock.timestamp.label("timestamp"),
            )
            .join(EthereumBlock)
            .filter(filters)
            .filter(EthereumBlock.timestamp > start_time)
            .order_by(text("timestamp desc"))
            .limit(1)
        ).one_or_none()
        start_time = False

        if future_last_transaction:
            next_future_timestamp = future_last_transaction[-1]
        else:
            next_future_timestamp = None

    if end_time:
        ethereum_transactions = ethereum_transactions.filter(
            EthereumBlock.timestamp >= end_time
        )
        print("end_time", end_time)
        next_last_transaction = (
            db_session.query(
                EthereumTransaction.hash,
                EthereumTransaction.block_number,
                EthereumTransaction.from_address,
                EthereumTransaction.to_address,
                EthereumTransaction.gas,
                EthereumTransaction.gas_price,
                EthereumTransaction.input,
                EthereumTransaction.nonce,
                EthereumTransaction.value,
                EthereumBlock.timestamp.label("timestamp"),
            )
            .join(EthereumBlock)
            .filter(filters)
            .filter(1628263498 > EthereumBlock.timestamp)
            .order_by(text("timestamp desc"))
            .limit(1)
        ).one_or_none()
        start_time = False
        print("next_last_transaction_timestamp", next_last_transaction)
        if next_last_transaction:
            next_last_transaction_timestamp = next_last_transaction[-1]
        else:
            next_last_transaction_timestamp = None

    print(f"count: {ethereum_transactions.count()}")

    response = []
    for row_index, (
        hash,
        block_number,
        from_address,
        to_address,
        gas,
        gas_price,
        input,
        nonce,
        value,
        timestamp,
    ) in enumerate(ethereum_transactions):

        subscription_type_id = None
        from_label = None
        to_label = None
        color = None

        if from_address in subscriptions_addresses:
            from_label = user_subscriptions_resources_by_address[from_address]["label"]
            subscription_type_id = user_subscriptions_resources_by_address[
                from_address
            ]["subscription_type_id"]
            color = user_subscriptions_resources_by_address[from_address]["color"]

        if to_address in subscriptions_addresses:
            subscription_type_id = user_subscriptions_resources_by_address[to_address][
                "subscription_type_id"
            ]
            to_label = user_subscriptions_resources_by_address[to_address]["label"]
            color = user_subscriptions_resources_by_address[to_address]["color"]

        response.append(
            data.EthereumTransactionItem(
                color=color,
                from_label=from_label,
                to_label=to_label,
                block_number=block_number,
                gas=gas,
                gasPrice=gas_price,
                value=value,
                from_address=from_address,
                to_address=to_address,
                hash=hash,
                input=input,
                nonce=nonce,
                timestamp=timestamp,
                subscription_type_id=subscription_type_id,
            )
        )

    return (
        response,
        end_time,
        next_future_timestamp,
        next_last_transaction_timestamp,
    )


def database_search_query(q: str, allowed_addresses: List[str]):

    filters = q.split("+")
    constructed_filters = []
    for filter_item in filters:
        if filter_item == "":
            logger.warning("Skipping empty filter item")
            continue

        # Try Google style search filters
        components = filter_item.split(":")
        if len(components) == 2:
            filter_type = components[0]
            filter_value = components[1]
        else:
            continue

        if filter_type == "to" and filter_value:
            constructed_filters.append(EthereumTransaction.to_address == filter_value)

        if filter_type == "from" and filter_value:
            if filter_value not in allowed_addresses:
                continue
            constructed_filters.append(EthereumTransaction.from_address == filter_value)

        if filter_type == "address" and filter_value:
            constructed_filters.append(
                or_(
                    EthereumTransaction.to_address == filter_value,
                    EthereumTransaction.from_address == filter_value,
                )
            )

    return constructed_filters
