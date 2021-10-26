from web3 import Web3
from .settings import MOONSTREAM_WEB3_PROVIDER

moonstream_web3_provider = Web3(Web3.HTTPProvider(MOONSTREAM_WEB3_PROVIDER))


def yield_web3_provider() -> Web3:
    return moonstream_web3_provider
