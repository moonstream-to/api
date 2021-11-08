import logging
from dataclasses import dataclass
from typing import Iterator, List, Optional, Tuple, cast

from hexbytes import HexBytes
from moonstreamdb.models import EthereumBlock, EthereumLabel, EthereumTransaction
from sqlalchemy.orm import Query, Session
from web3 import Web3
from web3.types import TxReceipt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ContractDeployment:
    address: str
    block_number: int
    transaction_hash: str
    deployer_address: str
    block_timestamp: int
    gas_used: int
    gas_price: int
    transaction_fee: int


@dataclass
class RawDeploymentTx:
    transaction_hash: str
    gas_price: int
    timestamp: int


class MoonstreamDataStore:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
        self.label = "contract_deployment"

    def get_last_labeled_block_number(
        self,
    ) -> int:
        """
        Returns the last block number that has been labeled.
        """

        last_block = (
            self.db_session.query(EthereumLabel)
            .filter(EthereumLabel.label == self.label)
            .order_by(EthereumLabel.block_number.desc())
            .first()
        )
        if last_block is None:
            return 0
        else:
            return last_block.block_number

    def get_first_labeled_block_number(self) -> int:
        """
        Returns the first block number that has been labeled.
        """
        first_block = (
            self.db_session.query(EthereumLabel)
            .filter(EthereumLabel.label == self.label)
            .order_by(EthereumLabel.block_number)
            .first()
        )
        if first_block is None:
            return 0
        return first_block.block_number

    def get_last_block_number(self) -> int:
        """
        Returns the last block number that has been processed.
        """
        last_block = (
            self.db_session.query(EthereumBlock)
            .order_by(EthereumBlock.block_number.desc())
            .first()
        )
        if last_block is None:
            return 0
        return last_block.block_number

    def get_first_block_number(self) -> int:
        """
        Returns the first block number that has been processed.
        """
        first_block = (
            self.db_session.query(EthereumBlock)
            .order_by(EthereumBlock.block_number.asc())
            .first()
        )
        if first_block is None:
            return 0
        return first_block.block_number

    def get_raw_contract_deployment_transactions(
        self, from_block: int, to_block: int
    ) -> List[RawDeploymentTx]:
        """
        Returns a list of raw contract deployment transactions.
        """
        result = (
            self.db_session.query(
                EthereumTransaction.hash,
                EthereumTransaction.gas_price,
                EthereumBlock.timestamp,
            )
            .join(
                EthereumBlock,
                EthereumTransaction.block_number == EthereumBlock.block_number,
            )
            .filter(EthereumBlock.block_number >= from_block)
            .filter(EthereumBlock.block_number <= to_block)
            .filter(EthereumTransaction.to_address == None)
            .all()
        )
        return [
            RawDeploymentTx(
                transaction_hash=row[0],
                gas_price=row[1],
                timestamp=row[2],
            )
            for row in result
        ]

    def save_contract_deployment_labels(
        self, contract_deployment_list: List[ContractDeployment]
    ) -> None:
        """
        Saves a list of contract deployment labels.
        """
        transaction_hashes = [
            contract_deployment.transaction_hash
            for contract_deployment in contract_deployment_list
        ]
        existing_labels = (
            self.db_session.query(EthereumLabel.transaction_hash)
            .filter(EthereumLabel.label == self.label)
            .filter(EthereumLabel.transaction_hash.in_(transaction_hashes))
            .all()
        )
        existing_labels_tx_hashes = [
            label_tx_hash[0] for label_tx_hash in existing_labels
        ]
        new_labels = [
            EthereumLabel(
                transaction_hash=contract_deployment.transaction_hash,
                block_number=contract_deployment.block_number,
                block_timestamp=contract_deployment.block_timestamp,
                label=self.label,
                address=contract_deployment.address,
                label_data={
                    "deployer": contract_deployment.deployer_address,
                    "gasUsed": int(contract_deployment.gas_used),
                    "gasPrice": int(contract_deployment.gas_price),
                    "transactionFee": int(contract_deployment.transaction_fee),
                },
            )
            for contract_deployment in contract_deployment_list
            if contract_deployment.transaction_hash not in existing_labels_tx_hashes
        ]
        if not new_labels:
            return
        try:
            logger.info(f"Saving {len(new_labels)} new contract deployment labels.")
            self.db_session.add_all(new_labels)
            self.db_session.commit()
        except Exception as e:
            logger.error(f"Error saving contract deployment labels: {e}")
            self.db_session.rollback()


def get_transaction_receipt(web3: Web3, tx_hash: str) -> TxReceipt:
    """
    Returns the transaction receipt for the given transaction hash.
    """

    return web3.eth.get_transaction_receipt(cast(HexBytes, tx_hash))


def get_contract_deployment_transactions(
    web3: Web3,
    datastore: MoonstreamDataStore,
    from_block: int,
    to_block: int,
) -> List[ContractDeployment]:
    """
    Returns a list of ContractDeployment objects for all contract deployment transactions in the given block range.
    """
    logger.info(
        f"Getting contract deployment transactions from {from_block} to {to_block}"
    )
    contract_deployment_transactions = []
    for raw_deployment_tx in datastore.get_raw_contract_deployment_transactions(
        from_block, to_block
    ):
        receipt = get_transaction_receipt(web3, raw_deployment_tx.transaction_hash)
        if receipt is None:
            continue

        contract_deployment_transactions.append(
            ContractDeployment(
                address=cast(str, receipt["contractAddress"]),
                block_number=receipt["blockNumber"],
                transaction_hash=receipt["transactionHash"].hex(),
                deployer_address=receipt["from"],
                block_timestamp=raw_deployment_tx.timestamp,
                gas_used=receipt["gasUsed"],
                gas_price=raw_deployment_tx.gas_price,
                transaction_fee=receipt["gasUsed"] * raw_deployment_tx.gas_price,
            )
        )
    return contract_deployment_transactions


# Function Fully Generated by copilot, looks correct, lol
def get_batch_block_range(
    from_block: int, to_block: int, batch_size: int
) -> Iterator[Tuple[int, int]]:
    """
    Returns a list of block ranges with the given batch size, from_block and to_block inclusive.
    """
    if from_block <= to_block:
        while from_block <= to_block:
            yield (from_block, min(from_block + batch_size - 1, to_block))
            from_block += batch_size
    else:
        while to_block <= from_block:
            yield (from_block, max(from_block - batch_size + 1, to_block))
            from_block -= batch_size


class ContractDeploymentCrawler:
    """
    Crawls contract deployments from MoonstreamDB transactions with the usage of web3
    to get transaction recipts
    """

    def __init__(self, web3: Web3, datastore: MoonstreamDataStore):
        self.web3 = web3
        self.datastore = datastore

    def crawl(
        self, from_block: Optional[int], to_block: Optional[int], batch_size: int = 200
    ) -> None:
        """
        Crawls contract deployments in batches with the given batch size
        If from_block is None then the first block from datastore is used as start
        If to_block is None then the latest block from datastore is used
        """
        if from_block is None:
            from_block = self.datastore.get_first_block_number()
        if to_block is None:
            to_block = self.datastore.get_last_block_number()

        for batch_from_block, batch_to_block in get_batch_block_range(
            from_block, to_block, batch_size
        ):
            contract_deployment_transactions = get_contract_deployment_transactions(
                self.web3, self.datastore, batch_from_block, batch_to_block
            )
            self.datastore.save_contract_deployment_labels(
                contract_deployment_transactions
            )
