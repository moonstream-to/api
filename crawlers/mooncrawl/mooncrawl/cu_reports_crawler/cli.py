import argparse
import csv
import datetime
import logging
from io import StringIO
from moonstream.client import Moonstream  # type: ignore
import time
import requests  # type: ignore
import json

from typing import Any, Dict, Union

from uuid import UUID

import boto3
from .queries import tokenomics_queries, cu_bank_queries

from ..settings import (
    MOONSTREAM_S3_PUBLIC_DATA_BUCKET,
    MOONSTREAM_S3_PUBLIC_DATA_BUCKET_PREFIX,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

addresess_erc20_721 = {
    "0x64060aB139Feaae7f06Ca4E63189D86aDEb51691": "ERC20",  # UNIM
    "0x431CD3C9AC9Fc73644BF68bF5691f4B83F9E104f": "ERC20",  # RBW
    "0xdC0479CC5BbA033B3e7De9F178607150B3AbCe1f": "NFT",  # unicorns
    "0xA2a13cE1824F3916fC84C65e559391fc6674e6e8": "NFT",  # lands
    "0xa7D50EE3D7485288107664cf758E877a0D351725": "NFT",  # shadowcorns
}

addresess_erc1155 = ["0x99A558BDBdE247C2B2716f0D4cFb0E246DFB697D"]


def recive_S3_data_from_query(
    client: Moonstream,
    token: Union[str, UUID],
    query_name: str,
    params: Dict[str, Any],
    time_await: int = 2,
    max_retries: int = 30,
) -> Any:
    """
    Await the query to be update data on S3 with if_modified_since and return new the data.
    """

    keep_going = True

    repeat = 0

    if_modified_since_datetime = datetime.datetime.utcnow()
    if_modified_since = if_modified_since_datetime.strftime("%a, %d %b %Y %H:%M:%S GMT")

    time.sleep(2)

    data_url = client.exec_query(
        token=token,
        name=query_name,
        params=params,
    )  # S3 presign_url

    while keep_going:
        time.sleep(time_await)
        try:
            data_response = requests.get(
                data_url.url,
                headers={"If-Modified-Since": if_modified_since},
                timeout=5,
            )
        except Exception as e:
            logger.error(e)
            continue

        if data_response.status_code == 200:
            break

        repeat += 1

        if repeat > max_retries:
            logger.info("Too many retries")
            break
    return data_response.json()


def generate_report(
    client: Moonstream,
    token: Union[str, UUID],
    query_name: str,
    params: Dict[str, Any],
    bucket_prefix: str,
    bucket: str,
    key: str,
):
    """
    Generate the report.
    """

    try:
        json_data = recive_S3_data_from_query(
            client=client,
            token=token,
            query_name=query_name,
            params=params,
        )

        client.upload_query_results(
            json.dumps(json_data),
            bucket,
            f"{bucket_prefix}/{key}",
        )
        logger.info(
            f"Report generated and results uploaded at: https://{bucket}/{bucket_prefix}/{key}"
        )
    except Exception as err:
        logger.error(
            f"Cant recive or load data for s3, for query: {query_name}, bucket: {bucket}, key: {key}. End with error: {err}"
        )


def create_user_query(
    client: Moonstream,
    token: Union[str, UUID],
    query_name: str,
    query: str,
):
    """
    Create a user query.
    """

    try:
        client.create_query(token=token, name=query_name, query=query)
    except Exception as err:
        logger.error(f"Cant create user query: {query_name}. End with error: {err}")


def delete_user_query(client: Moonstream, token: str, query_name: str):
    """
    Delete the user's queries.
    """

    id = client.delete_query(
        token=token,
        name=query_name,
    )

    logger.info(f"Query with name:{query_name} and id: {id} was deleted")


def init_game_bank_queries_handler(args: argparse.Namespace):
    """
    Create the game bank queries.
    """

    client = Moonstream()

    for query in cu_bank_queries:
        try:
            if args.overwrite:
                try:
                    # delete
                    delete_user_query(
                        client=client,
                        token=args.moonstream_token,
                        query_name=query["name"],
                    )
                except Exception as err:
                    logger.error(err)
            # create
            created_entry = client.create_query(
                token=args.moonstream_token,
                name=query["name"],
                query=query["query"],
            )
            logger.info(
                f"Created query {query['name']} please validate it in the UI url {created_entry.journal_url}/entries/{created_entry.id}/"
            )
        except Exception as e:
            logger.error(e)
            pass


def init_tokenomics_queries_handler(args: argparse.Namespace):
    """
    Create the tokenomics queries.
    """

    client = Moonstream()

    for query in tokenomics_queries:
        try:
            if args.overwrite:
                try:
                    # delete
                    delete_user_query(
                        client=client,
                        token=args.moonstream_token,
                        query_name=query["name"],
                    )
                except Exception as err:
                    logger.error(err)
            # create
            created_entry = client.create_query(
                token=args.moonstream_token,
                name=query["name"],
                query=query["query"],
            )
            logger.info(
                f"Created query {query['name']} please validate it in the UI url {created_entry.journal_url}/entries/{created_entry.id}/"
            )
        except Exception as e:
            logger.error(e)
            pass


def run_tokenomics_queries_handler(args: argparse.Namespace):
    client = Moonstream()

    query_name = "erc20_721_volume"

    ### Run voluem query

    ranges = [
        {"time_format": "YYYY-MM-DD HH24", "time_range": "24 hours"},
        {"time_format": "YYYY-MM-DD HH24", "time_range": "7 days"},
        {"time_format": "YYYY-MM-DD", "time_range": "30 days"},
    ]

    # volume of erc20 and erc721

    for address, type in addresess_erc20_721.items():
        for range in ranges:
            params: Dict[str, Any] = {
                "address": address,
                "type": type,
                "time_format": range["time_format"],
                "time_range": range["time_range"],
            }

            generate_report(
                client=client,
                token=args.moonstream_token,
                query_name=query_name,
                params=params,
                bucket_prefix=MOONSTREAM_S3_PUBLIC_DATA_BUCKET_PREFIX,
                bucket=MOONSTREAM_S3_PUBLIC_DATA_BUCKET,
                key=f'{query_name}/{address}/{range["time_range"].replace(" ","_")}/data.json',
            )

    # volume change of erc20 and erc721

    query_name = "volume_change"

    for address, type in addresess_erc20_721.items():
        for range in ranges:
            params = {
                "address": address,
                "type": type,
                "time_range": range["time_range"],
            }

            generate_report(
                client=client,
                token=args.moonstream_token,
                query_name=query_name,
                params=params,
                bucket_prefix=MOONSTREAM_S3_PUBLIC_DATA_BUCKET_PREFIX,
                bucket=MOONSTREAM_S3_PUBLIC_DATA_BUCKET,
                key=f'{query_name}/{address}/{range["time_range"].replace(" ","_")}/data.json',
            )

    query_name = "erc1155_volume"

    # volume of erc1155

    addresess_erc1155 = ["0x99A558BDBdE247C2B2716f0D4cFb0E246DFB697D"]

    for address in addresess_erc1155:
        for range in ranges:
            params = {
                "address": address,
                "time_format": range["time_format"],
                "time_range": range["time_range"],
            }

            generate_report(
                client=client,
                token=args.moonstream_token,
                query_name=query_name,
                params=params,
                bucket_prefix=MOONSTREAM_S3_PUBLIC_DATA_BUCKET_PREFIX,
                bucket=MOONSTREAM_S3_PUBLIC_DATA_BUCKET,
                key=f"{query_name}/{address}/{range['time_range'].replace(' ','_')}/data.json",
            )

    # most_recent_sale

    query_name = "most_recent_sale"

    for address, type in addresess_erc20_721.items():
        if type == "NFT":
            for amount in [10, 100]:
                params = {
                    "address": address,
                    "amount": amount,
                }

                generate_report(
                    client=client,
                    token=args.moonstream_token,
                    query_name=query_name,
                    params=params,
                    bucket_prefix=MOONSTREAM_S3_PUBLIC_DATA_BUCKET_PREFIX,
                    bucket=MOONSTREAM_S3_PUBLIC_DATA_BUCKET,
                    key=f"{query_name}/{address}/{amount}/data.json",
                )

    # most_active_buyers

    query_name = "most_active_buyers"

    for address, type in addresess_erc20_721.items():
        if type == "NFT":
            for range in ranges:
                params = {
                    "address": address,
                    "time_range": range["time_range"],
                }

                generate_report(
                    client=client,
                    token=args.moonstream_token,
                    query_name=query_name,
                    params=params,
                    bucket_prefix=MOONSTREAM_S3_PUBLIC_DATA_BUCKET_PREFIX,
                    bucket=MOONSTREAM_S3_PUBLIC_DATA_BUCKET,
                    key=f"{query_name}/{address}/{range['time_range'].replace(' ','_')}/data.json",
                )

    # most_active_sellers

    query_name = "most_active_sellers"

    for address, type in addresess_erc20_721.items():
        if type == "NFT":
            for range in ranges:
                params = {
                    "address": address,
                    "time_range": range["time_range"],
                }

                generate_report(
                    client=client,
                    token=args.moonstream_token,
                    query_name=query_name,
                    params=params,
                    bucket_prefix=MOONSTREAM_S3_PUBLIC_DATA_BUCKET_PREFIX,
                    bucket=MOONSTREAM_S3_PUBLIC_DATA_BUCKET,
                    key=f"{query_name}/{address}/{range['time_range'].replace(' ','_')}/data.json",
                )

    # lagerst_owners

    query_name = "lagerst_owners"
    for address, type in addresess_erc20_721.items():
        if type == "NFT":
            params = {
                "address": address,
            }

            generate_report(
                client=client,
                token=args.moonstream_token,
                query_name=query_name,
                params=params,
                bucket_prefix=MOONSTREAM_S3_PUBLIC_DATA_BUCKET_PREFIX,
                bucket=MOONSTREAM_S3_PUBLIC_DATA_BUCKET,
                key=f"{query_name}/{address}/data.json",
            )

    # total_supply_erc721

    query_name = "total_supply_erc721"

    for address, type in addresess_erc20_721.items():
        if type == "NFT":
            params = {
                "address": address,
            }

            generate_report(
                client=client,
                token=args.moonstream_token,
                query_name=query_name,
                params=params,
                bucket_prefix=MOONSTREAM_S3_PUBLIC_DATA_BUCKET_PREFIX,
                bucket=MOONSTREAM_S3_PUBLIC_DATA_BUCKET,
                key=f"{query_name}/{address}/data.json",
            )

    # total_supply_terminus

    query_name = "total_supply_terminus"

    for address in addresess_erc1155:
        params = {
            "address": address,
        }

        generate_report(
            client=client,
            token=args.moonstream_token,
            query_name=query_name,
            params=params,
            bucket_prefix=MOONSTREAM_S3_PUBLIC_DATA_BUCKET_PREFIX,
            bucket=MOONSTREAM_S3_PUBLIC_DATA_BUCKET,
            key=f"{query_name}/{address}/data.json",
        )

    logger.info("Done")


def list_user_queries_handler(args: argparse.Namespace):
    """
    List the user's queries.
    """

    client = Moonstream()

    queries = client.list_queries(
        token=args.moonstream_token,
    )

    for query in queries.queries:
        logger.info(query.name, query.id)


def delete_user_query_handler(args: argparse.Namespace):
    """
    Delete the user's queries.
    """
    client = Moonstream()

    delete_user_query(client=client, token=args.moonstream_token, query_name=args.name)


def create_user_query_handler(args: argparse.Namespace):
    """
    Create the user's queries.
    """
    client = Moonstream()

    for query in tokenomics_queries:
        if query["name"] == args.name:
            create_user_query(
                client=client,
                token=args.moonstream_token,
                query_name=query["name"],
                query=query["query"],
            )


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
            token=args.moonstream_token,
            query_name=query.name,
            params=params,
        )  # S3 presign_url

        while keep_going:
            data_response = requests.get(
                data_url,
                headers={"If-Modified-Since": if_modified_since},
                timeout=10,
            )
            # push to s3

            if data_response.status_code == 200:
                json.dumps(data_response.json())
                break
            else:
                time.sleep(2)
                continue

    pass


