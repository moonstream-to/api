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
ENDPOINTS = [ENDPOINT_PING, ENDPOINT_VERSION, ENDPOINT_NOW, ENDPOINT_TOKEN]


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


@dataclass(frozen=True)
class APISpec:
    url: str
    endpoints: Dict[str, str]


class Moonstream:
    """
    A Moonstream client configured to communicate with a given Moonstream API server.
    """

    def __init__(
        self, url: str = "https://api.moonstream.to", timeout: Optional[float] = None
    ):
        endpoints = moonstream_endpoints(url)
        self.api = APISpec(url=url, endpoints=endpoints)
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": "Moonstream Python client"})

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

    def authorize(self, api_token: str) -> None:
        if not api_token:
            logger.warning("Setting authorization header to empty token.")
        self._session.headers.update({"Authorization": f"Bearer {api_token}"})

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
