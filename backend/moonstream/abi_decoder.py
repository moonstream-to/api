from typing import Generic, List, Optional, TypeVar, Union, Type, cast
import pyevmasm
import binascii

from moonstreamdb.db import yield_db_session_ctx
from moonstreamdb.models import ESDEventSignature, ESDFunctionSignature
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import text
from .data import EVMEventSignature, EVMFunctionSignature, ContractABI


def query_for_text_signatures(
    session: Session,
    hex_signature: str,
    db_model: Union[ESDFunctionSignature, ESDEventSignature],
) -> Optional[List[str]]:
    query = session.query(db_model)
    query = query.filter(db_model.hex_signature == hex_signature)
    results = query.all()
    if not results:
        return None
    text_signatures = []
    for el in results:
        text_signatures.append(el.text_signature)
    return text_signatures


def decode_signatures(
    session: Session,
    hex_signatures: List[str],
    data_model: Union[Type[EVMEventSignature], Type[EVMFunctionSignature]],
    db_model: Union[ESDEventSignature, ESDFunctionSignature],
) -> List[Union[EVMEventSignature, EVMFunctionSignature]]:
    decoded_signatures = []
    for hex_signature in hex_signatures:
        signature = data_model(hex_signature=hex_signature)
        signature.text_signature_candidates = query_for_text_signatures(
            session, hex_signature, db_model
        )
        decoded_signatures.append(signature)
    return decoded_signatures


def decode_abi(source: str) -> ContractABI:
    disassembled = pyevmasm.disassemble_all(binascii.unhexlify(source))
    function_hex_signatures = []
    event_hex_signatures = []

    for instruction in disassembled:
        if instruction.name == "PUSH4":
            hex_signature = "0x{:x}".format(instruction.operand)
            if hex_signature not in function_hex_signatures:
                function_hex_signatures.append(hex_signature)
        elif instruction.name == "PUSH32":
            hex_signature = "0x{:x}".format(instruction.operand)
            if hex_signature not in event_hex_signatures:
                event_hex_signatures.append(hex_signature)

    with yield_db_session_ctx() as session:
        function_signatures = decode_signatures(
            session, function_hex_signatures, EVMFunctionSignature, ESDFunctionSignature
        )
        event_signatures = decode_signatures(
            session, event_hex_signatures, EVMEventSignature, ESDEventSignature
        )

        abi = ContractABI(
            functions=cast(EVMFunctionSignature, function_signatures),
            events=cast(EVMEventSignature, event_signatures),
        )
        return abi
