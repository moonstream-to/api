import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Generator, List, Optional, Tuple

import requests

from .version import MOONSTREAM_CLIENT_VERSION

logger = logging.getLogger(__name__)
log_level = logging.INFO
if os.environ.get("DEBUG", "").lower() in ["true", "1"]:
    log_level = logging.DEBUG
logger.setLevel(log_level)

ENDPOINT_PING = "/ping"
ENDPOINT_VERSION = "/version"
ENDPOINT_NOW = "/now"
ENDPOINT_TOKEN = "/users/token"
ENDPOINT_SUBSCRIPTIONS = "/subscriptions/"
ENDPOINT_SUBSCRIPTION_TYPES = "/subscriptions/types"
ENDPOINT_STREAMS = "/streams/"
ENDPOINT_STREAMS_LATEST = "/streams/latest"
ENDPOINT_STREAMS_NEXT = "/streams/next"
ENDPOINT_STREAMS_PREVIOUS = "/streams/previous"

ENDPOINTS = [
    ENDPOINT_PING,
    ENDPOINT_VERSION,
    ENDPOINT_NOW,
    ENDPOINT_TOKEN,
    ENDPOINT_SUBSCRIPTIONS,
    ENDPOINT_SUBSCRIPTION_TYPES,
    ENDPOINT_STREAMS,
    ENDPOINT_STREAMS_LATEST,
    ENDPOINT_STREAMS_NEXT,
    ENDPOINT_STREAMS_PREVIOUS,
]


def moonstream_endpoints(url: str) -> Dict[str, str]:
    """
    Creates a dictionary of Moonstream API endpoints at the given Moonstream API URL.
    """
    url_with_protocol = url
    if not (
        url_with_protocol.startswith("http://")
        or url_with_protocol.startswith("https://")
    ):
        url_with_protocol = f"http://{url_with_protocol}"

    normalized_url = url_with_protocol.rstrip("/")

    return {endpoint: f"{normalized_url}{endpoint}" for endpoint in ENDPOINTS}


class UnexpectedResponse(Exception):
    """
    Raised when a server response cannot be parsed into the appropriate/expected Python structure.
    """


class Unauthenticated(Exception):
    """
    Raised when a user tries to make a request that needs to be authenticated by they are not authenticated.
    """


@dataclass(frozen=True)
class APISpec:
    url: str
    endpoints: Dict[str, str]


