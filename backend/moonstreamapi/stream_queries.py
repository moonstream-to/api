"""
Stream queries - data structure, and parser.
"""
from ast import operator
import json
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from .data import EventFilters

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass
class StreamQuery:
    event_filters: Optional[EventFilters] = None
    subscription_types: List[str] = field(default_factory=list)
    # Subscriptions are expected to be specified in the form of an ordered pair:
    # (<subscription_type>, <address>)
    subscriptions: List[Tuple[str, str]] = field(default_factory=list)


EVENT_PREFIX = "event:"
SUBSCRIPTION_TYPE_PREFIX = "type:"
SUBSCRIPTION_PREFIX = "sub:"
SUBSCRIPTION_SEPARATOR = ":"


def parse_query_string(q: str) -> StreamQuery:
    """
    Parses a query string (as specified in query parameters on a call to the /streams/ endpoint).


    Example( generated from code ):
    stream?q="type:ethereum_blockchain sub:<subscription_type>:<address>"
    Missing why type is required?


    Args:
    1. q - Query string. It is parsed as follows:
        a. Query string is tokenized (by splitting on whitespace).
        b. Tokens of the form "type:<subscription_type>" populate the subscription_types field of the resulting StreamQuery.
        c. Tokens of the form "sub:<subscription_type>:<filter> populate the subscriptions field of the resulting StreamQuery.
           This "<filter>" should be a valid filter for the event provider corresponding to the given subscription type.
        d. Tokens of the form "event:<query>" query wich writed via schema defined in https://github.com/bugout-dev/moonstream/issues/534
           This query was transfor to sqlalchemy query to datbase wich give ability request any kind of data from labels tabel.

    Returns: Parsed StreamQuery object.
    """

    subscription_types: List[str] = []
    subscriptions: List[Tuple[str, str]] = []
    event_filters: Optional[EventFilters] = None

    tokens = q.split()
    for token in tokens:

        if token.startswith(SUBSCRIPTION_TYPE_PREFIX):
            # Read subcriptions types
            subscription_types.append(token[len(SUBSCRIPTION_TYPE_PREFIX) :])
        elif token.startswith(SUBSCRIPTION_PREFIX):
            # Read combine of types and address
            contents = token[len(SUBSCRIPTION_PREFIX) :]
            components = contents.split(SUBSCRIPTION_SEPARATOR)

            if len(components) < 2:
                logger.error(f"Invalid subscription token: {token}")
            else:
                subscriptions.append(
                    (components[0], SUBSCRIPTION_SEPARATOR.join(components[1:]))
                )

        elif token.startswith(EVENT_PREFIX):

            raw_data = token.split(EVENT_PREFIX)[-1]

            try:
                print(raw_data)
                filters = EventFilters.parse_obj(json.loads(raw_data))

                event_filters = filters
            except Exception as err:
                print(err)
                logger.error(f"Exception on validate event filters: {err}")

        else:
            logger.error(f"Invalid token: {token}")

    return StreamQuery(
        subscription_types=subscription_types,
        subscriptions=subscriptions,
        event_filters=event_filters,
    )
