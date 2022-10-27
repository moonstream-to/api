import argparse
import datetime
from moonstream.client import Moonstream
import time
import requests
import json


def init_game_bank_queries_handler(args: argparse.Namespace):

    """
    Create the game bank queries.
    """

    client = Moonstream()

    # Create
    client.create_query(
        token=args.moonstream_token,
        name="cu-bank-blances",
        query="""
        WITH game_contract as (
            SELECT
                *
            from
                polygon_labels
            where
                address = '0x94f557dDdb245b11d031F57BA7F2C4f28C4A203e'
                and label = 'moonworm-alpha'
        )
        SELECT
            address,
            div(sum(
                CASE
                    WHEN result_balances.token_address = '0x64060aB139Feaae7f06Ca4E63189D86aDEb51691' THEN amount
                    ELSE 0
                END
            ), 10^18::decimal) as UNIM_BALANCE,
            div(sum(
                CASE
                    WHEN result_balances.token_address = '0x431CD3C9AC9Fc73644BF68bF5691f4B83F9E104f' THEN amount
                    ELSE 0
                END
            ), 10^18::decimal) as RBW_BALANCE
        FROM
            (
                select
                    transaction_hash,
                    label_data -> 'args' ->> 'player' as address,
                    jsonb_array_elements(label_data -> 'args' -> 'tokenAddresses') ->> 0 as token_address,
                    - jsonb_array_elements(label_data -> 'args' -> 'tokenAmounts') :: decimal as amount
                from
                    game_contract
                where
                    label_data ->> 'name' = 'UnstashedMultiple'
                union
                ALL
                select
                    transaction_hash,
                    label_data -> 'args' ->> 'player' as address,
                    label_data -> 'args' ->> 'token' as token_address,
                    -((label_data -> 'args' -> 'amount') :: decimal) as amount
                from
                    game_contract
                where
                    label_data ->> 'name' = 'Unstashed'
                union
                ALL
                select
                    transaction_hash,
                    label_data -> 'args' ->> 'player' as address,
                    label_data -> 'args' ->> 'token' as token_address,
                    (label_data -> 'args' ->> 'amount') :: decimal as amount
                from
                    game_contract
                where
                    label_data ->> 'name' = 'Stashed'
                union
                ALL
                        select
                    transaction_hash,
                    label_data -> 'args' ->> 'player' as address,
                    jsonb_array_elements(label_data -> 'args' -> 'tokenAddresses') ->> 0 as token_address,
                    jsonb_array_elements(label_data -> 'args' -> 'tokenAmounts') :: decimal as amount
                from
                    game_contract
                where
                    label_data ->> 'name' = 'StashedMultiple'
                
            ) result_balances
        group by
            address
        ORDER BY
            UNIM_BALANCE DESC,
            RBW_BALANCE DESC;
        """,
    )

    client.create_query(
        token=args.moonstream_token,
        name="cu-bank-withdrawals-total",
        query="""
        WITH game_contract as (
            SELECT
                *
            from
                polygon_labels
            where
                address = '0x94f557dDdb245b11d031F57BA7F2C4f28C4A203e'
                and label = 'moonworm-alpha'
                block_timestamp >= :block_timestamp
        ), withdoraws_total as (
        SELECT
            address,
            div(sum(
                CASE
                    WHEN result_balances.token_address = '0x64060aB139Feaae7f06Ca4E63189D86aDEb51691' THEN amount
                    ELSE 0
                END
            ), 10^18::decimal) as UNIM_BALANCE,
            div(sum(
                CASE
                    WHEN result_balances.token_address = '0x431CD3C9AC9Fc73644BF68bF5691f4B83F9E104f' THEN amount
                    ELSE 0
                END
            ), 10^18::decimal) as RBW_BALANCE
        FROM
            (
                select
                    transaction_hash,
                    label_data -> 'args' ->> 'player' as address,
                    jsonb_array_elements(label_data -> 'args' -> 'tokenAddresses') ->> 0 as token_address,
                    jsonb_array_elements(label_data -> 'args' -> 'tokenAmounts') :: decimal as amount
                from
                    game_contract
                where
                    label_data ->> 'name' = 'UnstashedMultiple'
                union
                ALL
                select
                    transaction_hash,
                    label_data -> 'args' ->> 'player' as address,
                    label_data -> 'args' ->> 'token' as token_address,
                    ((label_data -> 'args' -> 'amount') :: decimal) as amount
                from
                    game_contract
                where
                    label_data ->> 'name' = 'Unstashed'
            ) result_balances
                group by
            address
        ORDER BY
            UNIM_BALANCE DESC,
            RBW_BALANCE DESC
        )
        SELECT
            address,
            UNIM_BALANCE,
            RBW_BALANCE,
            UNIM_BALANCE + RBW_BALANCE as TOTAL
        FROM
            withdoraws_total
        ORDER BY
            TOTAL DESC;
        """,
    )

    client.create_query(
        token=args.moonstream_token,
        name="cu-bank-withdrawals-events",
        query="""
        WITH game_contract as (
            SELECT
                *
            from
                polygon_labels
            where
                address = '0x94f557dDdb245b11d031F57BA7F2C4f28C4A203e'
                and label = 'moonworm-alpha'
                block_timestamp >= :block_timestamp
        ), withdoraws_total as (
        SELECT
            address,
            CASE
                WHEN result_balances.token_address = '0x64060aB139Feaae7f06Ca4E63189D86aDEb51691' THEN 'UNIM'
                WHEN result_balances.token_address = '0x431CD3C9AC9Fc73644BF68bF5691f4B83F9E104f' THEN  'RBW'
            END as currency,
            div(amount, 10^18::decimal) as amount
        FROM
            (
                select
                    transaction_hash,
                    label_data -> 'args' ->> 'player' as address,
                    jsonb_array_elements(label_data -> 'args' -> 'tokenAddresses') ->> 0 as token_address,
                    jsonb_array_elements(label_data -> 'args' -> 'tokenAmounts') :: decimal as amount
                from
                    game_contract
                where
                    label_data ->> 'name' = 'UnstashedMultiple'
                union
                ALL
                select
                    transaction_hash,
                    label_data -> 'args' ->> 'player' as address,
                    label_data -> 'args' ->> 'token' as token_address,
                    ((label_data -> 'args' -> 'amount') :: decimal) as amount
                from
                    game_contract
                where
                    label_data ->> 'name' = 'Unstashed'
            ) result_balances
        )
        SELECT
            address,
            currency,
            amount,
        FROM
            withdoraws_total
        ORDER BY
            amount DESC;
        """,
    )


