from datetime import datetime
import logging


from typing import Dict, Any, List, Optional, Union

from sqlalchemy.engine.base import Transaction
from moonstreamdb.models import (
    EthereumBlock,
    EthereumTransaction,
    EthereumPendingTransaction,
    EthereumAddress,
    EthereumLabel,
)
from sqlalchemy import or_, and_, text, union
from sqlalchemy.orm import Session

from . import data

from .settings import DEFAULT_STREAM_TIMEINTERVAL


logger = logging.getLogger(__name__)


async def get_transaction_in_blocks(
    db_session: Session,
    query: str,
    user_subscriptions_resources_by_address: Dict[str, Any],
    boundaries: data.PageBoundary,
) -> data.EthereumTransactionResponse:

    """
    Request transactions from database based on addresses from user subscriptions
    and selected boundaries.

    streams  empty for user without subscriptions
    Return last available transaction if boundaries is empty

    """

    subscriptions_addresses = list(user_subscriptions_resources_by_address.keys())

    if boundaries.start_time < 1438215988:  # first block
        boundaries.start_time = 0

    if boundaries.end_time < 1438215988:  # first block
        boundaries.end_time = 0

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
        filters = parse_search_query_to_sqlalchemy_filters(
            query, allowed_addresses=subscriptions_addresses
        )
        if not filters:
            return data.EthereumTransactionResponse(
                stream=[],
                boundaries=boundaries,
            )
        filters = and_(*filters)

    ethereum_transactions_in_subscriptions = (
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

    ethereum_transactions = ethereum_transactions_in_subscriptions

    # If not start_time and end_time not present
    # Get latest transaction
    if boundaries.end_time == 0:
        ethereum_transaction_start_point = (
            ethereum_transactions_in_subscriptions.order_by(
                text("timestamp desc")
            ).limit(1)
        ).one_or_none()
        if ethereum_transaction_start_point:
            boundaries.end_time = ethereum_transaction_start_point[-1]
            boundaries.start_time = (
                ethereum_transaction_start_point[-1] - DEFAULT_STREAM_TIMEINTERVAL
            )

    if boundaries.start_time != 0 and boundaries.end_time != 0:
        if boundaries.start_time > boundaries.end_time:
            boundaries.start_time, boundaries.end_time = (
                boundaries.end_time,
                boundaries.start_time,
            )

    if boundaries.end_time:
        ethereum_transactions = ethereum_transactions.filter(
            include_or_not_lower(
                EthereumBlock.timestamp, boundaries.include_end, boundaries.end_time
            )
        )

        next_transaction = (
            ethereum_transactions_in_subscriptions.filter(
                EthereumBlock.timestamp > boundaries.end_time
            )
            .order_by(text("timestamp ASC"))
            .limit(1)
        )

    if boundaries.start_time:
        ethereum_transactions = ethereum_transactions.filter(
            include_or_not_grater(
                EthereumBlock.timestamp,
                boundaries.include_start,
                boundaries.start_time,
            )
        )

        previous_transaction = (
            ethereum_transactions_in_subscriptions.filter(
                EthereumBlock.timestamp < boundaries.start_time
            )
            .order_by(text("timestamp desc"))
            .limit(1)
        )

    all_queries = [next_transaction, ethereum_transactions, previous_transaction]
    golden_set = union(*all_queries).alias()

    get_transaction = (
        db_session.query(
            golden_set.c.ethereum_transactions_hash,
            golden_set.c.ethereum_transactions_block_number,
            golden_set.c.ethereum_transactions_from_address,
            golden_set.c.ethereum_transactions_to_address,
            golden_set.c.ethereum_transactions_gas,
            golden_set.c.ethereum_transactions_gas_price,
            golden_set.c.ethereum_transactions_input,
            golden_set.c.ethereum_transactions_nonce,
            golden_set.c.ethereum_transactions_value,
            golden_set.c.timestamp.label("timestamp"),
        )
        .select_from(golden_set)
        .order_by(text("timestamp desc"))
    )
    response = []
    for index, (
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
    ) in enumerate(get_transaction):

        if index == 0:
            if timestamp > boundaries.end_time and boundaries.include_end:
                boundaries.next_event_time = timestamp
                continue
            elif timestamp == boundaries.end_time and not boundaries.include_end:
                boundaries.next_event_time = timestamp
                continue
        # Apply subscription data to each transaction
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

    if timestamp < boundaries.start_time and boundaries.start_time:
        boundaries.previous_event_time = timestamp
        response.pop()

    elif timestamp == boundaries.end_time and not boundaries.start_time:
        boundaries.previous_event_time = timestamp
        response.pop()

    return data.EthereumTransactionResponse(stream=response, boundaries=boundaries)


def include_or_not_grater(value1, include, value2):
    if include:
        return value1 >= value2
    else:
        return value1 > value2


def include_or_not_lower(value1, include, value2):
    if include:
        return value1 <= value2
    else:
        return value1 < value2


def parse_search_query_to_sqlalchemy_filters(q: str, allowed_addresses: List[str]):

    """
    Return list of sqlalchemy filters or empty list
    """

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


def get_address_labels(
    db_session: Session, start: int, limit: int, addresses: Optional[List[str]] = None
) -> List[EthereumAddress]:
    """
    Attach labels to addresses.
    """
    query = db_session.query(EthereumAddress)
    if addresses is not None:
        addresses_list = addresses.split(",")
        query = query.filter(EthereumAddress.address.in_(addresses_list))

    addresses_obj = query.order_by(EthereumAddress.id).slice(start, start + limit).all()

    addresses_response = data.AddressListLabelsResponse(addresses=[])

    for address in addresses_obj:
        labels_obj = (
            db_session.query(EthereumLabel)
            .filter(EthereumLabel.address_id == address.id)
            .all()
        )
        addresses_response.addresses.append(
            data.AddressLabelsResponse(
                address=address.address,
                labels=[
                    data.AddressLabelResponse(
                        label=label.label, label_data=label.label_data
                    )
                    for label in labels_obj
                ],
            )
        )

    return addresses_response
