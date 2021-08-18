"""
Stream queries - data structure, and parser.
"""
from dataclasses import dataclass, field
import logging
from typing import cast, List, Tuple

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass
class StreamQuery:
    subscription_types: List[str] = field(default_factory=list)
    # Subscriptions are expected to be specified in the form of an ordered pair:
    # (<subscription_type>, <address>)
    subscriptions: List[Tuple[str, str]] = field(default_factory=list)


SUBSCRIPTION_TYPE_PREFIX = "type:"
SUBSCRIPTION_PREFIX = "sub:"
SUBSCRIPTION_SEPARATOR = ":"


def parse_query_string(q: str) -> StreamQuery:
    """
    Parses a query string (as specified in query parameters on a call to the /streams/ endpoint).

    Args:
    1. q - Query string. It is parsed as follows:
        a. Query string is tokenized (by splitting on whitespace).
        b. Tokens of the form "type:<subscription_type>" populate the subscription_types field of the resulting StreamQuery
        c. Tokens of the form "sub:<subscription_type>:<address> populate the subscriptions field of the resulting StreamQuery

    Returns: Parsed StreamQuery object.
    """
    subscription_types: List[str] = []
    subscriptions: List[Tuple[str, str]] = []

    tokens = q.split()
    for token in tokens:
        if token.startswith(SUBSCRIPTION_TYPE_PREFIX):
            subscription_types.append(token[len(SUBSCRIPTION_TYPE_PREFIX) :])
        elif token.startswith(SUBSCRIPTION_PREFIX):
            contents = token[len(SUBSCRIPTION_PREFIX) :]
            components = tuple(contents.split(SUBSCRIPTION_SEPARATOR))
            if len(components) == 2:
                subscriptions.append(cast(Tuple[str, str], components))
            else:
                logger.error(f"Invalid subscription token: {token}")
        else:
            logger.error(f"Invalid token: {token}")

    return StreamQuery(
        subscription_types=subscription_types, subscriptions=subscriptions
    )