def generate_report_nft_dashboard_handler(args: argparse.Namespace):
    """
    Generate report from metadata crawler and push to s3
    use query API
    """

    client = Moonstream()

    for query in client.list_queries(
        token=args.moonstream_token,
    ).queries:
        params = {}  # type: ignore

        if query.name != "cu_nft_dashboard_data":
            continue

        logger.info(f"Generating report for {query.name}")
        data = recive_S3_data_from_query(
            client=client,
            token=args.moonstream_token,
            query_name=query.name,
            params=params,
        )

        logger.info(f"Data recived. Uploading report for {query.name} as json")

        # send as json
        ext = "json"

        url = client.upload_query_results(
            json.dumps(data),
            key=f"queries/{query.name}/data.{ext}",
            bucket=MOONSTREAM_S3_PUBLIC_DATA_BUCKET,
        )

        logger.info(f"Report uploaded to {url}")

        logger.info(f"Data recived. Uploading report for {query.name} as csv")

        ext = "csv"
        csv_buffer = StringIO()

        dict_csv_writer = csv.DictWriter(
            csv_buffer, fieldnames=data["data"][0].keys(), delimiter=","
        )

        # upload to s3 bucket as csv
        dict_csv_writer.writeheader()
        dict_csv_writer.writerows(data["data"])

        url = client.upload_query_results(
            data=csv_buffer.getvalue().encode("utf-8"),
            key=f"queries/{query.name}/data.{ext}",
            bucket=MOONSTREAM_S3_PUBLIC_DATA_BUCKET,
        )

        logger.info(f"Report uploaded to {url}")


