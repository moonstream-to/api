"""
Event providers powered by Bugout journals.
"""
from datetime import datetime
import json
import logging
import time
from typing import Dict, List, Optional, Tuple

from bugout.app import Bugout
from bugout.data import BugoutResource, BugoutSearchResult
from bugout.journal import SearchOrder
from dateutil.parser import parse
from sqlalchemy.orm import Session

from .. import data
from ..stream_queries import StreamQuery


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


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
        created_at = int(parse(entry.created_at).timestamp())
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
            operator = ">"
            if stream_boundary.include_start:
                operator = ">="
            time_constraints.append(
                f"created_at:{operator}{stream_boundary.start_time}"
            )

        if stream_boundary.end_time is not None:
            operator = "<"
            if stream_boundary.include_end:
                operator = "<="
            time_constraints.append(f"created_at:{operator}{stream_boundary.end_time}")

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
        operator = ">="
        if stream_boundary.include_end:
            operator = ">"
        additional_constraints.append(
            f"created_at:{operator}{stream_boundary.end_time}"
        )

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
        operator = "<="
        if stream_boundary.include_start:
            operator = "<"
        additional_constraints.append(
            f"created_at:{operator}{stream_boundary.start_time}"
        )

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


whalewatch_provider = BugoutEventProvider(
    event_type="ethereum_whalewatch", tags=["crawl_type:ethereum_trending"]
)
