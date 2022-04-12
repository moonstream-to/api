"""
Maps provider interface over all available providers.

Available providers are exposed through the `event_providers` dictionary.

Exposes all the standard event provider methods:
- get_events
- latest_events
- next_event
- previous_event

In addition to their standard arguments, adds the following arguments to each of these methods:
- `max_threads` - Since the mapper retrieves events from each providers in the background, this allows
the caller to specify how many threads they want to make available to the background executor. This
can be set to None, in which case it uses the Python default behaviour for the max_workers=None to
concurrent.futures.ThreadPoolExecutor. (Default: None)
- result_timeout - A float representing the number of seconds to wait for the background workers to get
events from the individual providers. (Default: 30.0)
- raise_on_error - Set this to True to raise an error if any of the individual event providers experiences an
error fulfilling its method. If set to False, ignores event providers which failed and still tries to
return data to the caller. (Default: False)
- sort_events - Set this to True to sort the events that come in from different providers. Set it to False
if the order does not matter and you would rather emphasize speed. Only available for method which involve
lists of events. (Default: True)
"""

import logging
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Dict, List, Optional, Tuple

from bugout.app import Bugout
from bugout.data import BugoutResource
from sqlalchemy.orm import Session

from .. import data
from ..stream_queries import StreamQuery
from . import bugout, moonworm_provider, transactions

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


class ReceivingEventsException(Exception):
    """
    Raised when error occurs during receiving events from provider.
    """


event_providers: Dict[str, Any] = {
    moonworm_provider.EthereumMoonwormProvider.event_type: moonworm_provider.EthereumMoonwormProvider,
    moonworm_provider.PolygonMoonwormProvider.event_type: moonworm_provider.PolygonMoonwormProvider,
    transactions.EthereumTransactions.event_type: transactions.EthereumTransactions,
    transactions.PolygonTransactions.event_type: transactions.PolygonTransactions,
    bugout.polygon_whalewatch_provider.event_type: bugout.polygon_whalewatch_provider,
    bugout.ethereum_txpool_provider.event_type: bugout.ethereum_txpool_provider,
    bugout.ethereum_whalewatch_provider.event_type: bugout.ethereum_whalewatch_provider,
    bugout.ethereum_txpool_provider.event_type: bugout.ethereum_txpool_provider,
}


def get_events(
    db_session: Session,
    bugout_client: Bugout,
    data_journal_id: str,
    data_access_token: str,
    stream_boundary: data.StreamBoundary,
    query: StreamQuery,
    user_subscriptions: Dict[str, List[BugoutResource]],
    max_threads: Optional[int] = None,
    result_timeout: float = 30.0,
    raise_on_error: bool = False,
    sort_events: bool = True,
) -> Tuple[data.StreamBoundary, List[data.Event]]:
    """
    Gets events from all providers and sends them back with the stream boundary.
    """

    futures: Dict[str, Future] = {}
    with ThreadPoolExecutor(
        max_workers=max_threads, thread_name_prefix="event_providers_"
    ) as executor:
        # Filter our not queried event_types
        event_providers_filtered = {
            key: value
            for (key, value) in event_providers.items()
            if value.event_type in query.subscription_types
        }

        for provider_name, provider in event_providers_filtered.items():
            futures[provider_name] = executor.submit(
                provider.get_events,
                db_session,
                bugout_client,
                data_journal_id,
                data_access_token,
                stream_boundary,
                query,
                user_subscriptions,
            )

    results: Dict[str, Tuple[data.StreamBoundary, List[data.Event]]] = {}
    for provider_name, future in futures.items():
        try:
            result = future.result(timeout=result_timeout)
            if result is not None:
                results[provider_name] = result
        except Exception as e:
            if not raise_on_error:
                logger.warn(
                    f"Error receiving events from provider: {provider_name}:\n{repr(e)}"
                )
            else:
                raise ReceivingEventsException(e)

    stream_boundary = [boundary for boundary, _ in results.values()][0]
    events = [event for _, event_list in results.values() for event in event_list]
    if sort_events:
        # If stream_boundary time was reversed, so do not reverse by timestamp,
        # it is already in correct oreder
        events.sort(
            key=lambda event: event.event_timestamp,
            reverse=not stream_boundary.reversed_time,
        )

    return (stream_boundary, events)