def generate_ens_domains_cache_handler(args: argparse.Namespace):
    client = Moonstream()

    for query in client.list_queries(
        token=args.moonstream_token,
    ).queries:
        params = {}  # type: ignore

        if query.name != "ens_cache":
            continue

        logger.info(f"Generating report for {query.name}")
        data = recive_S3_data_from_query(
            client=client,
            token=args.moonstream_token,
            query_name=query.name,
            params=params,
        )

        logger.info(f"Data recived. Uploading report for {query.name} as json")

        # send as json
        ext = "json"

        url = client.upload_query_results(
            json.dumps(data),
            key=f"queries/{query.name}/data.{ext}",
            bucket=MOONSTREAM_S3_PUBLIC_DATA_BUCKET,
        )

        ext = "csv"
        csv_buffer = StringIO()

        dict_csv_writer = csv.DictWriter(
            csv_buffer, fieldnames=data["data"][0].keys(), delimiter=","
        )

        # upload to s3 bucket as csv
        dict_csv_writer.writeheader()
        dict_csv_writer.writerows(data["data"])

        url = client.upload_query_results(
            data=csv_buffer.getvalue().encode("utf-8"),
            key=f"queries/{query.name}/data.{ext}",
            bucket=MOONSTREAM_S3_PUBLIC_DATA_BUCKET,
        )

        logger.info(f"Report uploaded to {url}")


