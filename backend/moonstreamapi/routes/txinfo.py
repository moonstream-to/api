"""
Moonstream's /txinfo endpoints.

These endpoints enrich raw blockchain transactions (as well as pending transactions, hypothetical
transactions, etc.) with side information and return objects that are better suited for displaying to
end users.
"""
import logging
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from moonstreamdb.db import yield_db_session

from .. import actions, data
from ..abi_decoder import decode_abi

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/txinfo")

# TODO(zomglings): Factor out the enrichment logic into a separate action, because it may be useful
# independently from serving API calls (e.g. data processing).
# TODO(kompotkot): Re-organize function to be able handle each steps with exceptions.
@router.post(
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

    source_info: Optional[data.EthereumSmartContractSourceInfo] = None
    if txinfo_request.tx.to_address is not None:
        source_info = actions.get_contract_source_info(
            db_session, txinfo_request.tx.to_address
        )
    if source_info is not None:
        response.smart_contract_info = source_info
        response.smart_contract_address = txinfo_request.tx.to_address
        response.is_smart_contract_call = True
    return response
