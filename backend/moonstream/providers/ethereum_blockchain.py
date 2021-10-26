import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, cast

from bugout.app import Bugout
from bugout.data import BugoutResource
from moonstreamdb.models import EthereumBlock, EthereumLabel, EthereumTransaction
from sqlalchemy import and_, or_, text
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql.functions import user

from .. import data
from ..stream_boundaries import validate_stream_boundary
from ..stream_queries import StreamQuery

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


event_type = "ethereum_blockchain"
allowed_tags = ["tag:erc721"]

description = f"""Event provider for transactions from the Ethereum blockchain.

To restrict your queries to this provider, add a filter of \"type:{event_type}\" to your query (query parameter: \"q\") on the /streams endpoint."""

default_time_interval_seconds: int = 5 * 60

# 200 transactions per block, 4 blocks per minute.
estimated_events_per_time_interval: float = 5 * 800


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


def stream_boundary_validator(stream_boundary: data.StreamBoundary) -> None:
    """
    Stream boundary validator for the ethereum_blockchain event provider.

    Checks that stream boundaries do not exceed periods of greater than 2 hours.

    Raises an error for invalid stream boundaries, else returns None.
    """
    valid_period_seconds = 2 * 60 * 60
    validate_stream_boundary(
        stream_boundary, valid_period_seconds, raise_when_invalid=True
    )


@dataclass
class Filters:
    """
    ethereum_blockchain event filters act as a disjunction over queries specifying a from address
    or a to address.
    """

    from_addresses: List[str] = field(default_factory=list)
    to_addresses: List[str] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)


def default_filters(subscriptions: List[BugoutResource]) -> Filters:
    """
    Default filter strings for the given list of subscriptions.
    """
    filters = Filters()
    for subscription in subscriptions:
        subscription_address = cast(
            Optional[str], subscription.resource_data.get("address")
        )
        if subscription_address is not None:
            if subscription_address in allowed_tags:
                filters.labels.append(subscription_address.split(":")[1])
            else:
                filters.from_addresses.append(subscription_address)
                filters.to_addresses.append(subscription_address)
        else:
            logger.warn(
                f"Could not find subscription address for subscription with resource id: {subscription.id}"
            )
    return filters


def parse_filters(
    query: StreamQuery, user_subscriptions: Dict[str, List[BugoutResource]]
) -> Optional[Filters]:
    """
    Passes raw filter strings into a Filters object which is used to construct a database query
    for ethereum transactions.

    Filter syntax is:
    - "from:<address>" - specifies that we want to include all transactions with "<address>" as a source
    - "to:<address>" - specifies that we want to include all transactions with "<address>" as a destination
    - "<address>" - specifies that we want to include all transactions with "<address>" as a source AND all transactions with "<address>" as a destination

    If the given StreamQuery induces filters on this provider, returns those filters. Otherwise, returns
    None indicating that the StreamQuery does not require any data from this provider.
    """
    if query.subscription_types and not any(
        subtype == event_type for subtype in query.subscription_types
    ):
        return None

    provider_subscriptions = user_subscriptions.get(event_type)

    # If the user has no subscriptions to this event type, we do not have to return any data!
    if not provider_subscriptions:
        return None
    parsed_filters = default_filters(provider_subscriptions)

    from_prefix_length = len("from:")
    to_prefix_length = len("to:")

    subscribed_addresses = {
        subscription.resource_data.get("address")
        for subscription in provider_subscriptions
        if subscription.resource_data.get("address") is not None
    }

    if query.subscriptions:
        parsed_filters.from_addresses = []
        parsed_filters.to_addresses = []
        for provider_type, raw_filter in query.subscriptions:
            if provider_type != event_type:
                continue

            if raw_filter.startswith("from:"):
                address = raw_filter[from_prefix_length:]
                if address in subscribed_addresses:
                    parsed_filters.from_addresses.append(address)
            elif raw_filter.startswith("to:"):
                address = raw_filter[to_prefix_length:]
                if address in subscribed_addresses:
                    parsed_filters.to_addresses.append(address)
            else:
                address = raw_filter
                if address in subscribed_addresses:
                    parsed_filters.from_addresses.append(address)
                    parsed_filters.to_addresses.append(address)

    if not (
        parsed_filters.from_addresses
        or parsed_filters.to_addresses
        or parsed_filters.labels
    ):
        return None

    return parsed_filters


