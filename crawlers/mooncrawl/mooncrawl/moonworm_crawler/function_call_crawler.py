import logging
from typing import Any, Dict, List, Optional, Union

from eth_typing.evm import ChecksumAddress
from hexbytes.main import HexBytes
from moonstreamdb.db import yield_db_session_ctx
from moonstreamdb.models import (
    Base,
    EthereumLabel,
    EthereumTransaction,
    PolygonLabel,
    PolygonTransaction,
)
from moonworm.crawler.function_call_crawler import (
    ContractFunctionCall,
    FunctionCallCrawler,
)
from moonworm.crawler.moonstream_ethereum_state_provider import (
    MoonstreamEthereumStateProvider,
)
from moonworm.crawler.networks import Network
from moonworm.cu_watch import MockState
from sqlalchemy.orm import Session
from web3 import Web3

from ..blockchain import connect, get_block_model, get_label_model
from ..data import AvailableBlockchainType
from ..settings import CRAWLER_LABEL
from .crawler import FunctionCallCrawlJob, _generate_reporter_callback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _crawl_functions(
    blockchain_type: AvailableBlockchainType,
    ethereum_state_provider: MoonstreamEthereumStateProvider,
    jobs: List[FunctionCallCrawlJob],
    from_block: int,
    to_block: int,
) -> List[ContractFunctionCall]:

    shared_state = MockState()

    crawled_functions = []

    for job in jobs:
        function_call_crawler = FunctionCallCrawler(
            shared_state,
            ethereum_state_provider,
            job.contract_abi,
            [job.contract_address],
            on_decode_error=_generate_reporter_callback(
                "function_call", blockchain_type
            ),
        )
        function_call_crawler.crawl(
            from_block,
            to_block,
        )
    crawled_functions = shared_state.state
    return crawled_functions


def function_call_crawler(
    db_session: Session,
    blockchain_type: AvailableBlockchainType,
    web3: Web3,
    jobs: List[FunctionCallCrawlJob],
    start_block: int,
    end_block: int,
    batch_size: int,
):
    network = (
        Network.ethereum
        if blockchain_type == AvailableBlockchainType.ETHEREUM
        else Network.polygon
    )
    ethereum_state_provider = MoonstreamEthereumStateProvider(
        web3,
        network,
        db_session,
    )

    for i in range(start_block, end_block + 1, batch_size):
        logger.info(f"Crawling from block {i} to {i + batch_size - 1}")
        crawled_functions = _crawl_functions(
            blockchain_type,
            ethereum_state_provider,
            jobs,
            i,
            min(i + batch_size - 1, end_block),
        )
        logger.info(f"Crawled {len(crawled_functions)} functions")
        for function_call in crawled_functions:
            print(function_call)
