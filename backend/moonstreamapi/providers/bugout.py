"""
Event providers powered by Bugout journals.
"""
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from bugout.app import Bugout
from bugout.data import BugoutResource, BugoutSearchResult
from bugout.journal import SearchOrder
from dateutil.parser import isoparse
from dateutil.tz import UTC
from sqlalchemy.orm import Session

from .. import data
from ..settings import HUMBUG_TXPOOL_CLIENT_ID
from ..stream_queries import StreamQuery

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)

allowed_tags = ["tag:erc721"]


class BugoutEventProviderError(Exception):
    """
    Catch-all error for BugoutEventProvider instances.
    """


class BugoutEventProvider:
    """
    Provides events (specified by a conjunction of tags) from a Bugout journal.
    """

    def __init__(
        self,
        event_type: str,
        description: str,
        default_time_interval_seconds: int,
        estimated_events_per_time_interval: float,
        tags: Optional[List[str]] = None,
        batch_size: int = 100,
        timeout: float = 30.0,
    ):
        """
        Args:
        - event_type: Name of event this instance provides
        - tags: Tags which define events that this provider works with
        - batch_size: Number of events to read from journal at a time
        - timeout: Request timeout for Bugout requests
        """
        self.event_type = event_type
        self.description = description
        self.default_time_interval_seconds = default_time_interval_seconds
        self.estimated_events_per_time_interval = estimated_events_per_time_interval
        self.batch_size = batch_size
        self.timeout = timeout
        if tags is None:
            tags = []
        self.tags: List[str] = tags
        self.query = [f"#{tag}" for tag in self.tags]

    def validate_subscription(
        self, subscription_resource_data: data.SubscriptionResourceData
    ) -> bool:
        """
        This implementation is maximally permissive and returns True for all subscriptions as long as
        their subscription_type_id is the configured event_type.
        Subclasses of this provider can impose stricter criteria on submissions to the relevant event types.
        """
        return subscription_resource_data.subscription_type_id == self.event_type

    def entry_event(self, entry: BugoutSearchResult) -> data.Event:
        """
        Load an event from a Bugout journal entry. Assumes that the entry content is a JSON string
        with no additional markdown formatting.
        """
        event_data = {}
        if entry.content is not None:
            event_data = json.loads(entry.content)
        created_at_dt = isoparse(entry.created_at)
        created_at_dt = created_at_dt.replace(tzinfo=UTC)
        created_at = int(created_at_dt.timestamp())
        return data.Event(
            event_type=self.event_type,
            event_timestamp=created_at,
            event_data=event_data,
        )

    def parse_filters(
        self, query: StreamQuery, user_subscriptions: Dict[str, List[BugoutResource]]
    ) -> Optional[List[str]]:
        """
        Subclasses can provide additional constraints to apply to the journal search.

        If None is returned, signals that no data should be returned from the provider at all.
        """
        is_query_constrained = query.subscription_types or query.subscriptions
        relevant_subscriptions = user_subscriptions.get(self.event_type)

        if (
            is_query_constrained and self.event_type not in query.subscription_types
        ) or not relevant_subscriptions:
            return None
        return []

    def get_events(
        self,
        db_session: Session,
        bugout_client: Bugout,
        data_journal_id: str,
        data_access_token: str,
        stream_boundary: data.StreamBoundary,
        query: StreamQuery,
        user_subscriptions: Dict[str, List[BugoutResource]],
    ) -> Optional[Tuple[data.StreamBoundary, List[data.Event]]]:
        """
        Uses journal search endpoint to retrieve events for the given stream boundary and query constraints
        from the connected journal.
        """
        additional_constraints = self.parse_filters(query, user_subscriptions)
        if additional_constraints is None:
            return None

        time_constraints: List[str] = []
        if stream_boundary.start_time > 0:
            start_time = datetime.utcfromtimestamp(
                stream_boundary.start_time
            ).isoformat()
            operator = ">"
            if stream_boundary.include_start:
                operator = ">="
            time_constraints.append(f"created_at:{operator}{start_time}")

        if stream_boundary.end_time is not None:
            end_time = datetime.utcfromtimestamp(stream_boundary.end_time).isoformat()
            operator = "<"
            if stream_boundary.include_end:
                operator = "<="
            time_constraints.append(f"created_at:{operator}{end_time}")

        final_query = " ".join(self.query + time_constraints + additional_constraints)
        events: List[data.Event] = []
        offset: Optional[int] = 0
        while offset is not None:
            search_results = bugout_client.search(
                data_access_token,
                data_journal_id,
                final_query,
                limit=self.batch_size,
                offset=offset,
                content=True,
                timeout=self.timeout,
                order=SearchOrder.DESCENDING,
            )
            events.extend([self.entry_event(entry) for entry in search_results.results])
            offset = search_results.next_offset

        return stream_boundary, events

    def latest_events(
        self,
        db_session: Session,
        bugout_client: Bugout,
        data_journal_id: str,
        data_access_token: str,
        query: StreamQuery,
        num_events: int,
        user_subscriptions: Dict[str, List[BugoutResource]],
    ) -> Optional[List[data.Event]]:
        """
        Gets the latest events corresponding to this provider from the given journal.
        """
        additional_constraints = self.parse_filters(query, user_subscriptions)
        if additional_constraints is None:
            return None

        if num_events > self.batch_size:
            raise BugoutEventProviderError(
                f"You requested too many events: event_type={self.event_type}, num_events={num_events}, limit={self.batch_size}"
            )

        final_query = " ".join(self.query + additional_constraints)
        search_results = bugout_client.search(
            data_access_token,
            data_journal_id,
            final_query,
            limit=num_events,
            content=True,
            timeout=self.timeout,
            order=SearchOrder.DESCENDING,
        )
        return [self.entry_event(entry) for entry in search_results.results]

    def next_event(
        self,
        db_session: Session,
        bugout_client: Bugout,
        data_journal_id: str,
        data_access_token: str,
        stream_boundary: data.StreamBoundary,
        query: StreamQuery,
        user_subscriptions: Dict[str, List[BugoutResource]],
    ) -> Optional[data.Event]:
        """
        Get the earliest event that occurred after the time window represented by the given stream boundary.
        """
        additional_constraints = self.parse_filters(query, user_subscriptions)
        if additional_constraints is None:
            return None

        if stream_boundary.end_time is None:
            raise BugoutEventProviderError(
                "Cannot return next event for a stream boundary which is current."
            )
        end_time = datetime.utcfromtimestamp(stream_boundary.end_time).isoformat()
        operator = ">="
        if stream_boundary.include_end:
            operator = ">"
        additional_constraints.append(f"created_at:{operator}{end_time}")

        final_query = " ".join(self.query + additional_constraints)
        search_results = bugout_client.search(
            data_access_token,
            data_journal_id,
            final_query,
            limit=1,
            content=True,
            timeout=self.timeout,
            order=SearchOrder.ASCENDING,
        )
        if not search_results.results:
            return None
        return self.entry_event(search_results.results[0])

    def previous_event(
        self,
        db_session: Session,
        bugout_client: Bugout,
        data_journal_id: str,
        data_access_token: str,
        stream_boundary: data.StreamBoundary,
        query: StreamQuery,
        user_subscriptions: Dict[str, List[BugoutResource]],
    ) -> Optional[data.Event]:
        """
        Get the latest event that occurred before the time window represented by the given stream boundary.
        """
        additional_constraints = self.parse_filters(query, user_subscriptions)
        if additional_constraints is None:
            return None

        if stream_boundary.start_time == 0:
            raise BugoutEventProviderError(
                "Cannot return previous event for a stream boundary starting at the beginning of time."
            )
        start_time = datetime.utcfromtimestamp(stream_boundary.start_time).isoformat()
        operator = "<="
        if stream_boundary.include_start:
            operator = "<"
        additional_constraints.append(f"created_at:{operator}{start_time}")

        final_query = " ".join(self.query + additional_constraints)
        search_results = bugout_client.search(
            data_access_token,
            data_journal_id,
            final_query,
            limit=1,
            content=True,
            timeout=self.timeout,
            order=SearchOrder.DESCENDING,
        )
        if not search_results.results:
            return None
        return self.entry_event(search_results.results[0])


