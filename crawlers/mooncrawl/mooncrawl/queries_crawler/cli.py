import argparse
import logging
from datetime import datetime, timezone

from moonstreamdb.blockchain import AvailableBlockchainType

from ..actions import push_data_to_bucket
from ..settings import (
    MOONSTREAM_S3_DATA_BUCKET,
    MOONSTREAM_S3_DATA_BUCKET_PREFIX,
)
from .actions import (
    OutputType,
    fetch_data_from_db,
    fetch_query_from_journal,
    prepare_output,
    query_validation,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parser_queries_execute_handler(args: argparse.Namespace) -> None:
    """
    Execute query from moonstream-queries journal and push to bucket.
    """
    try:
        query = fetch_query_from_journal(query_id=args.id, allow_not_approved=False)
        if args.id != str(query.id):
            raise Exception("Proposed query id is not equal to fetch query (entry id)")

        query_content = query_validation(query.content)
        data_keys, data_rows = fetch_data_from_db(query_id=args.id, query=query_content)

        output = prepare_output(
            output_type=OutputType(args.output),
            data_keys=data_keys,
            data_rows=data_rows,
        )

        if args.output is not None:
            if args.upload:
                bucket_metadata = {"source": "queries-crawler"}
                push_data_to_bucket(
                    data=output,
                    key=f"{MOONSTREAM_S3_DATA_BUCKET_PREFIX}/queries/{str(args.id)}/data.{args.output}",
                    bucket=MOONSTREAM_S3_DATA_BUCKET,
                    metadata=bucket_metadata,
                )
        else:
            print(output)
    except Exception as e:
        logger.error(e)


def main() -> None:
    parser = argparse.ArgumentParser(description="Moonstream query crawlers CLI")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Query crawlers commands")

    time_now = datetime.now(timezone.utc)

    parser_queries_execute = subcommands.add_parser(
        "execute", description="Execute query"
    )
    parser_queries_execute.add_argument(
        "-i",
        "--id",
        required=True,
        help="Query id (entry id in moonstream-queries journal)",
    )
    parser_queries_execute.add_argument(
        "-o",
        "--output",
        default=OutputType.NONE.value,
        help=f"Available output types: {[member.value for member in OutputType]}",
    )
    parser_queries_execute.add_argument(
        "-u",
        "--upload",
        action="store_true",
        help="Set this flag to push output into AWS S3 bucket",
    )
    parser_queries_execute.add_argument(
        "--blockchain",
        required=True,
        help=f"Available blockchain types: {[member.value for member in AvailableBlockchainType]}",
    )
    parser_queries_execute.set_defaults(func=parser_queries_execute_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
