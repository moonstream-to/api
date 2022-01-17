import argparse
import binascii
import sys
from typing import List, Optional, Type, Union, cast

import pyevmasm
from moonstreamdb.models import ESDEventSignature, ESDFunctionSignature
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import text

from moonstreamdb.db import yield_db_session

from .data import ContractABI, EVMEventSignature, EVMFunctionSignature


def query_for_text_signatures(
    session: Session,
    hex_signature: str,
    db_model: Union[ESDFunctionSignature, ESDEventSignature],
) -> List[str]:
    query = session.query(db_model)
    query = query.filter(db_model.hex_signature == hex_signature)
    results = query.all()
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


def decode_abi(source: str, session: Optional[Session] = None) -> ContractABI:
    normalized_source = source
    if normalized_source[:2] == "0x":
        normalized_source = normalized_source[2:]
    disassembled = pyevmasm.disassemble_all(binascii.unhexlify(normalized_source))
    function_hex_signatures = []
    event_hex_signatures = []

    should_close_session = False
    if session is None:
        should_close_session = True
        session = next(yield_db_session())

    for instruction in disassembled:
        if instruction.name == "PUSH4":
            hex_signature = "0x{:x}".format(instruction.operand)
            if hex_signature not in function_hex_signatures:
                function_hex_signatures.append(hex_signature)
        elif instruction.name == "PUSH32":
            hex_signature = "0x{:x}".format(instruction.operand)
            if hex_signature not in event_hex_signatures:
                event_hex_signatures.append(hex_signature)

    try:
        function_signatures = decode_signatures(
            session, function_hex_signatures, EVMFunctionSignature, ESDFunctionSignature
        )
        event_signatures = decode_signatures(
            session, event_hex_signatures, EVMEventSignature, ESDEventSignature
        )
    finally:
        if should_close_session:
            session.close()

    abi = ContractABI(
        functions=cast(EVMFunctionSignature, function_signatures),
        events=cast(EVMEventSignature, event_signatures),
    )
    return abi


def main() -> None:
    parser = argparse.ArgumentParser(description="Decode Ethereum smart contract ABIs")
    parser.add_argument(
        "-i",
        "--infile",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="File containing the ABI to decode",
    )
    args = parser.parse_args()

    source: Optional[str] = None
    with args.infile as ifp:
        source = ifp.read().strip()
    if source is None:
        raise ValueError("Could not read ABI.")

    abi = decode_abi(source)
    print(abi.json())


if __name__ == "__main__":
    main()
