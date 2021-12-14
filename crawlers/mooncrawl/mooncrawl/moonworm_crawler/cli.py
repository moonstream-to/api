import web3
from moonstreamdb.db import yield_db_session_ctx
from web3.middleware import geth_poa_middleware

from ..settings import MOONSTREAM_MOONWORM_TASKS_JOURNAL, bugout_client
from .crawler import *
from .event_crawler import continuous_event_crawler
from .function_call_crawler import function_call_crawler


def crawl_events():

    initial_event_jobs = make_event_crawl_jobs(
        get_crawl_job_entries(
            SubscriptionTypes.POLYGON_BLOCKCHAIN,
            "event",
            MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        )
    )
    logger.info(f"Initial event crawl jobs count: {len(initial_event_jobs)}")

    initial_function_call_jobs = make_function_call_crawl_jobs(
        get_crawl_job_entries(
            SubscriptionTypes.POLYGON_BLOCKCHAIN,
            "function",
            MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        )
    )
    logger.info(
        f"Initial function call crawl jobs count: {len(initial_function_call_jobs)}"
    )
    print(initial_function_call_jobs)

    with yield_db_session_ctx() as db_session:
        web3 = Web3(
            Web3.HTTPProvider(
                "https://polygon-mainnet.infura.io/v3/0492b7dd00bb4ad8a3346b3a0d780140"
            )
        )
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        function_call_crawler(
            db_session,
            AvailableBlockchainType.POLYGON,
            web3,
            initial_function_call_jobs,
            start_block=21418707,
            end_block=web3.eth.blockNumber,
            batch_size=100,
        )
        # continuous_event_crawler(
        #     db_session=session,
        #     blockchain_type=AvailableBlockchainType.POLYGON,
        #     web3=web3,
        #     crawl_jobs=initial_event_jobs,
        #     start_block=web3.eth.blockNumber - 120000,
        # )


crawl_events()
