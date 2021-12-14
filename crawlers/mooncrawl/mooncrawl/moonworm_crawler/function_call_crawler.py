import logging
from typing import Any, Dict, List, Optional, Union

from eth_typing.evm import ChecksumAddress
from hexbytes.main import HexBytes
from moonstreamdb.db import yield_db_session_ctx
from moonstreamdb.models import (
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
from moonworm.cu_watch import MockState
from moonworm.crawler.networks import Network
from sqlalchemy.orm import Session
from web3 import Web3
from moonstreamdb.models import Base

from ..data import AvailableBlockchainType
from .crawler import FunctionCallCrawlJob, _generate_reporter_callback
from ..blockchain import connect, get_block_model, get_label_model
from ..settings import CRAWLER_LABEL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _function_call_to_label(
    blockchain_type: AvailableBlockchainType, function_call: ContractFunctionCall
) -> Base:
    """
    Creates a label model.
    """
    label_model = get_label_model(blockchain_type)
    label = label_model(
        label=CRAWLER_LABEL,
        label_data={
            "type": "tx_call",
            "name": function_call.function_name,
            "caller": function_call.caller_address,
            "args": function_call.function_args,
            "status": function_call.status,
            "gasUsed": function_call.gas_used,
        },
        address=function_call.contract_address,
        block_number=function_call.block_number,
        transaction_hash=function_call.transaction_hash,
        block_timestamp=function_call.block_timestamp,
    )

    return label


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
