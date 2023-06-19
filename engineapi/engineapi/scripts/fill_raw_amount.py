import argparse
import logging
from typing import Dict, List, Optional, Any

from .. import db
from ..contracts import Dropper_interface, ERC20_interface
from ..settings import BLOCKCHAIN_WEB3_PROVIDERS, UNSUPPORTED_BLOCKCHAIN_ERROR_MESSAGE


def run_fill_raw_amount(args: argparse.Namespace):
    # sync raw_amount column with amount column

    # create chache of claim token type
    # newtwork contract and list of claims with their token type

    token_types: Dict[str, Dict[str, List[Dict[str, Any]]]] = dict()

    with db.yield_db_session_ctx() as db_session:
        res = db_session.execute(
            """select distinct dropper_contracts.blockchain, dropper_contracts.address, dropper_claims.claim_id from dropper_contracts
                            left join dropper_claims on dropper_contracts.id = dropper_claims.dropper_contract_id
                            where dropper_claims.claim_id is not null"""
        )
        results = res.fetchall()

        for blockchain, address, claim_id in results:
            if blockchain not in token_types:
                token_types[blockchain] = dict()
            if address not in token_types[blockchain]:
                token_types[blockchain][address] = list()
            token_types[blockchain][address].append(claim_id)

        db_session.execute(
            """
            create table temptest
            (
                blockchain varchar,
                address varchar,
                claim_id varchar,
                token_type varchar,
                zeros varchar
            )

            """
        )

        for blockchain in token_types:
            if blockchain not in BLOCKCHAIN_WEB3_PROVIDERS:
                logging.warn(
                    f"Blockchain: {blockchain}. {UNSUPPORTED_BLOCKCHAIN_ERROR_MESSAGE}"
                )
                continue
            for address in token_types[blockchain]:
                dropper_contract = Dropper_interface.Contract(
                    BLOCKCHAIN_WEB3_PROVIDERS[blockchain], address
                )

                for claim_id in token_types[blockchain][address]:
                    claim_info = dropper_contract.getClaim(claim_id).call()
                    zeros = None
                    if claim_info[0] == 20:
                        erc20_contract = ERC20_interface.Contract(
                            BLOCKCHAIN_WEB3_PROVIDERS[blockchain], claim_info[1]
                        )
                        zeros = "0" * erc20_contract.decimals()

                    db_session.execute(
                        """
                                insert into temptest
                                (
                                    blockchain,
                                    address,
                                    claim_id,
                                    token_type,
                                    zeros

                                )
                                values
                                (
                                    :blockchain,
                                    :address,
                                    :claim_id,
                                    :token_type,
                                    :zeros
                                )
                                """,
                        {
                            "blockchain": blockchain,
                            "address": address,
                            "claim_id": str(claim_id),
                            "token_type": str(claim_info[0]),
                            "zeros": zeros,
                        },
                    )

        db_session.commit()

        # update raw_amount column
        db_session.execute(
            """
            update
                dropper_claimants
            set
                raw_amount = (
                    CASE
                        WHEN (
                            select
                                DISTINCT temptest.token_type
                            from
                                temptest
                                inner join dropper_claims ON temptest.claim_id :: int = dropper_claims.claim_id
                            where
                                dropper_claims.id = dropper_claimants.dropper_claim_id
                        ) :: int = 20 THEN CASE
                            WHEN dropper_claimants.amount is not null
                            and dropper_claimants.amount > 0 THEN CONCAT(
                                CAST(dropper_claimants.amount as varchar),
                                    (
                                        select
                                            temptest.zeros
                                        from
                                            temptest
                                            inner join dropper_claims ON temptest.claim_id :: int = dropper_claims.claim_id
                                        where
                                            dropper_claims.id = dropper_claimants.dropper_claim_id
                                    )
                                )
                                WHEN true THEN CAST(dropper_claimants.amount as varchar)
                            END
                            WHEN true THEN CAST(dropper_claimants.amount as varchar)
                        END
                    );
            """
        )
        db_session.commit()


def main():
    parser = argparse.ArgumentParser(
        description="dao: The command line interface to Moonstream DAO"
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers()

    run_fill_raw_amount_parser = subparsers.add_parser(
        "fill_raw_amount", help="Fill raw_amount column"
    )

    run_fill_raw_amount_parser.set_defaults(func=run_fill_raw_amount)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
