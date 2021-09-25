import os

from moonstreamdb.db import yield_db_session_ctx
from web3 import Web3

from .materialize import get_rows, EventType, preproccess

if __name__ == "__main__":
    web3_path = os.environ.get("MOONSTREAM_IPC_PATH")
    web3_client = Web3(Web3.HTTPProvider(web3_path))

    with yield_db_session_ctx() as db_session:
        rows = get_rows(db_session, EventType.TRANSFER)
        rows = preproccess(db_session, web3_client, rows)
        for row in rows:
            print(row)
