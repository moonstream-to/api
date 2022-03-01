import logging
import os
import json
from typing import Any, Dict, List, Optional, Union
import traceback

import boto3  # type: ignore
from moonstreamdb.db import yield_db_session_ctx
from sqlalchemy.orm import Session

from . import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def push_statistics(s3: Any, data: Any, key: str, bucket: str) -> None:

    s3.put_object(
        Body=data,
        Bucket=bucket,
        Key=key,
        ContentType="application/json",
        Metadata={"leaderboard_query": "data"},
    )

    logger.info(f"Statistics push to bucket: s3://{bucket}/{key}")


def main():

    retry_count = 7
    full_count = 0

    MOONSTREAM_CU_LEADERBOARD_QUERY = os.environ.get(
        "MOONSTREAM_CU_LEADERBOARD_QUERY",
        "With small_bottle_size as ( select 250 as unim_voluem, 5 as pool_id ), medium_bottle_size as ( select 2500 as unim_voluem, 6 as pool_id ), big_bottle_size as ( select 25000 as unim_voluem, 7 as pool_id ), polygon_labels_with_time_treshold as ( SELECT * from polygon_labels where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' ), small_bottle_UNIM_balance_per_address as ( Select difference.address, ( difference.transfers_in - difference.transfers_out ) * small_bottle_size.unim_voluem as count from ( SELECT total.address, sum(total.transfer_out) as transfers_out, sum(total.transfer_in) as transfers_in from ( /* From transactions in batch / SELECT label_data->'args'->>'from' as address, (label_data->'args'->'values'->>0)::int as transfer_out, 0 as transfer_in from polygon_labels_with_time_treshold, small_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferBatch' and (label_data->'args'->'ids'->>0)::int = small_bottle_size.pool_id UNION ALL / From transactions single / SELECT label_data->'args'->>'from' as address, (label_data->'args'->'value')::int as transfer_out, 0 as transfer_in from polygon_labels_with_time_treshold, small_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferSingle' and (label_data->'args'->>'id')::int = small_bottle_size.pool_id UNION ALL / To transactions single / select label_data->'args'->>'to' as address, 0 as transfer_out, (label_data->'args'->>'value')::int as transfer_in from polygon_labels_with_time_treshold, small_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferSingle' and (label_data->'args'->>'id')::int = small_bottle_size.pool_id UNION ALL / To transactions batch */ select label_data->'args'->>'to' as address, 0 as transfer_out, (label_data->'args'->'values'->>0)::int as transfer_in from polygon_labels_with_time_treshold, small_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferBatch' and (label_data->'args'->'ids'->>0)::int = small_bottle_size.pool_id ) as total group by address ) difference, small_bottle_size order by count desc ), medium_bottle_UNIM_balance_per_address as ( Select difference.address, ( difference.transfers_in - difference.transfers_out ) * medium_bottle_size.unim_voluem as count from ( SELECT total.address, sum(total.transfer_out) as transfers_out, sum(total.transfer_in) as transfers_in from ( /* From transactions in batch / SELECT label_data->'args'->>'from' as address, (label_data->'args'->'values'->>0)::int as transfer_out, 0 as transfer_in from polygon_labels_with_time_treshold, medium_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferBatch' and (label_data->'args'->'ids'->>0)::int = medium_bottle_size.pool_id UNION ALL / From transactions single / SELECT label_data->'args'->>'from' as address, (label_data->'args'->'value')::int as transfer_out, 0 as transfer_in from polygon_labels_with_time_treshold, medium_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferSingle' and (label_data->'args'->>'id')::int = medium_bottle_size.pool_id UNION ALL / To transactions single / select label_data->'args'->>'to' as address, 0 as transfer_out, (label_data->'args'->>'value')::int as transfer_in from polygon_labels_with_time_treshold, medium_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferSingle' and (label_data->'args'->>'id')::int = medium_bottle_size.pool_id UNION ALL / To transactions batch */ select label_data->'args'->>'to' as address, 0 as transfer_out, (label_data->'args'->'values'->>0)::int as transfer_in from polygon_labels_with_time_treshold, medium_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferBatch' and (label_data->'args'->'ids'->>0)::int = medium_bottle_size.pool_id ) as total group by address ) difference, medium_bottle_size order by count desc ), big_bottle_UNIM_balance_per_address as ( Select difference.address, ( difference.transfers_in - difference.transfers_out ) * big_bottle_size.unim_voluem as count from ( SELECT total.address, sum(total.transfer_out) as transfers_out, sum(total.transfer_in) as transfers_in from ( /* From transactions in batch / SELECT label_data->'args'->>'from' as address, (label_data->'args'->'values'->>0)::int as transfer_out, 0 as transfer_in from polygon_labels_with_time_treshold, big_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferBatch' and (label_data->'args'->'ids'->>0)::int = big_bottle_size.pool_id UNION ALL / From transactions single / SELECT label_data->'args'->>'from' as address, (label_data->'args'->'value')::int as transfer_out, 0 as transfer_in from polygon_labels_with_time_treshold, big_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferSingle' and (label_data->'args'->>'id')::int = big_bottle_size.pool_id UNION ALL / To transactions single / select label_data->'args'->>'to' as address, 0 as transfer_out, (label_data->'args'->>'value')::int as transfer_in from polygon_labels_with_time_treshold, big_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferSingle' and (label_data->'args'->>'id')::int = big_bottle_size.pool_id UNION ALL / To transactions batch */ select label_data->'args'->>'to' as address, 0 as transfer_out, (label_data->'args'->'values'->>0)::int as transfer_in from polygon_labels_with_time_treshold, big_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferBatch' and (label_data->'args'->'ids'->>0)::int = big_bottle_size.pool_id ) as total group by address ) difference, big_bottle_size order by count desc ), amount_in_bottle as ( SELECT bottled_UNIM.address as address, sum(bottled_UNIM.count) as bottled_UNIM_voluem from ( select * from small_bottle_UNIM_balance_per_address UNION ALL select * from medium_bottle_UNIM_balance_per_address UNION ALL select * from big_bottle_UNIM_balance_per_address ) as bottled_UNIM where address NOT IN ('0xb5a4b925005b59c9c04fbf2742aee3b80834089f') /* BLACK LIST */ group by bottled_UNIM.address order by bottled_UNIM_voluem desc ) select (unim_balance_per_address.address)::text as address, (transfers_in - transfers_out)::INT as unim_balance, DENSE_RANK () over ( ORDER BY (transfers_in - transfers_out)::INT DESC) as rank from ( SELECT full_unim.address as address, sum(full_unim.transfer_out) as transfers_out, sum(full_unim.transfer_in) as transfers_in from ( SELECT label_data->'args'->>'from' as address, case when LEFT(label_data->'args'->>'value', -18) != '' then LEFT(label_data->'args'->>'value', -18)::INT else 0 end as transfer_out, 0 as transfer_in from polygon_labels where label_data->>'name' = 'Transfer' and address = '0x64060aB139Feaae7f06Ca4E63189D86aDEb51691' UNION ALL select label_data->'args'->>'to' as address, 0 as transfer_out, case when LEFT(label_data->'args'->>'value', -18) != '' then LEFT(label_data->'args'->>'value', -18)::INT else 0 end as transfer_in from polygon_labels where label_data->>'name' = 'Transfer' and address = '0x64060aB139Feaae7f06Ca4E63189D86aDEb51691' UNION ALL select address as address, 0 as transfer_out, bottled_UNIM_voluem as transfer_in from amount_in_bottle where bottled_UNIM_voluem > 0 ) as full_unim group by address ) unim_balance_per_address where (transfers_in - transfers_out)::INT > 0 order by unim_balance desc;",
    )

    MOONSTREAM_CU_LEADERBOARD_NTILES_QUERY = os.environ.get(
        "MOONSTREAM_CU_LEADERBOARD_NTILES_QUERY",
        "With small_bottle_size as (     select 250 as unim_voluem,         5 as pool_id ), medium_bottle_size as (     select 2500 as unim_voluem,         6 as pool_id ), big_bottle_size as (     select 25000 as unim_voluem,         7 as pool_id ), polygon_labels_with_time_treshold as (     SELECT *     from polygon_labels     where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' ), small_bottle_UNIM_balance_per_address as (     Select difference.address,         (             difference.transfers_in - difference.transfers_out         ) * small_bottle_size.unim_voluem as count     from (             SELECT total.address,                 sum(total.transfer_out) as transfers_out,                 sum(total.transfer_in) as transfers_in             from (                     /* From transactions in batch / SELECT label_data->'args'->>'from' as address, (label_data->'args'->'values'->>0)::int as transfer_out, 0 as transfer_in from polygon_labels_with_time_treshold, small_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferBatch' and (label_data->'args'->'ids'->>0)::int = small_bottle_size.pool_id UNION ALL / From transactions single / SELECT label_data->'args'->>'from' as address, (label_data->'args'->'value')::int as transfer_out, 0 as transfer_in from polygon_labels_with_time_treshold, small_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferSingle' and (label_data->'args'->>'id')::int = small_bottle_size.pool_id UNION ALL / To transactions single / select label_data->'args'->>'to' as address, 0 as transfer_out, (label_data->'args'->>'value')::int as transfer_in from polygon_labels_with_time_treshold, small_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferSingle' and (label_data->'args'->>'id')::int = small_bottle_size.pool_id UNION ALL / To transactions batch */                     select label_data->'args'->>'to' as address,                         0 as transfer_out,                         (label_data->'args'->'values'->>0)::int as transfer_in                     from polygon_labels_with_time_treshold,                         small_bottle_size                     where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796'                         and label = 'moonworm-alpha'                         and label_data->>'name' = 'TransferBatch'                         and (label_data->'args'->'ids'->>0)::int = small_bottle_size.pool_id                 ) as total             group by address         ) difference,         small_bottle_size     order by count desc ), medium_bottle_UNIM_balance_per_address as (     Select difference.address,         (             difference.transfers_in - difference.transfers_out         ) * medium_bottle_size.unim_voluem as count     from (             SELECT total.address,                 sum(total.transfer_out) as transfers_out,                 sum(total.transfer_in) as transfers_in             from (                     /* From transactions in batch / SELECT label_data->'args'->>'from' as address, (label_data->'args'->'values'->>0)::int as transfer_out, 0 as transfer_in from polygon_labels_with_time_treshold, medium_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferBatch' and (label_data->'args'->'ids'->>0)::int = medium_bottle_size.pool_id UNION ALL / From transactions single / SELECT label_data->'args'->>'from' as address, (label_data->'args'->'value')::int as transfer_out, 0 as transfer_in from polygon_labels_with_time_treshold, medium_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferSingle' and (label_data->'args'->>'id')::int = medium_bottle_size.pool_id UNION ALL / To transactions single / select label_data->'args'->>'to' as address, 0 as transfer_out, (label_data->'args'->>'value')::int as transfer_in from polygon_labels_with_time_treshold, medium_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferSingle' and (label_data->'args'->>'id')::int = medium_bottle_size.pool_id UNION ALL / To transactions batch */                     select label_data->'args'->>'to' as address,                         0 as transfer_out,                         (label_data->'args'->'values'->>0)::int as transfer_in                     from polygon_labels_with_time_treshold,                         medium_bottle_size                     where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796'                         and label = 'moonworm-alpha'                         and label_data->>'name' = 'TransferBatch'                         and (label_data->'args'->'ids'->>0)::int = medium_bottle_size.pool_id                 ) as total             group by address         ) difference,         medium_bottle_size     order by count desc ), big_bottle_UNIM_balance_per_address as (     Select difference.address,         (             difference.transfers_in - difference.transfers_out         ) * big_bottle_size.unim_voluem as count     from (             SELECT total.address,                 sum(total.transfer_out) as transfers_out,                 sum(total.transfer_in) as transfers_in             from (                     /* From transactions in batch / SELECT label_data->'args'->>'from' as address, (label_data->'args'->'values'->>0)::int as transfer_out, 0 as transfer_in from polygon_labels_with_time_treshold, big_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferBatch' and (label_data->'args'->'ids'->>0)::int = big_bottle_size.pool_id UNION ALL / From transactions single / SELECT label_data->'args'->>'from' as address, (label_data->'args'->'value')::int as transfer_out, 0 as transfer_in from polygon_labels_with_time_treshold, big_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferSingle' and (label_data->'args'->>'id')::int = big_bottle_size.pool_id UNION ALL / To transactions single / select label_data->'args'->>'to' as address, 0 as transfer_out, (label_data->'args'->>'value')::int as transfer_in from polygon_labels_with_time_treshold, big_bottle_size where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796' and label = 'moonworm-alpha' and label_data->>'name' = 'TransferSingle' and (label_data->'args'->>'id')::int = big_bottle_size.pool_id UNION ALL / To transactions batch */                     select label_data->'args'->>'to' as address,                         0 as transfer_out,                         (label_data->'args'->'values'->>0)::int as transfer_in                     from polygon_labels_with_time_treshold,                         big_bottle_size                     where address = '0x062BEc5e84289Da2CD6147E0e4DA402B33B8f796'                         and label = 'moonworm-alpha'                         and label_data->>'name' = 'TransferBatch'                         and (label_data->'args'->'ids'->>0)::int = big_bottle_size.pool_id                 ) as total             group by address         ) difference,         big_bottle_size     order by count desc ), amount_in_bottle as (     SELECT bottled_UNIM.address as address,         sum(bottled_UNIM.count) as bottled_UNIM_voluem     from (             select *             from small_bottle_UNIM_balance_per_address             UNION ALL             select *             from medium_bottle_UNIM_balance_per_address             UNION ALL             select *             from big_bottle_UNIM_balance_per_address         ) as bottled_UNIM     where address NOT IN ('0xb5a4b925005b59c9c04fbf2742aee3b80834089f')         /* BLACK LIST */     group by bottled_UNIM.address     order by bottled_UNIM_voluem desc ), leaderboard as (select (unim_balance_per_address.address)::text as address,     (transfers_in - transfers_out)::INT as unim_balance,     DENSE_RANK () over (         ORDER BY (transfers_in - transfers_out)::INT DESC     ) as rank from (         SELECT full_unim.address as address,             sum(full_unim.transfer_out) as transfers_out,             sum(full_unim.transfer_in) as transfers_in         from (                 SELECT label_data->'args'->>'from' as address,                     case                         when LEFT(label_data->'args'->>'value', -18) != '' then LEFT(label_data->'args'->>'value', -18)::INT                         else 0                     end as transfer_out,                     0 as transfer_in                 from polygon_labels                 where label_data->>'name' = 'Transfer'                     and address = '0x64060aB139Feaae7f06Ca4E63189D86aDEb51691'                 UNION ALL                 select label_data->'args'->>'to' as address,                     0 as transfer_out,                     case                         when LEFT(label_data->'args'->>'value', -18) != '' then LEFT(label_data->'args'->>'value', -18)::INT                         else 0                     end as transfer_in                 from polygon_labels                 where label_data->>'name' = 'Transfer'                     and address = '0x64060aB139Feaae7f06Ca4E63189D86aDEb51691'                 UNION ALL                 select address as address,                     0 as transfer_out,                     bottled_UNIM_voluem as transfer_in                 from amount_in_bottle                 where bottled_UNIM_voluem > 0             ) as full_unim         group by address     ) unim_balance_per_address where (transfers_in - transfers_out)::INT > 0 order by unim_balance desc), maximum as (     select max(leaderboard.rank) as max_rank from leaderboard ), leaderboard_counted_ntile as ( select  ranked_board.address as address,         ranked_board.unim_balance as balance,         ranked_board.rank as rank,         ranked_board.category as category,         ROW_NUMBER() over (             partition by category             ORDER BY rank desc         ) as number_in_category from (     select leaderboard.address,         leaderboard.unim_balance,         leaderboard.rank,             (case when CAST(leaderboard.rank as REAL) / maximum.max_rank < 0.25 then 1                 when CAST(leaderboard.rank as REAL) / maximum.max_rank < 0.50 then 2                 when CAST(leaderboard.rank as REAL) / maximum.max_rank < 0.75 then 3                 else 4             end) as category     from          leaderboard, maximum ) ranked_board order by rank, address  ) select leaderboard_counted_ntile.address,        leaderboard_counted_ntile.balance as balance,        leaderboard_counted_ntile.rank     from leaderboard_counted_ntile         where leaderboard_counted_ntile.category in (1,2,3)               and leaderboard_counted_ntile.number_in_category = 1  ;   /* ,  */",
    )

    if MOONSTREAM_CU_LEADERBOARD_QUERY == "":
        raise Exception("MOONSTREAM_CU_LEADERBOARD_QUERY env variable is not set")

    db_session: Session = yield_db_session_ctx()

    s3 = boto3.client("s3")

    while full_count < retry_count:

        try:

            # Leaderboards generate
            with yield_db_session_ctx() as db_session:

                ntiles_dict = {}

                ntiles_label = ("25%", "50%", "75%")

                ntiles = db_session.execute(MOONSTREAM_CU_LEADERBOARD_NTILES_QUERY)

                for index, netile in enumerate(ntiles):

                    ntiles_dict[ntiles_label[index]] = dict(netile)

                block_number, block_timestamp = db_session.execute(
                    "SELECT block_number, block_timestamp FROM polygon_labels WHERE block_number=(SELECT max(block_number) FROM polygon_labels where label='moonworm-alpha') limit 1;",
                ).one()

                rows_as_dict = [
                    dict(row)
                    for row in db_session.execute(MOONSTREAM_CU_LEADERBOARD_QUERY, {})
                ]

                full_leaderboard_data = {
                    "block_number": block_number,
                    "block_timestamp": block_timestamp,
                    "total": sum([account["unim_balance"] for account in rows_as_dict]),
                    "data": rows_as_dict,
                }

                full_leaderboard_data.update(ntiles_dict)
                data = json.dumps(full_leaderboard_data).encode("utf-8")

                print(
                    f"{settings.MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET}/LEADERBOARD_DATA/FULL_LIST.json"
                )

                push_statistics(
                    s3=s3,
                    data=data,
                    key=f"LEADERBOARD_DATA/FULL_LIST.json",
                    bucket=settings.MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET,
                )

                # indexing file

                # Leaderboards generate

                data = json.dumps(
                    {
                        "block_number": block_number,
                        "block_timestamp": block_timestamp,
                        "data": {
                            account["address"]: {
                                "unim_balance": account["unim_balance"],
                                "rank": account["rank"],
                                "position": index,
                            }
                            for index, account in enumerate(rows_as_dict)
                        },
                    }
                ).encode("utf-8")

                push_statistics(
                    s3=s3,
                    data=data,
                    key=f"LEADERBOARD_DATA/IMDEX_FILE.json",
                    bucket=settings.MOONSTREAM_S3_SMARTCONTRACTS_ABI_BUCKET,
                )

                break

        except Exception as e:
            traceback.print_exc()
            full_count += 1
            logger.error(f"Exception happen on generation time {e}")
            if full_count >= retry_count:
                raise BaseException("Stats not updated")


if __name__ == "__main__":
    main()