class EthereumTXPoolProvider(BugoutEventProvider):
    def __init__(
        self,
        event_type: str,
        description: str,
        default_time_interval_seconds: int,
        estimated_events_per_time_interval: float,
        tags: Optional[List[str]] = None,
        batch_size: int = 100,
        timeout: float = 30.0,
    ):

        super().__init__(
            event_type=event_type,
            description=description,
            default_time_interval_seconds=default_time_interval_seconds,
            estimated_events_per_time_interval=estimated_events_per_time_interval,
            tags=tags,
            batch_size=batch_size,
            timeout=timeout,
        )

    def parse_filters(
        self, query: StreamQuery, user_subscriptions: Dict[str, List[BugoutResource]]
    ) -> Optional[List[str]]:

        is_query_constrained = query.subscription_types or query.subscriptions
        relevant_subscriptions = user_subscriptions.get(self.event_type)

        if (
            is_query_constrained and self.event_type not in query.subscription_types
        ) or not relevant_subscriptions:
            return None
        addresses = [
            subscription.resource_data["address"]
            for subscription in relevant_subscriptions
        ]
        subscriptions_filters = []
        for address in addresses:
            if address in allowed_tags:
                subscriptions_filters.append(address)
            else:
                subscriptions_filters.extend(
                    [f"?#from_address:{address}", f"?#to_address:{address}"]
                )

        return subscriptions_filters


whalewatch_description = """Event provider for Ethereum whale watch.

Shows the top 10 addresses active on the Ethereum blockchain over the last hour in the following categories:
1. Number of transactions sent
2. Number of transactions received
3. Amount (in WEI) sent
4. Amount (in WEI) received

To restrict your queries to this provider, add a filter of \"type:ethereum_whalewatch\" to your query (query parameter: \"q\") on the /streams endpoint."""
ethereum_whalewatch_provider = BugoutEventProvider(
    event_type="ethereum_whalewatch",
    description=whalewatch_description,
    default_time_interval_seconds=310,
    estimated_events_per_time_interval=1,
    tags=["crawl_type:ethereum_trending"],
)

polygon_whalewatch_provider = BugoutEventProvider(
    event_type="polygon_whalewatch",
    description=whalewatch_description,
    default_time_interval_seconds=310,
    estimated_events_per_time_interval=1,
    tags=["crawl_type:polygon_trending"],
)

ethereum_txpool_description = """Event provider for Ethereum transaction pool.

Shows the latest events (from the previous hour) in the Ethereum transaction pool.

To restrict your queries to this provider, add a filter of \"type:ethereum_txpool\" to your query (query parameter: \"q\") on the /streams endpoint."""
ethereum_txpool_provider = EthereumTXPoolProvider(
    event_type="ethereum_txpool",
    description=ethereum_txpool_description,
    default_time_interval_seconds=5,
    estimated_events_per_time_interval=50,
    tags=[f"client:{HUMBUG_TXPOOL_CLIENT_ID}"],
)
