import argparse
import logging
import time
from typing import Optional
from uuid import UUID

from moonstreamdb.blockchain import AvailableBlockchainType
from sqlalchemy.orm.session import Session
from web3 import Web3

from ..blockchain import connect
from ..db import yield_db_session_ctx
from ..settings import NB_CONTROLLER_ACCESS_ID
from .deployment_crawler import ContractDeploymentCrawler, MoonstreamDataStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_crawler_asc(
    w3: Web3,
    session: Session,
    from_block: Optional[int],
    to_block: Optional[int],
    synchronize: bool,
    batch_size: int,
    respect_state: bool,
    sleep_time: int,
):
    """
    Runs crawler in ascending order
    """
    moonstream_data_store = MoonstreamDataStore(session)
    contract_deployment_crawler = ContractDeploymentCrawler(w3, moonstream_data_store)

    if respect_state:
        from_block = moonstream_data_store.get_last_labeled_block_number() + 1
        logger.info(f"Respecting state, starting from block {from_block}")

    if from_block is None:
        from_block = moonstream_data_store.get_first_block_number()
        logger.info(f"Starting block set to : {from_block}")

    if to_block is None:
        to_block = moonstream_data_store.get_last_block_number()
        logger.info(f"Ending block set to : {to_block}")

    assert (
        from_block <= to_block
    ), "from_block must be less than or equal to to_block in asc order, used --order desc"

    logger.info(f"Starting crawling from block {from_block} to block {to_block}")
    contract_deployment_crawler.crawl(
        from_block=from_block,
        to_block=to_block,
        batch_size=batch_size,
    )
    if synchronize:
        last_crawled_block = to_block
        while True:
            contract_deployment_crawler.crawl(
                from_block=last_crawled_block + 1,
                to_block=None,  # to_block will be set to last_crawled_block
                batch_size=batch_size,
            )
            time.sleep(sleep_time)


def run_crawler_desc(
    w3: Web3,
    session: Session,
    from_block: Optional[int],
    to_block: Optional[int],
    synchronize: bool,
    batch_size: int,
    respect_state: bool,
    sleep_time: int,
):
    """
    Runs crawler in descending order
    """
    moonstream_data_store = MoonstreamDataStore(session)
    contract_deployment_crawler = ContractDeploymentCrawler(w3, moonstream_data_store)

    if respect_state:
        to_block = moonstream_data_store.get_first_block_number() - 1
        logger.info(f"Respecting state, ending at block {to_block}")

    if from_block is None:
        from_block = moonstream_data_store.get_last_block_number()
        logger.info(f"Starting block set to : {from_block}")

    if to_block is None:
        to_block = moonstream_data_store.get_first_block_number()
        logger.info(f"Ending block set to : {to_block}")

    assert (
        from_block >= to_block
    ), "from_block must be greater than or equal to to_block in desc order, used --order asc"

    logger.info(f"Starting crawling from block {from_block} to block {to_block}")
    contract_deployment_crawler.crawl(
        from_block=from_block,
        to_block=to_block,
        batch_size=batch_size,
    )
    if synchronize:
        last_crawled_block = to_block
        while True:
            to_block = moonstream_data_store.get_first_block_number()
            contract_deployment_crawler.crawl(
                from_block=last_crawled_block - 1,
                to_block=to_block,
                batch_size=batch_size,
            )
            time.sleep(sleep_time)


def handle_parser(args: argparse.Namespace):
    with yield_db_session_ctx() as session:
        w3 = connect(AvailableBlockchainType.ETHEREUM, access_id=args.access_id)
        if args.order == "asc":
            run_crawler_asc(
                w3=w3,
                session=session,
                from_block=args.start,
                to_block=args.to,
                synchronize=args.synchronize,
                batch_size=args.batch,
                respect_state=args.respect_state,
                sleep_time=args.sleep,
            )
        elif args.order == "desc":
            run_crawler_desc(
                w3=w3,
                session=session,
                from_block=args.start,
                to_block=args.to,
                synchronize=args.synchronize,
                batch_size=args.batch,
                respect_state=args.respect_state,
                sleep_time=args.sleep,
            )


def generate_parser():
    """
    --start, -s: block to start crawling from, default: minimum block from database
    --to, -t: block to stop crawling at, default: maximum block from database
    --order: order to crawl : (desc, asc) default: asc
    --synchronize: Continious crawling, default: False
    --batch, -b : batch size, default: 10
    --respect-state: If set to True:\n If order is asc: start=last_labeled_block+1\n If order is desc: start=first_labeled_block-1
    """

    parser = argparse.ArgumentParser(description="Moonstream Deployment Crawler")

    parser.add_argument(
        "--access-id",
        default=NB_CONTROLLER_ACCESS_ID,
        type=UUID,
        help="User access ID",
    )

    parser.add_argument(
        "--start", "-s", type=int, default=None, help="block to start crawling from"
    )
    parser.add_argument(
        "--to", "-t", type=int, default=None, help="block to stop crawling at"
    )

    parser.add_argument(
        "--order",
        "-o",
        type=str,
        default="asc",
        choices=["asc", "desc"],
        help="order to crawl : (desc, asc)",
    )

    parser.add_argument(
        "--synchronize", action="store_true", default=False, help="Continious crawling"
    )
    parser.add_argument("--batch", "-b", type=int, default=10, help="batch size")
    parser.add_argument(
        "--respect-state",
        action="store_true",
        default=False,
        help="If set to True:\n If order is asc: start=last_labeled_block+1\n If order is desc: start=first_labeled_block-1",
    )
    parser.add_argument(
        "--sleep",
        type=int,
        default=3 * 60,
        help="time to sleep synzhronize mode waiting for new block crawled to db",
    )
    parser.set_defaults(func=handle_parser)
    return parser


def main():
    parser = generate_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