def latest_events(
    db_session: Session,
    bugout_client: Bugout,
    data_journal_id: str,
    data_access_token: str,
    query: StreamQuery,
    num_events: int,
    user_subscriptions: Dict[str, List[BugoutResource]],
    max_threads: Optional[int] = None,
    result_timeout: float = 30.0,
    raise_on_error: bool = False,
    sort_events: bool = True,
) -> List[data.Event]:
    """
    Gets num_events most recent events from all providers, compiles them into a single list, and
    returns them to the caller.

    NOTE: Unlike simple event providers, the interpretation of num_events here is that we return num_event
    events per individual event provider!
    """

    futures: Dict[str, Future] = {}
    with ThreadPoolExecutor(
        max_workers=max_threads, thread_name_prefix="event_providers_"
    ) as executor:
        # Filter our not queried event_types
        event_providers_filtered = {
            key: value
            for (key, value) in event_providers.items()
            if value.event_type in query.subscription_types
        }

        for provider_name, provider in event_providers_filtered.items():
            futures[provider_name] = executor.submit(
                provider.latest_events,
                db_session,
                bugout_client,
                data_journal_id,
                data_access_token,
                query,
                num_events,
                user_subscriptions,
            )

    results: Dict[str, List[data.Event]] = {}
    for provider_name, future in futures.items():
        try:
            result = future.result(timeout=result_timeout)
            if result is not None:
                results[provider_name] = result
        except Exception as e:
            if not raise_on_error:
                logger.warn(
                    f"Error receiving events from provider: {provider_name}:\n{repr(e)}"
                )
            else:
                raise ReceivingEventsException(e)
    events = [event for event_list in results.values() for event in event_list]
    if sort_events:
        events.sort(key=lambda event: event.event_timestamp, reverse=True)

    return events


def next_event(
    db_session: Session,
    bugout_client: Bugout,
    data_journal_id: str,
    data_access_token: str,
    stream_boundary: data.StreamBoundary,
    query: StreamQuery,
    user_subscriptions: Dict[str, List[BugoutResource]],
    max_threads: Optional[int] = None,
    result_timeout: float = 30.0,
    raise_on_error: bool = False,
) -> Optional[data.Event]:
    """
    Get earliest event after stream boundary across all available providers.
    """

    futures: Dict[str, Future] = {}
    with ThreadPoolExecutor(
        max_workers=max_threads, thread_name_prefix="event_providers_"
    ) as executor:
        # Filter our not queried event_types
        event_providers_filtered = {
            key: value
            for (key, value) in event_providers.items()
            if value.event_type in query.subscription_types
        }

        for provider_name, provider in event_providers_filtered.items():
            futures[provider_name] = executor.submit(
                provider.next_event,
                db_session,
                bugout_client,
                data_journal_id,
                data_access_token,
                stream_boundary,
                query,
                user_subscriptions,
            )

    results: Dict[str, data.Event] = {}
    for provider_name, future in futures.items():
        try:
            result = future.result(timeout=result_timeout)
            if result is not None:
                results[provider_name] = result
        except Exception as e:
            if not raise_on_error:
                logger.warn(
                    f"Error receiving events from provider: {provider_name}:\n{repr(e)}"
                )
            else:
                raise ReceivingEventsException(e)

    event: Optional[data.Event] = None
    for candidate in results.values():
        if event is None:
            event = candidate
        elif event.event_timestamp > candidate.event_timestamp:
            event = candidate

    return event


def previous_event(
    db_session: Session,
    bugout_client: Bugout,
    data_journal_id: str,
    data_access_token: str,
    stream_boundary: data.StreamBoundary,
    query: StreamQuery,
    user_subscriptions: Dict[str, List[BugoutResource]],
    max_threads: Optional[int] = None,
    result_timeout: float = 30.0,
    raise_on_error: bool = False,
) -> Optional[data.Event]:
    """
    Get latest event before stream boundary across all available providers.
    """

    futures: Dict[str, Future] = {}
    with ThreadPoolExecutor(
        max_workers=max_threads, thread_name_prefix="event_providers_"
    ) as executor:
        # Filter our not queried event_types
        event_providers_filtered = {
            key: value
            for (key, value) in event_providers.items()
            if value.event_type in query.subscription_types
        }

        for provider_name, provider in event_providers_filtered.items():
            futures[provider_name] = executor.submit(
                provider.previous_event,
                db_session,
                bugout_client,
                data_journal_id,
                data_access_token,
                stream_boundary,
                query,
                user_subscriptions,
            )

    results: Dict[str, data.Event] = {}
    for provider_name, future in futures.items():
        try:
            result = future.result(timeout=result_timeout)
            if result is not None:
                results[provider_name] = result
        except Exception as e:
            if not raise_on_error:
                logger.warn(
                    f"Error receiving events from provider: {provider_name}:\n{repr(e)}"
                )
            else:
                raise ReceivingEventsException(e)

    event: Optional[data.Event] = None
    for candidate in results.values():
        if event is None:
            event = candidate
        elif event.event_timestamp < candidate.event_timestamp:
            event = candidate

    return event
