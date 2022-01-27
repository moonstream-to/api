from array import array
from ast import operator
from ctypes import Union
from email.policy import default
import logging
from dataclasses import dataclass, field
from multiprocessing import Condition
from re import A, L
from tkinter.messagebox import NO
from typing import Any, Dict, List, Optional, Tuple
from black import patch_click

from bugout.app import Bugout
from bugout.data import BugoutResource
from moonstreamdb.blockchain import AvailableBlockchainType, get_label_model
from sqlalchemy import (
    and_,
    desc,
    or_,
    select,
    text,
    func,
    types,
    cast,
    String,
    Integer,
    Numeric,
)
from sqlalchemy.orm import Query, Session, query_expression
from sqlalchemy.sql.expression import label

from .. import data
from ..stream_boundaries import validate_stream_boundary
from ..stream_queries import StreamQuery

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


ethereum_event_type = "ethereum_blockchain"
polygon_event_type = "polygon_blockchain"
allowed_tags = ["tag:erc721"]

description = f"""Event provider for transactions from the Ethereum blockchain.

To restrict your queries to this provider, add a filter of \"type:{ethereum_event_type}\{polygon_event_type}\" to your query (query parameter: \"q\") on the /streams endpoint."""

default_time_interval_seconds: int = 5 * 60

# 200 transactions per block, 4 blocks per minute.
estimated_events_per_time_interval: float = 5 * 800


