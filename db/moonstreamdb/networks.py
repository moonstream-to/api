

from enum import Enum
from typing import Dict, Union

from .models import (
    Base,
    EthereumBlock,
    EthereumLabel,
    EthereumTransaction,
    MumbaiBlock,
    MumbaiLabel,
    MumbaiTransaction,
    PolygonBlock,
    PolygonLabel,
    PolygonTransaction,
    WyrmBlock,
    WyrmLabel,
    WyrmTransaction,
    XDaiBlock,
    XDaiLabel,
    XDaiTransaction,
)


class Network(Enum):
    ethereum = "ethereum"
    polygon = "polygon"
    mumbai = "mumbai"
    xdai = "xdai"
    wyrm = "wyrm"

tx_raw_types = Union[
    EthereumTransaction,
    MumbaiTransaction,
    PolygonTransaction,
    WyrmTransaction,
    XDaiTransaction
]    

MODELS: Dict[Network, Dict[str, Base]] = {
    Network.ethereum: {
        "blocks": EthereumBlock,
        "labels": EthereumLabel,
        "transactions": EthereumTransaction,
    },
    Network.mumbai: {
        "blocks": MumbaiBlock,
        "labels": MumbaiLabel,
        "transactions": MumbaiTransaction,
    },
    Network.polygon: {
        "blocks": PolygonBlock,
        "labels": PolygonLabel,
        "transactions": PolygonTransaction,
    },
    Network.xdai: {
        "blocks": XDaiBlock,
        "labels": XDaiLabel,
        "transactions": XDaiTransaction,
    },
    Network.wyrm: {
        "blocks": WyrmBlock,
        "labels": WyrmLabel,
        "transactions": WyrmTransaction,
    },
}
