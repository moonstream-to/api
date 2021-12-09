import web3
from moonstreamdb.db import yield_db_session_ctx
from web3.middleware import geth_poa_middleware

from ..settings import MOONSTREAM_MOONWORM_TASKS_JOURNAL, bugout_client
from .crawler import *
from .event_crawler import continuous_event_crawler


def crawl_events():
    initial_jobs = make_event_crawl_jobs(
        get_crawl_job_entries(
            SubscriptionTypes.POLYGON_BLOCKCHAIN,
            "event",
            MOONSTREAM_MOONWORM_TASKS_JOURNAL,
        )
    )
    print(len(initial_jobs))
    with yield_db_session_ctx() as session:
        web3 = Web3(
            Web3.HTTPProvider(
                "https://polygon-mainnet.infura.io/v3/0492b7dd00bb4ad8a3346b3a0d780140"
            )
        )
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        continuous_event_crawler(
            db_session=session,
            blockchain_type=AvailableBlockchainType.POLYGON,
            web3=web3,
            crawl_jobs=initial_jobs,
            start_block=web3.eth.blockNumber - 120000,
        )


crawl_events()
