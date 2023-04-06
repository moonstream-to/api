cu_bank_queries = [
    {
        "name": "cu-bank-blances",
        "query": """
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
            RBW_BALANCE DESC
""",
    },
    {
        "name": "cu-bank-withdrawals-total",
        "query": """
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
    },
    {
        "name": "cu-bank-withdrawals-events",
        "query": """
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
            amount DESC
        """,
    },
]


tokenomics_queries = [
    {
        "name": "volume_change",
        "query": """
            with all_transfers as (
                    select
                        transaction_hash,
                        CASE
                            WHEN type: ='NFT' THEN 1
                            ELSE (label_data->'args'->>'value')::decimal
                        END as value,
                        block_timestamp as block_timestamp
                    from polygon_labels
                        where label='moonworm-alpha'
                            and address= :address
                            and label_data->>'name'='Transfer'
            ), after_range_transfer as (
                select 
                    *
                FROM 
                    all_transfers
                where block_timestamp >= extract(epoch from now() - interval :time_range)::int
            ), current_volume as (
                SELECT
                    sum(all_transfers.value) as value,
                    sum(
                    CASE
                        WHEN to_address in ('0xF715bEb51EC8F63317d66f491E37e7BB048fCc2d','0xfede379e48C873C75F3cc0C81F7C784aD730a8F7','0x00000000006c3852cbef3e08e8df289169ede581')
                        THEN 1
                        else 0
                    END
                    ) as os_sales
                from all_transfers
                    LEFT JOIN polygon_transactions ON all_transfers.transaction_hash = polygon_transactions.hash
            ), volume_different as (
                select 
                    sum(after_range_transfer.value) as value,
                    sum(
                        CASE
                            WHEN to_address in ('0xF715bEb51EC8F63317d66f491E37e7BB048fCc2d','0xfede379e48C873C75F3cc0C81F7C784aD730a8F7','0x00000000006c3852cbef3e08e8df289169ede581')
                            THEN 1
                            else 0
                        END
                    ) as os_sales
                from after_range_transfer
                    LEFT JOIN polygon_transactions ON after_range_transfer.transaction_hash = polygon_transactions.hash
            )
            SELECT
                volume_different.value as diff,
                volume_different.os_sales as os_diff,
                current_volume.value as current,
                current_volume.os_sales as os_current
            from current_volume, volume_different
        """,
    },
    {
        "name": "erc20_721_volume",
        "query": """
    with interval_transfers as (
            select
                transaction_hash,
                CASE
                    WHEN :type ='NFT' THEN 1
                    ELSE (label_data->'args'->>'value')::decimal
                END as value,
                label_data->'args'->>'to' as buyer,
                label_data->'args'->>'from' as seller, 
                to_char(to_timestamp(block_timestamp), :time_format) as time
            from polygon_labels
                where label='moonworm-alpha'
                    and address= :address
                    and label_data->>'name'='Transfer'
                    and block_timestamp >= extract(epoch from now() - interval :time_range)::int
    )
    SELECT
        time as time,
        sum(interval_transfers.value) as value,
        sum(
        CASE
            WHEN to_address in ('0xF715bEb51EC8F63317d66f491E37e7BB048fCc2d','0xfede379e48C873C75F3cc0C81F7C784aD730a8F7','0x00000000006c3852cbef3e08e8df289169ede581')
            THEN 1
            else 0
        END
        ) as os_sales
    from interval_transfers
            LEFT JOIN polygon_transactions ON interval_transfers.transaction_hash = polygon_transactions.hash
            GROUP BY time
    """,
    },
    {
        "name": "erc1155_volume",
        "query": """
    with labels_data as (
        select
            *
        from
            polygon_labels
        where address= :address
        AND label='moonworm-alpha'
        AND block_timestamp >= extract(epoch from now() - interval :time_range)::int
    ),
    nfts_data as (
        select
            transaction_hash,
            label_data->'args'->>'to' as buyer,
            label_data->'args'->>'from' as seller, 
            jsonb_array_elements(label_data -> 'args' -> 'values') :: decimal as value,
            jsonb_array_elements(label_data -> 'args' -> 'ids')->>0 as token_id,
            to_char(to_timestamp(block_timestamp), :time_format) as time
        from
            labels_data
        where
            label_data ->> 'name' = 'TransferBatch'
        UNION ALL
        select
            transaction_hash,
            label_data->'args'->>'to' as buyer,
            label_data->'args'->>'from' as seller, 
            (label_data -> 'args' ->> 'value') :: decimal as value,
            label_data -> 'args' ->> 'id' as token_id,
            to_char(to_timestamp(block_timestamp), :time_format) as time
        from
            labels_data
        where
            label_data ->> 'name' = 'TransferSingle'
    )
        SELECT
            time as time,
            token_id as token_id,
            sum(nfts_data.value) as value,
            sum(
            CASE
                WHEN to_address in ('0xF715bEb51EC8F63317d66f491E37e7BB048fCc2d','0xfede379e48C873C75F3cc0C81F7C784aD730a8F7','0x00000000006c3852cbef3e08e8df289169ede581')
                THEN 1
                else 0
            END
            ) as os_sales
        from nfts_data
            LEFT JOIN polygon_transactions ON nfts_data.transaction_hash = polygon_transactions.hash
        GROUP BY 
            time,
            token_id
        ORDER BY token_id::int, time DESC
""",
    },
    {
        "name": "most_recent_sale",
        "query": """
    with contract_erc721_transfers as (
        select
            transaction_hash,
            label_data->'args'->>'tokenId' as token_id,
            label_data->'args'->>'to' as buyer,
            label_data->'args'->>'from' as seller, 
            block_timestamp as block_timestamp
        from polygon_labels
            where label='moonworm-alpha'
                and address= :address
                and label_data->>'name'='Transfer'
            order by block_number desc
        
    )
    SELECT
        polygon_transactions.hash as transaction_hash,
        contract_erc721_transfers.block_timestamp as block_timestamp,
        contract_erc721_transfers.token_id as token_id,
        contract_erc721_transfers.buyer as buyer,
        contract_erc721_transfers.seller as seller
    from polygon_transactions
        inner JOIN contract_erc721_transfers ON contract_erc721_transfers.transaction_hash = polygon_transactions.hash
    where polygon_transactions.to_address in ('0xF715bEb51EC8F63317d66f491E37e7BB048fCc2d','0xfede379e48C873C75F3cc0C81F7C784aD730a8F7', '0x00000000006c3852cbef3e08e8df289169ede581') 
    limit :amount
""",
    },
    {
        "name": "most_active_buyers",
        "query": """
        with contracts_data as (
            select
                *
            from polygon_labels
                where label='moonworm-alpha'
                    and address= :address
                    and block_timestamp >= extract(epoch from now() - interval :time_range)::int
        ), contract_nfts_transfers as (
            select
                transaction_hash,
                label_data->'args'->>'to' as buyer,
                label_data->'args'->>'from' as seller
            from contracts_data
                where label_data->>'name'='Transfer'
            UNION ALL
            select
                transaction_hash,
                label_data->'args'->>'to' as buyer,
                label_data->'args'->>'from' as seller
            from
                contracts_data
            where
                label_data ->> 'name' = 'TransferBatch'
            UNION ALL
            select
                transaction_hash,
                label_data->'args'->>'to' as buyer,
                label_data->'args'->>'from' as seller
            from
                contracts_data
            where
                label_data ->> 'name' = 'TransferSingle'
            
        )
        SELECT
            contract_nfts_transfers.buyer as buyer,
            count(*) as sale_count
        from polygon_transactions
            inner JOIN contract_nfts_transfers ON contract_nfts_transfers.transaction_hash = polygon_transactions.hash
        where polygon_transactions.to_address in ('0xF715bEb51EC8F63317d66f491E37e7BB048fCc2d','0xfede379e48C873C75F3cc0C81F7C784aD730a8F7','0x00000000006c3852cbEf3e08E8dF289169EdE581') 
        group by contract_nfts_transfers.buyer
        order by sale_count desc
        """,
    },
    {
        "name": "most_active_sellers",
        "query": """
        with contracts_data as (
            select
                *
            from polygon_labels
                where label='moonworm-alpha'
                    and address= :address
                    and block_timestamp >= extract(epoch from now() - interval :time_range)::int
        ), contract_nfts_transfers as (
            select
                transaction_hash,
                label_data->'args'->>'to' as buyer,
                label_data->'args'->>'from' as seller
            from contracts_data
                where label_data->>'name'='Transfer'
            UNION ALL
            select
                transaction_hash,
                label_data->'args'->>'to' as buyer,
                label_data->'args'->>'from' as seller
            from
                contracts_data
            where
                label_data ->> 'name' = 'TransferBatch'
            UNION ALL
            select
                transaction_hash,
                label_data->'args'->>'to' as buyer,
                label_data->'args'->>'from' as seller
            from
                contracts_data
            where
                label_data ->> 'name' = 'TransferSingle'
            
        )
        SELECT
            contract_nfts_transfers.seller as seller,
            count(*) as sale_count
        from polygon_transactions
            inner JOIN contract_nfts_transfers ON contract_nfts_transfers.transaction_hash = polygon_transactions.hash
        where polygon_transactions.to_address in ('0xF715bEb51EC8F63317d66f491E37e7BB048fCc2d','0xfede379e48C873C75F3cc0C81F7C784aD730a8F7','0x00000000006c3852cbEf3e08E8dF289169EdE581') 
        group by contract_nfts_transfers.seller
        order by sale_count desc
        """,
    },
    {
        "name": "lagerst_owners",
        "query": """
        WITH erc_1155_721_contracts_transfers_with_trashhold as (
        SELECT
                label_data as label_data,
                block_timestamp as block_timestamp,
                address as address
            from
                polygon_labels
            WHERE
                polygon_labels.label = 'moonworm-alpha'
                AND polygon_labels.address = :address
                
        ),
        own_erc_1155_721_count as (
            Select
                difference.address,
                (
                    difference.transfers_in - difference.transfers_out
                ) as owned_nfts
            from
                (
                    SELECT
                        total.address,
                        sum(total.transfer_out) as transfers_out,
                        sum(total.transfer_in) as transfers_in
                    from
                        (
                            SELECT
                                label_data -> 'args' ->> 'from' as address,
                                jsonb_array_elements(label_data -> 'args' -> 'values') :: decimal as transfer_out,
                                0 as transfer_in
                            from
                                erc_1155_721_contracts_transfers_with_trashhold
                            where
                                label_data ->> 'name' = 'TransferBatch'
                            UNION
                            ALL
                            SELECT
                                label_data -> 'args' ->> 'from' as address,
                                (label_data -> 'args' ->> 'value') :: decimal as transfer_out,
                                0 as transfer_in
                            from
                                erc_1155_721_contracts_transfers_with_trashhold
                            where
                                label_data ->> 'name' = 'TransferSingle'
                            UNION
                            ALL
                            select
                                label_data -> 'args' ->> 'to' as address,
                                0 as transfer_out,
                                (label_data -> 'args' ->>'value') :: decimal as transfer_in
                            from
                                erc_1155_721_contracts_transfers_with_trashhold
                            where
                                label_data ->> 'name' = 'TransferSingle'
                            UNION
                            ALL
                            select
                                label_data -> 'args' ->> 'to' as address,
                                0 as transfer_out,
                                jsonb_array_elements(label_data -> 'args' -> 'values') :: decimal as transfer_in
                            from
                                erc_1155_721_contracts_transfers_with_trashhold
                            where
                                label_data ->> 'name' = 'TransferBatch'
                            UNION
                            ALL
                            select
                                label_data -> 'args' ->> 'from' as address,
                                1 as transfer_out,
                                0 as transfer_in
                            from
                                erc_1155_721_contracts_transfers_with_trashhold
                                
                            where
                                label_data ->> 'name' = 'Transfer'
                            UNION
                            ALL
                            select
                                label_data -> 'args' ->> 'to' as address,
                                0 as transfer_out,
                                1 as transfer_in
                            from
                                erc_1155_721_contracts_transfers_with_trashhold
                                
                            where
                                label_data ->> 'name' = 'Transfer'
                        ) as total
                    group by
                        address
                ) difference
            order by
                owned_nfts desc
        )
        SELECT
            *
        from
            own_erc_1155_721_count
        WHERE
            address not in (
                '0x000000000000000000000000000000000000dEaD',
                '0x0000000000000000000000000000000000000000'
            )
        order by
            owned_nfts desc
            """,
    },
    {
        "name": "total_supply_erc721",
        "query": """
        select
            count(*) as total_supply
        from(
            SELECT DISTINCT ON((label_data->'args'->>'tokenId')::INT) (label_data->'args'->>'tokenId')::INT as token_id,
                label_data->'args'->>'to' as current_owner
            FROM polygon_labels
            WHERE address = :address
                AND (label = 'moonworm' or label = 'moonworm-alpha')
                AND block_number >= 21418707
                AND label_data->>'type' = 'event'
                AND label_data->>'name' = 'Transfer'
                AND label_data->'args'->>'to' != '0x8d528e98A69FE27b11bb02Ac264516c4818C3942'
                AND label_data->'args'->>'from' != '0x8d528e98A69FE27b11bb02Ac264516c4818C3942'
            ORDER BY (label_data->'args'->>'tokenId')::INT ASC,
                block_number::INT DESC,
                log_index::INT DESC
        ) as total_supply
        where current_owner not in ('0x000000000000000000000000000000000000dEaD','0x0000000000000000000000000000000000000000')
        """,
    },
    {
        "name": "total_supply_terminus",
        "query": """
        WITH erc_1155_721_contracts_transfers_with_trashhold as (
        SELECT
                label_data as label_data,
                block_timestamp as block_timestamp,
                address as address
            from
                polygon_labels
            WHERE
                polygon_labels.label = 'moonworm-alpha'
                AND polygon_labels.address = :address
        ),
        own_erc_1155_721_count as (
            Select

                difference.address,
                token_id,
                (
                    difference.transfers_in - difference.transfers_out
                ) as owned_nfts
            from
                (
                    SELECT
                        total.address,
                        token_id,
                        sum(total.transfer_out) as transfers_out,
                        sum(total.transfer_in) as transfers_in
                    from
                        (
                            SELECT
                                label_data -> 'args' ->> 'from' as address,
                                jsonb_array_elements(label_data -> 'args' -> 'ids')->>0 as token_id,
                                jsonb_array_elements(label_data -> 'args' -> 'values') :: decimal as transfer_out,
                                0 as transfer_in
                            from
                                erc_1155_721_contracts_transfers_with_trashhold
                            where
                                label_data ->> 'name' = 'TransferBatch'
                            UNION
                            ALL
                            SELECT
                                label_data -> 'args' ->> 'from' as address,
                                label_data -> 'args' ->> 'id' as token_id,
                                (label_data -> 'args' ->> 'value') :: decimal as transfer_out,
                                0 as transfer_in
                            from
                                erc_1155_721_contracts_transfers_with_trashhold
                            where
                                label_data ->> 'name' = 'TransferSingle'
                            UNION
                            ALL
                            select
                                label_data -> 'args' ->> 'to' as address,
                                label_data -> 'args' ->> 'id' as token_id,
                                0 as transfer_out,
                                (label_data -> 'args' ->>'value') :: decimal as transfer_in
                            from
                                erc_1155_721_contracts_transfers_with_trashhold
                            where
                                label_data ->> 'name' = 'TransferSingle'
                            UNION
                            ALL
                            select
                                label_data -> 'args' ->> 'to' as address,
                                jsonb_array_elements(label_data -> 'args' -> 'ids')->>0 as token_id,
                                0 as transfer_out,
                                jsonb_array_elements(label_data -> 'args' -> 'values') :: decimal as transfer_in
                            from
                                erc_1155_721_contracts_transfers_with_trashhold
                            where
                                label_data ->> 'name' = 'TransferBatch'
                        ) as total
                    group by
                        address, token_id
                ) difference
            order by
                owned_nfts desc
        )
        SELECT
            token_id as token_id,
            sum(owned_nfts) as total_supply
        from
            own_erc_1155_721_count
        WHERE
            address not in (
                '0x000000000000000000000000000000000000dEaD',
                '0x0000000000000000000000000000000000000000'
            )
        group by
            token_id
        order by
            token_id::int desc
        """,
    },
]


tokenomics_orange_dao_queries = [
    {
        "name": "balances_by_address",
        "query": """
        select
            address,
            transfers_in - transfers_out as balance
            from (
                SELECT transfer_in_out_erc20.address as address,
                    sum(transfer_in_out_erc20.transfer_out) as transfers_out,
                    sum(transfer_in_out_erc20.transfer_in) as transfers_in
                from (
                        SELECT label_data->'args'->>'from' as address,
                            (label_data->'args'->>'value')::decimal as transfer_out,
                            0 as transfer_in
                        from ethereum_labels
                        where label_data->>'name' = 'Transfer'
                            and label = 'moonworm-alpha'
                            and address =  '0x1bBD79f1Ecb3f2cCC586A5E3A26eE1d1D2E1991f'
                        UNION ALL
                        select label_data->'args'->>'to' as address,
                            0 as transfer_out,
                            (label_data->'args'->>'value')::decimal as transfer_in
                        from ethereum_labels
                        where label_data->>'name' = 'Transfer'
                            and label = 'moonworm-alpha'
                            and address = '0x1bBD79f1Ecb3f2cCC586A5E3A26eE1d1D2E1991f'
                    ) as transfer_in_out_erc20
                group by address
            ) as full_erc20
        """,
    },
    {
        "name": "transfers_feed",
        "query": """
            select
                transaction_hash,
                label_data -> 'args' ->> 'value' as value,
                label_data -> 'args' ->> 'from' as from_address,
                label_data -> 'args' ->> 'to' as to_address,
                block_timestamp as block_timestamp
            from
                ethereum_labels
            where
                label = 'moonworm-alpha'
                and address = '0x1bBD79f1Ecb3f2cCC586A5E3A26eE1d1D2E1991f'
                and label_data ->> 'name' = 'Transfer'
                and block_timestamp >= extract(epoch from now() - interval :time_range)::int;
        """,
    },
    {
        "name": "largest_distributors",
        "query": """
        select
            address,
            transfers_out as transfers_out
            from (
                SELECT transfer_in_out_erc20.address as address,
                    sum(transfer_in_out_erc20.transfer_out) as transfers_out,
                    sum(transfer_in_out_erc20.transfer_in) as transfers_in
                from (
                        SELECT label_data->'args'->>'from' as address,
                            (label_data->'args'->>'value')::decimal as transfer_out,
                            0 as transfer_in
                        from ethereum_labels
                        where label_data->>'name' = 'Transfer'
                            and label = 'moonworm-alpha'
                            and address =  '0x1bBD79f1Ecb3f2cCC586A5E3A26eE1d1D2E1991f'
                        UNION ALL
                        select label_data->'args'->>'to' as address,
                            0 as transfer_out,
                            (label_data->'args'->>'value')::decimal as transfer_in
                        from ethereum_labels
                        where label_data->>'name' = 'Transfer'
                            and label = 'moonworm-alpha'
                            and address = '0x1bBD79f1Ecb3f2cCC586A5E3A26eE1d1D2E1991f'
                    ) as transfer_in_out_erc20
                group by address
            ) as full_erc20
        order by transfers_out desc
        limit :limit;
        """,
    },
    {
        "name": "largest_recipients",
        "query": """
        select
            address,
            transfers_in as transfers_in
            from (
                SELECT transfer_in_out_erc20.address as address,
                    sum(transfer_in_out_erc20.transfer_out) as transfers_out,
                    sum(transfer_in_out_erc20.transfer_in) as transfers_in
                from (
                        SELECT label_data->'args'->>'from' as address,
                            (label_data->'args'->>'value')::decimal as transfer_out,
                            0 as transfer_in
                        from ethereum_labels
                        where label_data->>'name' = 'Transfer'
                            and label = 'moonworm-alpha'
                            and address =  '0x1bBD79f1Ecb3f2cCC586A5E3A26eE1d1D2E1991f'
                        UNION ALL
                        select label_data->'args'->>'to' as address,
                            0 as transfer_out,
                            (label_data->'args'->>'value')::decimal as transfer_in
                        from ethereum_labels
                        where label_data->>'name' = 'Transfer'
                            and label = 'moonworm-alpha'
                            and address = '0x1bBD79f1Ecb3f2cCC586A5E3A26eE1d1D2E1991f'
                    ) as transfer_in_out_erc20
                group by address
            ) as full_erc20
        order by transfers_in desc
        limit :limit;
        """,
    },
]