class MoonwormProvider:
    def __init__(
        self,
        event_type: str,
        blockchain: AvailableBlockchainType,
        description: str,
        streamboaundary_range_limit: int,
    ):
        self.event_type = event_type
        self.blockchain = blockchain
        self.description = description
        self.valid_period_seconds = streamboaundary_range_limit

    def default_filters(
        self, subscriptions: List[BugoutResource]
    ) -> Tuple[data.EventFilters, List[str]]:
        """
        Default filter strings for the given list of subscriptions.
        """

        addresses = []

        for subscription in subscriptions:
            subscription_address = subscription.resource_data.get("address")
            if subscription_address is not None:
                addresses.append(subscription_address)

            else:
                logger.warn(
                    f"Could not find subscription address for subscription with resource id: {subscription.id}"
                )
        # Add addresses only without filters
        # Predefined query for usual frontend behaivior

        if addresses:

            event_filters = data.EventFilters.parse_obj(
                [
                    {
                        "$map": [
                            {"data.block_number": None},
                            {"data.address": None},
                            {"data.transaction_hash": None},
                            {"data.label_data": None},
                            {"data.block_timestamp": None},
                            {"data.log_index": None},
                            {"data.created_at": None},
                        ]
                    },
                    {"$sort": {"data.block_timestamp": "desc"}},
                    {
                        "$match": {
                            "data.label": "moonworm",
                            "data.address": {"$in": addresses},
                        }
                    },
                ]
            )
        else:

            event_filters = data.EventFilters()

        return event_filters, addresses

    def apply_query_filters(
        self, filters: data.EventFilters, query_filters: StreamQuery
    ):
        """
        Required to implement filters wich depends on procider
        """
        return filters

    def events(self, row: Tuple) -> data.Event:
        """
        Parses a result from the result set of a database query for Ethereum transactions with block timestamp
        into an Event object.
        """
        (
            block_number,
            address,
            transaction_hash,
            label_data,
            block_timestamp,
            log_index,
            created_at,
        ) = row
        return data.Event(
            event_type=self.event_type,
            event_timestamp=block_timestamp,
            event_data={
                "hash": transaction_hash,
                "block_number": block_number,
                "address": address,
                "label_data": label_data,
                "log_index": log_index,
                "created_at": created_at,
            },
        )

    def parse_filters(
        self,
        query: StreamQuery,
        user_subscriptions: Dict[str, List[BugoutResource]],
    ) -> Optional[data.EventFilters]:
        """
        Passes raw filter strings into a Filters object which is used to construct a database query
        for ethereum transactions.
        Right now support only addresses query.
        """

        if query.subscription_types and not any(
            subtype == self.event_type for subtype in query.subscription_types
        ):
            return None

        provider_subscriptions = user_subscriptions.get(self.event_type)

        # If the user has no subscriptions to this event type, we do not have to return any data!
        if not provider_subscriptions:
            return None
        parsed_filters: Any = {}

        if not query.event_filters:
            parsed_filters, addresses = self.default_filters(provider_subscriptions)

            self.apply_query_filters(parsed_filters, query)
            if not (addresses):
                return None

        else:
            parsed_filters = query.event_filters

        return parsed_filters

    def generate_selector(
        self, filter_name: str, label=None
    ):  # filter_condition: Union[str, Dict[str, Any]]):
        """
        Return selector for column or JSONB
        """

        constract_select_column = filter_name.split(".")

        label_model = get_label_model(self.blockchain)

        select = label_model

        for name in constract_select_column:

            if name == "data":
                continue

            if name in data.accessible_columns:
                select = getattr(select, name)

            elif name == "type":
                select = select.label_data["type"].astext

            elif name == "name":
                select = select.label_data["name"].astext

            elif name == "args":
                select = getattr(select, "label_data")["args"]

            else:
                # astext must be applied only on last key of JSONB right now accsess to variable more nested then args produce error

                select = select[name].astext

        if label:
            select = select.label(label)

        return select

    def generate_filter_expression(self, selector: Any, operator: str, value: Any):
        """
        Generate filters wich be apply to sqlalchemy query
        """

        if operator == "==":
            return selector == value
        elif operator == "$in":
            return selector.in_(value)
        elif operator == "$gt":
            return selector > value
        elif operator == "$lt":
            return selector < value
        elif operator == "$gte":
            return selector >= value
        elif operator == "$lte":
            return selector <= value

    def generate_filters(self, filters_block):
        """
        Parse our mongo like filters statment block


        As example:

            {
                "$match": {
                    "data.args.from": "0x0000000000000000000000000000000000000000",
                    "data.type": "event",
                    "data.name": "Transfer",
                    "data.address": "<contract address>",
                    "data.args.tokenId": {
                        "$cast": "int",
                        "$in": [
                        11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000
                        ]
                    }
                }
            }
        """

        list_of_filters: List[Dict[str, Any]] = []

        # it must be or/and nesting so we probably must start from most nested part and just apply nesting one by one
        # mainly need reverse the list of operations

        def unnesting_filters(filters_states, list_of_filters, condition="AND"):
            """
            Write new filters to filters list
            {
                'data.args.from': '0x0000000000000000000000000000000000000000',
                'data.type': 'event',
                'data.name': 'Transfer',
                'data.address': '<contract_address>',
                'data.args.tokenId': {'$cast': 'int', '$in':[11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000]
            }
            """

            filter = {condition: []}

            for key, value in filters_states.items():

                if key not in data.conditions_keys:

                    selector = self.generate_selector(key)

                    cast_to = None

                    if isinstance(value, str):
                        operator = "=="

                    elif isinstance(value, dict):

                        conditions = value.items()

                        for operation, op_value in conditions:
                            if operation == "$cast":
                                if op_value == "str":
                                    cast_to = String
                                elif op_value == "float":
                                    cast_to = Numeric
                                elif op_value == "int":
                                    cast_to = Integer

                            elif operation in ["$in", "$gt", "$lt", "$gte", "$lte"]:
                                value = op_value
                                operator = operation

                    if cast_to:
                        selector = cast(selector, cast_to)

                    filter_expression = self.generate_filter_expression(
                        selector, operator, value
                    )
                    filter[condition].append(filter_expression)

            list_of_filters.append(filter)

            if "AND" in filters_states:
                return filters_states["AND"], "AND"

            if "OR" in filters_states:
                return filters_states["OR"], "OR"

            return None, None

        filters_block, condition = unnesting_filters(
            getattr(filters_block, "match"), list_of_filters
        )

        while filters_block:
            filters_block, condition = unnesting_filters(
                filters_block, list_of_filters, condition
            )

        # we reverse filters and apply one by one as onion
        list_of_filters.reverse()

        filters = None

        for filter in list_of_filters:

            if "AND" in filter:
                if filters is not None:
                    filter["AND"].append(filters)
                filters = and_(*filter["AND"])

            if "OR" in filter:
                if filters is not None:
                    filter["OR"].append(filters)
                filters = or_(*filter["OR"])
        return filters

    def generate_select(self, select_block):
        """
        Generate list of select

         {
            "$map": [
                {
                    "data.args.to": "purchaser"
                },
                {
                    "data.args.tokenId": "tokenId"
                },
                {
                    "block_timestamp": "time_of_sale"
                }
            ]
        }
        """

        selects = []

        for select in getattr(select_block, "MAP"):

            # do better processing of list of dict
            for column_name, label in select.items():

                selector = self.generate_selector(column_name, label)

            selects.append(selector)

        return selects

    def generate_order(self, order_block):
        """
        Creater order by condition
        {"$sort": { "data.args.tokenId": "desc" }}

        """

        order_by = []

        for select, ordering in getattr(order_block, "SORT").items():

            selector = self.generate_selector(select)

            if ordering == "desc":
                order_by.append(selector.desc())
            if ordering == "asc":
                order_by.append(selector.asc())

        return order_by

    def stream_boundary_validator(
        self, stream_boundary: data.StreamBoundary
    ) -> data.StreamBoundary:
        """
        Stream boundary validator for the events provider.

        Checks that stream boundaries do not exceed periods of greater than 24 hours.

        Raises an error for invalid stream boundaries, else returns None.
        """
        valid_period_seconds = self.valid_period_seconds

        _, stream_boundary = validate_stream_boundary(
            stream_boundary, valid_period_seconds, raise_when_invalid=False
        )
        return stream_boundary

    def generate_events_query(
        self,
        db_session: Session,
        stream_boundary: data.StreamBoundary,
        parsed_filters: data.EventFilters,
    ) -> Query:
        """
        Builds a database query for Ethereum transactions that occurred within the window of time that
        the given stream_boundary represents and satisfying the constraints of parsed_filters.
        """

        Labels = get_label_model(self.blockchain)

        # process select block

        array_columns = []

        for block in parsed_filters.__root__:

            if isinstance(block, data.MatchFilters):

                filters = self.generate_filters(block)

            elif isinstance(block, data.SelectMap):

                array_columns = self.generate_select(block)

            elif isinstance(block, data.SortCondition):

                order_by = self.generate_order(block)

        query = db_session.query(*array_columns).filter(*filters).order_by(*order_by)

        # apply streamBoundary

        if stream_boundary.include_start:
            query = query.filter(Labels.block_timestamp >= stream_boundary.start_time)
        else:
            query = query.filter(Labels.block_timestamp > stream_boundary.start_time)

        if stream_boundary.end_time is not None:
            if stream_boundary.include_end:
                query = query.filter(Labels.block_timestamp <= stream_boundary.end_time)
            else:
                query = query.filter(Labels.block_timestamp <= stream_boundary.end_time)

        return query

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
        Returns blockchain events for the given addresses in the time period represented
        by stream_boundary.

        If the query does not require any data from this provider, returns None.
        """
        stream_boundary = self.stream_boundary_validator(stream_boundary)

        parsed_filters = self.parse_filters(query, user_subscriptions)
        if parsed_filters is None:
            return None

        ethereum_transactions = self.generate_events_query(
            db_session, stream_boundary, parsed_filters
        )

        ethereum_transactions = ethereum_transactions.order_by(
            text("block_timestamp desc")
        )

        # TODO(zomglings): Catch the operational error denoting that the statement timed out here
        # and wrap it in an error that tells the API to return the appropriate 400 response. Currently,
        # when the statement times out, the API returns a 500 status code to the client, which doesn't
        # do anything to help them get data from teh backend.
        # The error message on the API side when the statement times out:
        # > sqlalchemy.exc.OperationalError: (psycopg2.errors.QueryCanceled) canceling statement due to statement timeout
        # [{"$match":{"data.args.from":"0x0000000000000000000000000000000000000000","data.type":"event","data.name":"Transfer","data.address":"0xA2a13cE1824F3916fC84C65e559391fc6674e6e8","data.args.tokenId":{"$cast":"int","$in":[11000,12000,13000,14000,15000,16000,17000,18000,19000,20000]}}},{"$sort":{"data.args.tokenId":"desc"}},{"$map":[{"data.args.to":"purchaser"},{"data.args.tokenId":"tokenId"},{"block_timestamp":"time_of_sale"}]}]

        if not query.event_filters:
            events = [self.events(row) for row in ethereum_transactions]
        else:
            events = [row for row in ethereum_transactions]

        if (stream_boundary.end_time is None) and events:
            stream_boundary.end_time = events[0].event_timestamp
            stream_boundary.include_end = True

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
        Returns the num_events latest events from the current provider, subject to the constraints imposed
        by the given filters.

        If the query does not require any data from this provider, returns None.
        """
        assert num_events > 0, f"num_events ({num_events}) should be positive."

        stream_boundary = data.StreamBoundary(
            start_time=0, include_start=True, end_time=None, include_end=False
        )
        parsed_filters = self.parse_filters(query, user_subscriptions)
        if parsed_filters is None:
            return None
        ethereum_transactions = (
            self.generate_events_query(db_session, stream_boundary, parsed_filters)
            .order_by(text("block_timestamp desc"))
            .limit(num_events)
        )

        return [self.events(row) for row in ethereum_transactions]

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
        parsed_filters = self.parse_filters(query, user_subscriptions)
        if parsed_filters is None:
            return None

        maybe_ethereum_transaction = (
            self.generate_events_query(db_session, next_stream_boundary, parsed_filters)
            .order_by(text("block_timestamp asc"))
            .limit(1)
        ).one_or_none()

        if maybe_ethereum_transaction is None:
            return None
        return self.events(maybe_ethereum_transaction)

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
        parsed_filters = self.parse_filters(query, user_subscriptions)
        if parsed_filters is None:
            return None

        maybe_ethereum_transaction = (
            self.generate_events_query(
                db_session, previous_stream_boundary, parsed_filters
            )
            .order_by(text("block_timestamp desc"))
            .limit(1)
        ).one_or_none()
        if maybe_ethereum_transaction is None:
            return None
        return self.events(maybe_ethereum_transaction)


EthereumMoonwormProvider = MoonwormProvider(
    event_type="ethereum_smartcontract",
    blockchain=AvailableBlockchainType("ethereum"),
    description="Provider for resiving transactions from Ethereum tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)

PolygonMoonwormProvider = MoonwormProvider(
    event_type="polygon_smartcontract",
    blockchain=AvailableBlockchainType("polygon"),
    description="Provider for resiving transactions from Polygon tables.",
    streamboaundary_range_limit=2 * 60 * 60,
)
