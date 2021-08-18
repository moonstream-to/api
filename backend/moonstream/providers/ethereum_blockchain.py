from dataclasses import dataclass, field
import logging
from typing import cast, Dict, Any, List, Optional, Tuple

from bugout.app import Bugout
from bugout.data import BugoutResource

from moonstreamdb.models import (
    EthereumBlock,
    EthereumTransaction,
)
from sqlalchemy import or_, and_, text
from sqlalchemy.orm import Session, Query

from .. import data
from ..settings import DEFAULT_STREAM_TIMEINTERVAL
from ..stream_queries import StreamQuery


logger = logging.getLogger(__name__)


event_type = "ethereum_blockchain"


def validate_subscription(
    subscription_resource_data: data.SubscriptionResourceData,
) -> Tuple[bool, List[str]]:
    """
    Checks that the subscription represents a valid subscription to an Ethereum address.

    NOTE: Currently, this function only checks that the address is a nonempty string.
    """
    errors: List[str] = []
    if subscription_resource_data.address == "":
        errors.append("address is empty")

    if subscription_resource_data.subscription_type_id != event_type:
        errors.append(
            f"Invalid subscription_type ({subscription_resource_data.subscription_type_id}). Expected: {event_type}."
        )

    if errors:
        return False, errors
    return True, errors


@dataclass
class Filters:
    """
    ethereum_blockchain event filters act as a disjunction over queries specifying a from address
    or a to address.
    """

    from_addresses: List[str] = field(default_factory=list)
    to_addresses: List[str] = field(default_factory=list)


def default_filters(subscriptions: List[BugoutResource]) -> List[str]:
    """
    Default filter strings for the given list of subscriptions.
    """
    filters = []
    for subscription in subscriptions:
        subscription_address = subscription.resource_data.get("address")
        if subscription_address is not None:
            filters.append(cast(str, subscription_address))
        else:
            logger.warn(
                f"Could not find subscription address for subscription with resource id: {subscription.id}"
            )
    return filters


def parse_filters(filters: List[str]) -> Filters:
    """
    Passes raw filter strings into a Filters object which is used to construct a database query
    for ethereum transactions.

    Filter syntax is:
    - "from:<address>" - specifies that we want to include all transactions with "<address>" as a source
    - "to:<address>" - specifies that we want to include all transactions with "<address>" as a destination
    - "<address>" - specifies that we want to include all transactions with "<address>" as a source AND all transactions with "<address>" as a destination
    """
    parsed_filters = Filters()

    from_slice_start = len("from:")
    to_slice_start = len("to:")

    for raw_filter in filters:
        if raw_filter.startswith("from:"):
            parsed_filters.from_addresses.append(raw_filter[from_slice_start:])
        elif raw_filter.startswith("to:"):
            parsed_filters.to_addresses.append(raw_filter[to_slice_start:])
        else:
            parsed_filters.from_addresses.append(raw_filter)
            parsed_filters.to_addresses.append(raw_filter)

    return parsed_filters


def query_ethereum_transactions(
    db_session: Session, stream_boundary: data.StreamBoundary, parsed_filters: Filters
) -> Query:
    """
    Builds a database query for Ethereum transactions that occurred within the window of time that
    the given stream_boundary represents and satisfying the constraints of parsed_filters.
    """
    query = db_session.query(
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
    ).join(
        EthereumBlock, EthereumTransaction.block_number == EthereumBlock.block_number
    )

    if stream_boundary.include_start:
        query = query.filter(EthereumBlock.timestamp >= stream_boundary.start_time)
    else:
        query = query.filter(EthereumBlock.timestamp > stream_boundary.start_time)

    if stream_boundary.end_time is not None:
        if stream_boundary.include_end:
            query = query.filter(EthereumBlock.timestamp <= stream_boundary.end_time)
        else:
            query = query.filter(EthereumBlock.timestamp <= stream_boundary.end_time)

    # We want to take a big disjunction (OR) over ALL the filters, be they on "from" address or "to" address
    address_clauses = [
        EthereumTransaction.from_address == address
        for address in parsed_filters.from_addresses
    ] + [
        EthereumTransaction.to_address == address
        for address in parsed_filters.to_addresses
    ]
    if address_clauses:
        query = query.filter(or_(*address_clauses))

    return query


