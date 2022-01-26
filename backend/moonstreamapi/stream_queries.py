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


# custom parser
EVENTS_PREFIX = "events:"
EVENT_ADDRESS_PREFIX = "event_address:"
EVENT_LABEL_PREFIX = "event_label:"
EVENT_ARGS_PREFIX = "argument:"

# parse as custom parser
EVENTS_PREFIX = "events:"
EVENT_ADDRESS_PREFIX = "address:"
EVENT_LABEL_PREFIX = "label:"
EVENT_ARGS_PREFIX = "arg_type:"
EVENT_ARGS_OPERATOR_PREFIX = "arg_operation:"
EVENT_ARGS_VALUE_PREFIX = "arg_value:"


# example of object parser

EVENT_PREFIX = "event:"
EVENT_ADDRESS_PREFIX = "address:"
EVENT_LABEL_PREFIX = "label:"
EVENT_ARGS_PREFIX = "arg_type:"
EVENT_ARGS_OPERATOR_PREFIX = "arg_operation:"
EVENT_ARGS_VALUE_PREFIX = "arg_value:"


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

    event:<address>:<event_name>:<argument_name>:<argument_type>:<operator>:<arg_value>

    #
    tx_call
    event

    {
        output_statment: [
            block_timestamp:{
                func:
                type:
            }
            address:{
                func:
                type:
            }
            args:{
                name:
                unc:
                type:
            }


        ]
        filters :[  # All times or
            {
                "address": "0xe77bbFD8ED65720F187eFdD109e38D75EaCa7385",
                "label_filters": [
                    {
                        "name": "Transfer"
                        "type": "metod"
                        "args": [
                            {
                                "name": "to"
                                "value": "0x962355fC06e85A341E9f20C395F2fe70f25E793E"
                                "type": "str"
                            }
                        ]
                    }
                ]

            },
            {
                "address": "0x1AaaC93313A263992b682DCA299142eCdA0a43Bc",
                "label_filters": [
                    {
                        "name": "Transfer"
                        "type": "metod"
                        "args_filters": [
                            "amount[int]>=5"
                            ]
                        ]
                    }
                ]

            },
        ]
        group_condition: [

        ]
        order_by":[

        ]
    }

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
