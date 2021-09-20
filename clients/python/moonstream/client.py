from dataclasses import dataclass, field
import logging
import os
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)
log_level = logging.INFO
if os.environ.get("DEBUG", "").lower() in ["true", "1"]:
    log_level = logging.DEBUG
logger.setLevel(log_level)


# Keep this synchronized with the version in setup.py
CLIENT_VERSION = "0.0.1"

ENDPOINT_PING = "/ping"
ENDPOINT_VERSION = "/version"
ENDPOINT_NOW = "/now"
ENDPOINT_TOKEN = "/users/token"
ENDPOINT_SUBSCRIPTIONS = "/subscriptions/"
ENDPOINT_SUBSCRIPTION_TYPES = "/subscriptions/types"
ENDPOINTS = [
    ENDPOINT_PING,
    ENDPOINT_VERSION,
    ENDPOINT_NOW,
    ENDPOINT_TOKEN,
    ENDPOINT_SUBSCRIPTIONS,
    ENDPOINT_SUBSCRIPTION_TYPES,
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
            {"User-Agent": f"Moonstream Python client (version {CLIENT_VERSION})"}
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
        token = r.text
        self.authorize(token)
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
            ENDPOINT_SUBSCRIPTIONS,
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