def ethereum_transaction_event(row: Tuple) -> data.Event:
    """
    Parses a result from the result set of a database query for Ethereum transactions with block timestamp
    into an Event object.
    """
    (
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
    ) = row
    return data.Event(
        event_type=event_type,
        event_timestamp=timestamp,
        event_data={
            "hash": hash,
            "block_number": block_number,
            "from": from_address,
            "to": to_address,
            "gas": gas,
            "gas_price": gas_price,
            "input": input,
            "nonce": nonce,
            "value": value,
        },
    )


def get_events(
    db_session: Session,
    bugout_client: Bugout,
    data_journal_id: str,
    data_access_token: str,
    stream_boundary: data.StreamBoundary,
    filters: List[str],
) -> Tuple[data.StreamBoundary, List[data.Event]]:
    """
    Returns ethereum_blockchain events for the given addresses in the time period represented
    by stream_boundary.
    """
    parsed_filters = parse_filters(filters)

    ethereum_transactions = query_ethereum_transactions(
        db_session, stream_boundary, parsed_filters
    )

    ethereum_transactions = ethereum_transactions.order_by(text("timestamp desc"))

    events: List[data.Event] = [
        ethereum_transaction_event(row) for row in ethereum_transactions
    ]

    if (stream_boundary.end_time is None) and events:
        stream_boundary.end_time = events[0].event_timestamp
        stream_boundary.include_end = True

    return stream_boundary, events


def latest_events(
    db_session: Session,
    bugout_client: Bugout,
    data_journal_id: str,
    data_access_token: str,
    filters: List[str],
    num_events: int,
) -> List[data.Event]:
    """
    Returns the num_events latest events from the current provider, subject to the constraints imposed
    by the given filters.
    """
    assert num_events > 0, f"num_events ({num_events}) should be positive."

    stream_boundary = data.StreamBoundary(
        start_time=0, include_start=True, end_time=None, include_end=False
    )
    parsed_filters = parse_filters(filters)
    ethereum_transactions = (
        query_ethereum_transactions(db_session, stream_boundary, parsed_filters)
        .order_by(text("timestamp desc"))
        .limit(num_events)
    )

    return [ethereum_transaction_event(row) for row in ethereum_transactions]


def next_event(
    db_session: Session,
    bugout_client: Bugout,
    data_journal_id: str,
    data_access_token: str,
    stream_boundary: data.StreamBoundary,
    filters: List[str],
) -> Optional[data.Event]:
    assert (
        stream_boundary.end_time is not None
    ), "Cannot return next event for up-to-date stream boundary"
    next_stream_boundary = data.StreamBoundary(
        start_time=stream_boundary.end_time,
        include_start=(not stream_boundary.include_end),
        end_time=None,
        include_end=False,
    )
    parsed_filters = parse_filters(filters)
    maybe_ethereum_transaction = (
        query_ethereum_transactions(db_session, next_stream_boundary, parsed_filters)
        .order_by(text("timestamp asc"))
        .limit(1)
        .one_or_none()
    )

    if maybe_ethereum_transaction is None:
        return None
    return ethereum_transaction_event(maybe_ethereum_transaction)


def previous_event(
    db_session: Session,
    bugout_client: Bugout,
    data_journal_id: str,
    data_access_token: str,
    stream_boundary: data.StreamBoundary,
    filters: List[str],
) -> Optional[data.Event]:
    assert (
        stream_boundary.start_time != 0
    ), "Cannot return previous event for stream starting at time 0"
    previous_stream_boundary = data.StreamBoundary(
        start_time=0,
        include_start=True,
        end_time=stream_boundary.start_time,
        include_end=(not stream_boundary.include_start),
    )
    parsed_filters = parse_filters(filters)
    maybe_ethereum_transaction = (
        query_ethereum_transactions(
            db_session, previous_stream_boundary, parsed_filters
        )
        .order_by(text("timestamp desc"))
        .limit(1)
        .one_or_none()
    )

    if maybe_ethereum_transaction is None:
        return None
    return ethereum_transaction_event(maybe_ethereum_transaction)


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

        next_transaction = next_transaction.one_or_none()

        if next_transaction:
            boundaries.next_event_time = next_transaction[-1]
        else:
            boundaries.next_event_time = None

    if boundaries.start_time:
        ethereum_transactions = ethereum_transactions.filter(
            include_or_not_greater(
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
        ).one_or_none()

        if previous_transaction:
            boundaries.previous_event_time = previous_transaction[-1]
        else:
            boundaries.previous_event_time = None

    response = []
    for (
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
    ) in ethereum_transactions:

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

    return data.EthereumTransactionResponse(stream=response, boundaries=boundaries)


def include_or_not_greater(value1, include, value2):
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