def list_user_queries_handler(args: argparse.Namespace):
    """
    List the user's queries.
    """

    client = Moonstream()

    queries = client.list_queries(
        token=args.token,
    )

    for query in queries.queries:
        print(query.name, query.id)


def delete_user_query(args: argparse.Namespace):
    """
    Delete the user's queries.
    """
    client = Moonstream()

    id = client.delete_query(
        token=args.token,
        name=args.name,
    )

    print(f"Query with name:{args.name} and id: {id} was deleted")


def generate_game_bank_report(args: argparse.Namespace):
    """
    han
    Generate the game bank query.
    """

    client = Moonstream()

    for query in client.list_queries(
        token=args.moonstream_token,
    ).queries:

        params = {}

        if (
            query.name == "cu-bank-withdrawals-total"
            or query.name == "cu-bank-withdrawals-events"
        ):
            blocktimestamp = int(time.time())
            params = {"block_timestamp": blocktimestamp}

        keep_going = True

        if_modified_since_datetime = datetime.datetime.utcnow()
        if_modified_since = if_modified_since_datetime.strftime(
            "%a, %d %b %Y %H:%M:%S GMT"
        )

        data_url = client.exec_query(
            token=args.token,
            query_name=query.name,
        )  # S3 presign_url
        while keep_going:
            data_response = requests.get(
                data_url,
                headers={"If-Modified-Since": if_modified_since},
                timeout=10,
            )
            # push to s3

            if data_response.status_code == 200:
                json.dump(data_response.json())
                break
            else:
                # You can put a sleep in here if you want
                continue

    pass


def main():

    parser = argparse.ArgumentParser()

    parser.set_defaults(func=lambda _: parser.print_help())

    subparsers = parser.add_subparsers()

    cu_reports_parser = subparsers.add_parser("cu-reports", help="CU Reports")

    cu_reports_subparsers = cu_reports_parser.add_subparsers()

    cu_reports_subparsers.add_argument(
        "--moonstream-token",
        required=True,
        type=str,
    )
    queries_parser = cu_reports_subparsers.add_parser(
        "queries",
        help="Queries commands",
    )

    queries_parser.set_defaults(func=lambda _: queries_parser.print_help())

    queries_subparsers = queries_parser.add_subparsers()

    queries_subparsers.add_parser(
        "list",
        help="List all queries",
        description="List all queries",
    ).set_defaults(func=list_user_queries_handler)

    queries_subparsers.add_parser(
        "init",
        help="Create all predifind query",
        description="Create all predifind query",
    ).set_defaults(func=init_game_bank_queries_handler)

    delete_query = queries_subparsers.add_parser(
        "delete",
        help="Delete all predifind query",
        description="Delete all predifind query",
    )

    delete_query.add_argument(
        "--name",
        required=True,
        type=str,
    )

    delete_query.set_defaults(func=delete_user_query)

    cu_bank_parser = cu_reports_subparsers.add_parser(
        "generate-reports",
        help="Generate cu-bank state reports",
    )
    cu_bank_parser.add_argument("--addresses", type=str, required=True)
    cu_bank_parser.add_argument(
        "--output",
        required=True,
        type=str,
        help="Output file name",
    )
    cu_bank_parser.add_argument("--blockchain", type=str, help="Blockchain")
    cu_bank_parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Limit of the search results",
    )

    cu_bank_parser.add_argument(
        "--",
        type=str,
        help="Filter by created_at",
    )

    cu_bank_parser.set_defaults(func=generate_game_bank_report)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