class Moonstream:
    """
    A Moonstream client configured to communicate with a given Moonstream API server.
    """

    def __init__(
        self,
        url: str = "https://api.moonstream.to",
        timeout: Optional[float] = None,
    ):
        """
        Initializes a Moonstream API client.

        Arguments:
        url - Moonstream API URL. By default this points to the production Moonstream API at https://api.moonstream.to,
        but you can replace it with the URL of any other Moonstream API instance.
        timeout - Timeout (in seconds) for Moonstream API requests. Default is None, which means that
        Moonstream API requests will never time out.

        Returns: A Moonstream client.
        """
        endpoints = moonstream_endpoints(url)
        self.api = APISpec(url=url, endpoints=endpoints)
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {
                "User-Agent": f"Moonstream Python client (version {MOONSTREAM_CLIENT_VERSION})"
            }
        )

    def ping(self) -> Dict[str, Any]:
        """
        Checks that you have a connection to the Moonstream API.
        """
        r = self._session.get(self.api.endpoints[ENDPOINT_PING])
        r.raise_for_status()
        return r.json()

    def version(self) -> Dict[str, Any]:
        """
        Gets the Moonstream API version information from the server.
        """
        r = self._session.get(self.api.endpoints[ENDPOINT_VERSION])
        r.raise_for_status()
        return r.json()

    def server_time(self) -> float:
        """
        Gets the current time (as microseconds since the Unix epoch) on the server.
        """
        r = self._session.get(self.api.endpoints[ENDPOINT_NOW])
        r.raise_for_status()
        result = r.json()
        raw_epoch_time = result.get("epoch_time")
        if raw_epoch_time is None:
            raise UnexpectedResponse(
                f'Server response does not contain "epoch_time": {result}'
            )

        try:
            epoch_time = float(raw_epoch_time)
        except:
            raise UnexpectedResponse(
                f"Could not process epoch time as a float: {raw_epoch_time}"
            )

        return epoch_time

    def authorize(self, access_token: str) -> None:
        if not access_token:
            logger.warning("Setting authorization header to empty token.")
        self._session.headers.update({"Authorization": f"Bearer {access_token}"})

    def requires_authorization(self):
        if self._session.headers.get("Authorization") is None:
            raise Unauthenticated(
                'This method requires that you authenticate to the API, either by calling the "authorize" method with an API token or by calling the "login" method.'
            )

    def login(self, username: str, password: Optional[str] = None) -> str:
        """
        Authorizes this client to act as the given user when communicating with the Moonstream API.

        To register an account on the production Moonstream API, go to https://moonstream.to.

        Arguments:
        username - Username of the user to authenticate as.
        password - Optional password for the user. If this is not provided, you will be prompted for
        the password.
        """
        if password is None:
            password = input(f"Moonstream password for {username}: ")

        r = self._session.post(
            self.api.endpoints[ENDPOINT_TOKEN],
            data={"username": username, "password": password},
        )
        r.raise_for_status()

        token = r.json()
        self.authorize(token["id"])
        return token

    def logout(self) -> None:
        """
        Logs the current user out of the Moonstream client.
        """
        self._session.delete(self.api.endpoints[ENDPOINT_TOKEN])
        self._session.headers.pop("Authorization")

    def subscription_types(self) -> Dict[str, Any]:
        """
        Gets the currently available subscription types on the Moonstream API.
        """
        r = self._session.get(self.api.endpoints[ENDPOINT_SUBSCRIPTION_TYPES])
        r.raise_for_status()
        return r.json()

    def list_subscriptions(self) -> Dict[str, Any]:
        """
        Gets the currently authorized user's subscriptions from the API server.
        """
        self.requires_authorization()
        r = self._session.get(self.api.endpoints[ENDPOINT_SUBSCRIPTIONS])
        r.raise_for_status()
        return r.json()

    def create_subscription(
        self, subscription_type: str, label: str, color: str, specifier: str = ""
    ) -> Dict[str, Any]:
        """
        Creates a subscription.

        Arguments:
        subscription_type - The type of subscription you would like to create. To see the available subscription
        types, call the "subscription_types" method on this Moonstream client. This argument must be
        the "id" if the subscription type you want.
        label - A label for the subscription. This will identify the subscription to you in your stream.
        color - A hexadecimal color to associate with the subscription.
        specifier - A specifier for the subscription, which must correspond to one of the choices in the
        subscription type. This is optional because some subscription types do not require a specifier.

        Returns: The subscription resource that was created on the backend.
        """
        self.requires_authorization()
        r = self._session.post(
            self.api.endpoints[ENDPOINT_SUBSCRIPTIONS],
            data={
                "subscription_type_id": subscription_type,
                "label": label,
                "color": color,
                "address": specifier,
            },
        )
        r.raise_for_status()
        return r.json()

    def delete_subscription(self, id: str) -> Dict[str, Any]:
        """
        Delete a subscription by ID.

        Arguments:
        id - ID of the subscription to delete.

        Returns: The subscription resource that was deleted.
        """
        self.requires_authorization()
        r = self._session.delete(f"{self.api.endpoints[ENDPOINT_SUBSCRIPTIONS]}{id}")
        r.raise_for_status()
        return r.json()

    def update_subscription(
        self, id: str, label: Optional[str] = None, color: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a subscription label or color.

        Arguments:
        label - New label for subscription (optional).
        color - New color for subscription (optional).

        Returns - If neither label or color are specified, raises a ValueError. Otherwise PUTs the updated
        information to the server and returns the updated subscription resource.
        """
        if label is None and color is None:
            raise ValueError(
                "At least one of the arguments to this method should not be None."
            )
        self.requires_authorization()
        data = {}
        if label is not None:
            data["label"] = label
        if color is not None:
            data["color"] = color

        r = self._session.put(
            f"{self.api.endpoints[ENDPOINT_SUBSCRIPTIONS]}{id}", data=data
        )
        r.raise_for_status()
        return r.json()

    def latest_events(self, q: str = "") -> List[Dict[str, Any]]:
        """
        Returns the latest events in your stream. You can optionally provide a query parameter to
        constrain the query to specific subscription types or to specific subscriptions.

        Arguments:
        - q - Optional query (default is the empty string). The syntax to constrain to a particular
        type of subscription is "type:<subscription_type>". For example, to get the latest event from
        your Ethereum transaction pool subscriptions, you would use "type:ethereum_txpool".

        Returns: A list of the latest events in your stream.
        """
        self.requires_authorization()
        query_params: Dict[str, str] = {}
        if q:
            query_params["q"] = q
        r = self._session.get(
            self.api.endpoints[ENDPOINT_STREAMS_LATEST], params=query_params
        )
        r.raise_for_status()
        return r.json()

    def next_event(
        self, end_time: int, include_end: bool = True, q: str = ""
    ) -> Optional[Dict[str, Any]]:
        """
        Return the earliest event in your stream that occurred after the given end_time.

        Arguments:
        - end_time - Time after which you want to retrieve the earliest event from your stream.
        - include_end - If True, the result is the first event that occurred in your stream strictly
        *after* the end time. If False, then you will get the first event that occurred in your
        stream *on* or *after* the end time.
        - q - Optional query to filter over your available subscriptions and subscription types.

        Returns: None if no event has occurred after the given end time, else returns a dictionary
        representing that event.
        """
        self.requires_authorization()
        query_params: Dict[str, Any] = {
            "end_time": end_time,
            "include_end": include_end,
        }
        if q:
            query_params["q"] = q
        r = self._session.get(
            self.api.endpoints[ENDPOINT_STREAMS_NEXT], params=query_params
        )
        r.raise_for_status()
        return r.json()

    def previous_event(
        self, start_time: int, include_start: bool = True, q: str = ""
    ) -> Optional[Dict[str, Any]]:
        """
        Return the latest event in your stream that occurred before the given start_time.

        Arguments:
        - start_time - Time before which you want to retrieve the latest event from your stream.
        - include_start - If True, the result is the last event that occurred in your stream strictly
        *before* the start time. If False, then you will get the last event that occurred in your
        stream *on* or *before* the start time.
        - q - Optional query to filter over your available subscriptions and subscription types.

        Returns: None if no event has occurred before the given start time, else returns a dictionary
        representing that event.
        """
        self.requires_authorization()
        query_params: Dict[str, Any] = {
            "start_time": start_time,
            "include_start": include_start,
        }
        if q:
            query_params["q"] = q
        r = self._session.get(
            self.api.endpoints[ENDPOINT_STREAMS_PREVIOUS], params=query_params
        )
        r.raise_for_status()
        return r.json()

    def events(
        self,
        start_time: int,
        end_time: int,
        include_start: bool = False,
        include_end: bool = False,
        q: str = "",
    ) -> Dict[str, Any]:
        """
        Return all events in your stream that occurred between the given start and end times.

        Arguments:
        - start_time - Time after which you want to query your stream.
        - include_start - Whether or not events that occurred exactly at the start_time should be included in the results.
        - end_time - Time before which you want to query your stream.
        - include_end - Whether or not events that occurred exactly at the end_time should be included in the results.
        - q - Optional query to filter over your available subscriptions and subscription types.

        Returns: A dictionary representing the results of your query.
        """
        self.requires_authorization()
        query_params: Dict[str, Any] = {
            "start_time": start_time,
            "include_start": include_start,
            "end_time": end_time,
            "include_end": include_end,
        }
        if q:
            query_params["q"] = q

        r = self._session.get(self.api.endpoints[ENDPOINT_STREAMS], params=query_params)
        r.raise_for_status()
        return r.json()

    def create_stream(
        self,
        start_time: int,
        end_time: Optional[int] = None,
        q: str = "",
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Return a stream of event. Event packs will be generated with 1 hour time range.

        Arguments:
        - start_time - One of time border.
        - end_time - Time until the end of stream, if set to None stream will be going forward endlessly.
        - q - Optional query to filter over your available subscriptions and subscription types.

        Returns: A dictionary stream representing the results of your query.
        """
        # TODO(kompotkot): Add tests
        shift_two_hours = 2 * 60 * 60  # 2 hours
        shift_half_hour = 1 * 30 * 30  # 30 min

        def fetch_events(
            modified_start_time: int, modified_end_time: int
        ) -> Generator[Tuple[Dict[str, Any], bool], None, None]:
            # If it is going from top to bottom in history,
            # then time_range will be reversed
            reversed_time = False
            if modified_start_time > modified_end_time:
                reversed_time = True
            max_boundary = max(modified_start_time, modified_end_time)
            min_boundary = min(modified_start_time, modified_end_time)

            time_range_list = []
            # 300, 450 with shift 100 => [{"start_time": 300, "end_time": 399}, {"start_time": 400, "end_time": 450}]
            if max_boundary - min_boundary > shift_half_hour:
                for i in range(min_boundary, max_boundary, shift_half_hour):
                    end_i = (
                        i + shift_half_hour - 1
                        if i + shift_half_hour <= max_boundary
                        else max_boundary
                    )
                    time_range_list.append({"start_time": i, "end_time": end_i})
            else:
                time_range_list.append(
                    {"start_time": min_boundary, "end_time": max_boundary}
                )
            if reversed_time:
                time_range_list.reverse()

            for time_range in time_range_list:
                r_json = self.events(
                    start_time=time_range["start_time"],
                    end_time=time_range["end_time"],
                    include_start=True,
                    include_end=True,
                    q=q,
                )

                yield r_json, reversed_time

            time_range_list = time_range_list[:]

        if end_time is None:
            float_start_time = start_time

            while True:
                end_time = int(self.server_time())
                # If time range is greater then 2 hours,
                # shift float_start time close to end_time to prevent stream block
                if end_time - float_start_time > shift_two_hours:
                    float_start_time = shift_two_hours
                for r_json, reversed_time in fetch_events(float_start_time, end_time):

                    yield r_json

                    events = r_json.get("events", [])
                    if len(events) > 0:
                        # Updating float_start_time after first iteration to last event time
                        if reversed_time:
                            float_start_time = events[-1].get("event_timestamp") - 1
                        else:
                            float_start_time = events[0].get("event_timestamp") + 1

                    else:
                        # If there are no events in response, wait
                        # until new will be added
                        time.sleep(5)
        else:
            for r_json, reversed_time in fetch_events(start_time, end_time):
                yield r_json


def client_from_env() -> Moonstream:
    """
    Produces a Moonstream client instantiated using the following environment variables:
    - MOONSTREAM_API_URL: Specifies the url parameter on the Moonstream client
    - MOONSTREAM_TIMEOUT_SECONDS: Specifies the request timeout
    - MOONSTREAM_ACCESS_TOKEN: If this environment variable is defined, the client sets this token as
    the authorization header for all Moonstream API requests.
    """
    kwargs: Dict[str, Any] = {}

    url = os.environ.get("MOONSTREAM_API_URL")
    if url is not None:
        kwargs["url"] = url

    raw_timeout = os.environ.get("MOONSTREAM_TIMEOUT_SECONDS")
    timeout: Optional[float] = None
    if raw_timeout is not None:
        try:
            timeout = float(raw_timeout)
        except:
            raise ValueError(
                f"Could not convert MOONSTREAM_TIMEOUT_SECONDS ({raw_timeout}) to float."
            )

    kwargs["timeout"] = timeout

    moonstream_client = Moonstream(**kwargs)

    access_token = os.environ.get("MOONSTREAM_ACCESS_TOKEN")
    if access_token is not None:
        moonstream_client.authorize(access_token)

    return moonstream_client
