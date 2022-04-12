import logging

from web3 import Web3

from .settings import MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI

logger = logging.getLogger(__name__)

moonstream_web3_provider = Web3(
    Web3.HTTPProvider(MOONSTREAM_ETHEREUM_WEB3_PROVIDER_URI)
)


def yield_web3_provider() -> Web3:
    return moonstream_web3_provider