def get_select_ens_handler(args: argparse.Namespace):
    """
    Get ens domains from s3 via S3 select
    """

    s3 = boto3.client("s3")

    response = s3.select_object_content(
        Bucket=MOONSTREAM_S3_PUBLIC_DATA_BUCKET,
        Key="queries/ens_cache/data.csv",
        ExpressionType="SQL",
        Expression=f"select * from s3object s where s.node='{args.node}'",  # type: ignore
        InputSerialization={"CSV": {"FileHeaderInfo": "Use"}},
        OutputSerialization={"CSV": {}},
    )

    #  upack query response
    records = []
    for event in response["Payload"]:
        if "Records" in event:
            records.append(event["Records"]["Payload"])

    print(records)
    #  store unpacked data as a CSV format
    file_str = "".join(req.decode("utf-8") for req in records)

    print(file_str)


def main():
    parser = argparse.ArgumentParser()

    parser.set_defaults(func=lambda _: parser.print_help())

    subparsers = parser.add_subparsers()

    cu_reports_parser = subparsers.add_parser("cu-reports", help="CU Reports")

    cu_reports_subparsers = cu_reports_parser.add_subparsers()

    cu_reports_parser.add_argument(
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

    init_game_bank_parser = queries_subparsers.add_parser(
        "init-game-bank",
        help="Create all predifind query",
        description="Create all predifind query",
    )

    init_game_bank_parser.add_argument("--overwrite", type=bool, default=False)

    init_game_bank_parser.set_defaults(func=init_game_bank_queries_handler)

    init_tokenonomics_parser = queries_subparsers.add_parser(
        "init-tokenonomics",
        help="Create all predifind query",
        description="Create all predifind query",
    )

    init_tokenonomics_parser.add_argument("--overwrite", type=bool, default=False)

    init_tokenonomics_parser.set_defaults(func=init_tokenomics_queries_handler)

    generate_report = queries_subparsers.add_parser(
        "run-tokenonomics",
        help="Run tokenomics queries and push to S3 public backet",
        description="Run tokenomics queries and push to S3 public backet",
    )

    generate_report.set_defaults(func=run_tokenomics_queries_handler)

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

    delete_query.set_defaults(func=delete_user_query_handler)

    create_query = queries_subparsers.add_parser(
        "create",
        help="Create all predifind query",
        description="Create all predifind query",
    )

    create_query.add_argument(
        "--name",
        required=True,
        type=str,
    )

    create_query.set_defaults(func=create_user_query_handler)

    cu_bank_parser = cu_reports_subparsers.add_parser(
        "generate-reports",
        help="Generate cu-bank state reports",
    )

    cu_bank_parser.set_defaults(func=generate_game_bank_report)

    cu_nft_dashboard_parser = cu_reports_subparsers.add_parser(
        "generate-nft-dashboard",
        help="Generate cu-nft-dashboard",
    )
    cu_nft_dashboard_parser.set_defaults(func=generate_report_nft_dashboard_handler)

    ens_parser = cu_reports_subparsers.add_parser("ens", help="ENS commands")

    ens_parser.set_defaults(func=lambda _: ens_parser.print_help())

    ens_subparsers = ens_parser.add_subparsers()

    ens_subparsers.add_parser(
        "generate",
        help="Generate ENS domains",
        description="Generate ENS domains",
    ).set_defaults(func=generate_ens_domains_cache_handler)

    get_select_ens_parser = ens_subparsers.add_parser(
        "get-select",
        help="Get select",
        description="Get select",
    )

    get_select_ens_parser.add_argument(
        "--node",
        type=str,
    )

    get_select_ens_parser.set_defaults(func=get_select_ens_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
