"""
Moonstream's /txinfo endpoints.

These endpoints enrich raw blockchain transactions (as well as pending transactions, hypothetical
transactions, etc.) with side information and return objects that are better suited for displaying to
end users.
"""
import logging
from typing import Dict

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from moonstreamdb.db import yield_db_session
from moonstreamdb.models import EthereumAddress
from sqlalchemy.orm import Session

from ..abi_decoder import decode_abi
from .. import actions
from .. import data
from ..middleware import BroodAuthMiddleware
from ..settings import DOCS_TARGET_PATH, ORIGINS, DOCS_PATHS
from ..version import MOONSTREAM_VERSION

logger = logging.getLogger(__name__)

tags_metadata = [
    {"name": "txinfo", "description": "Ethereum transactions info."},
]

app = FastAPI(
    title=f"Moonstream /txinfo API.",
    description="User, token and password handlers.",
    version=MOONSTREAM_VERSION,
    openapi_tags=tags_metadata,
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=f"/{DOCS_TARGET_PATH}",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

whitelist_paths: Dict[str, str] = {}
whitelist_paths.update(DOCS_PATHS)
app.add_middleware(BroodAuthMiddleware, whitelist=whitelist_paths)


# TODO(zomglings): Factor out the enrichment logic into a separate action, because it may be useful
# independently from serving API calls (e.g. data processing).
# TODO(kompotkot): Re-organize function to be able handle each steps with exceptions.
@app.post(
    "/ethereum_blockchain",
    tags=["txinfo"],
    response_model=data.TxinfoEthereumBlockchainResponse,
)
async def txinfo_ethereum_blockchain_handler(
    txinfo_request: data.TxinfoEthereumBlockchainRequest,
    db_session: Session = Depends(yield_db_session),
) -> data.TxinfoEthereumBlockchainResponse:
    response = data.TxinfoEthereumBlockchainResponse(tx=txinfo_request.tx)
    if txinfo_request.tx.input is not None:
        try:
            response.abi = decode_abi(txinfo_request.tx.input, db_session)
        except Exception as err:
            logger.error(r"Could not decode ABI:")
            logger.error(err)
            response.errors.append("Could not decode ABI from the given input")

    # transaction is contract deployment:
    if txinfo_request.tx.to_address is None:
        response.is_smart_contract_deployment = True
        smart_contract = (
            db_session.query(EthereumAddress)
            .filter(EthereumAddress.transaction_hash == txinfo_request.tx.hash)
            .one_or_none()
        )
        if smart_contract is not None:
            response.is_smart_contract_deployment = True
    else:
        source_info = actions.get_contract_source_info(
            db_session, txinfo_request.tx.to_address
        )
        if source_info is not None:
            response.smart_contract_info = source_info
            response.smart_contract_address = txinfo_request.tx.to_address
            response.is_smart_contract_call = True
    return response
