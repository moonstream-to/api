import logging
from typing import List, Union

from moonstreamdb.blockchain import AvailableBlockchainType
from moonstreamtypes.blockchain import AvailableBlockchainType
from moonstreamdb.networks import blockchain_type_to_network_type  # type: ignore
from moonworm.crawler.function_call_crawler import (  # type: ignore
    ContractFunctionCall,
    FunctionCallCrawler,
)
from moonworm.crawler.moonstream_ethereum_state_provider import (  # type: ignore
    MoonstreamEthereumStateProvider,
)
from moonworm.crawler.ethereum_state_provider import Web3StateProvider
from moonworm.watch import MockState  # type: ignore
from sqlalchemy.orm import Session
from web3 import Web3

from .crawler import FunctionCallCrawlJob, _generate_reporter_callback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _crawl_functions(
    blockchain_type: AvailableBlockchainType,
    ethereum_state_provider: Union[MoonstreamEthereumStateProvider, Web3StateProvider],
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
        print(f"Processing job {function_call_crawler.whitelisted_methods}")
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
    version: int = 2,
):
    if version != 2:
        raise ValueError("Only version 2 is supported")
    try:
        network = blockchain_type_to_network_type(blockchain_type=blockchain_type)  # type: ignore
    except Exception as e:
        raise Exception(e)

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