def query_ethereum_transactions(
    db_session: Session,
    stream_boundary: data.StreamBoundary,
    parsed_filters: Filters,
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
        EthereumBlock,
        EthereumTransaction.block_number == EthereumBlock.block_number,
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
    address_clauses = []

    address_clauses.extend(
        [
            EthereumTransaction.from_address == address
            for address in parsed_filters.from_addresses
        ]
        + [
            EthereumTransaction.to_address == address
            for address in parsed_filters.to_addresses
        ]
    )

    labels_clause = []

    if parsed_filters.labels:
        label_clause = (
            db_session.query(EthereumLabel)
            .filter(
                or_(
                    *[
                        EthereumLabel.label.contains(label)
                        for label in list(set(parsed_filters.labels))
                    ]
                )
            )
            .exists()
        )
        labels_clause.append(label_clause)

    subscriptions_clause = address_clauses + labels_clause

    if subscriptions_clause:
        query = query.filter(or_(*subscriptions_clause))

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
    query: StreamQuery,
    user_subscriptions: Dict[str, List[BugoutResource]],
) -> Optional[Tuple[data.StreamBoundary, List[data.Event]]]:
    """
    Returns ethereum_blockchain events for the given addresses in the time period represented
    by stream_boundary.

    If the query does not require any data from this provider, returns None.
    """
    stream_boundary_validator(stream_boundary)

    parsed_filters = parse_filters(query, user_subscriptions)
    if parsed_filters is None:
        return None

    ethereum_transactions = query_ethereum_transactions(
        db_session, stream_boundary, parsed_filters
    )

    ethereum_transactions = ethereum_transactions.order_by(text("timestamp desc"))

    # TODO(zomglings): Catch the operational error denoting that the statement timed out here
    # and wrap it in an error that tells the API to return the appropriate 400 response. Currently,
    # when the statement times out, the API returns a 500 status code to the client, which doesn't
    # do anything to help them get data from teh backend.
    # The error message on the API side when the statement times out:
    # > sqlalchemy.exc.OperationalError: (psycopg2.errors.QueryCanceled) canceling statement due to statement timeout
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
    query: StreamQuery,
    num_events: int,
    user_subscriptions: Dict[str, List[BugoutResource]],
) -> Optional[List[data.Event]]:
    """
    Returns the num_events latest events from the current provider, subject to the constraints imposed
    by the given filters.

    If the query does not require any data from this provider, returns None.
    """
    assert num_events > 0, f"num_events ({num_events}) should be positive."

    stream_boundary = data.StreamBoundary(
        start_time=0, include_start=True, end_time=None, include_end=False
    )
    parsed_filters = parse_filters(query, user_subscriptions)
    if parsed_filters is None:
        return None
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
    query: StreamQuery,
    user_subscriptions: Dict[str, List[BugoutResource]],
) -> Optional[data.Event]:
    """
    Returns the earliest event occuring after the given stream boundary corresponding to the given
    query from this provider.

    If the query does not require any data from this provider, returns None.
    """
    assert (
        stream_boundary.end_time is not None
    ), "Cannot return next event for up-to-date stream boundary"
    next_stream_boundary = data.StreamBoundary(
        start_time=stream_boundary.end_time,
        include_start=(not stream_boundary.include_end),
        end_time=None,
        include_end=False,
    )
    parsed_filters = parse_filters(query, user_subscriptions)
    if parsed_filters is None:
        return None

    maybe_ethereum_transaction = (
        query_ethereum_transactions(db_session, next_stream_boundary, parsed_filters)
        .order_by(text("timestamp asc"))
        .limit(1)
    ).one_or_none()

    if maybe_ethereum_transaction is None:
        return None
    return ethereum_transaction_event(maybe_ethereum_transaction)


def previous_event(
    db_session: Session,
    bugout_client: Bugout,
    data_journal_id: str,
    data_access_token: str,
    stream_boundary: data.StreamBoundary,
    query: StreamQuery,
    user_subscriptions: Dict[str, List[BugoutResource]],
) -> Optional[data.Event]:
    """
    Returns the latest event occuring before the given stream boundary corresponding to the given
    query from this provider.

    If the query does not require any data from this provider, returns None.
    """
    assert (
        stream_boundary.start_time != 0
    ), "Cannot return previous event for stream starting at time 0"
    previous_stream_boundary = data.StreamBoundary(
        start_time=0,
        include_start=True,
        end_time=stream_boundary.start_time,
        include_end=(not stream_boundary.include_start),
    )
    parsed_filters = parse_filters(query, user_subscriptions)
    if parsed_filters is None:
        return None
    maybe_ethereum_transaction = (
        query_ethereum_transactions(
            db_session, previous_stream_boundary, parsed_filters
        )
        .order_by(text("timestamp desc"))
        .limit(1)
    ).one_or_none()
    if maybe_ethereum_transaction is None:
        return None
    return ethereum_transaction_event(maybe_ethereum_transaction)
