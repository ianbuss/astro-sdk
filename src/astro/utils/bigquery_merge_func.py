from astro.sql.table import Table


def bigquery_merge_func(
    target_table: Table,
    merge_table: Table,
    merge_keys,
    target_columns,
    merge_columns,
    conflict_strategy,
):
    statement = f"MERGE {target_table.schema}.{target_table.table_name} T USING {merge_table.schema}.{merge_table.table_name} S\
                ON {' AND '.join(['T.'+col +'= S.'+col for col in merge_keys])}\
                WHEN NOT MATCHED BY TARGET THEN INSERT ({','.join(target_columns)}) VALUES ({','.join(merge_columns)})"

    if conflict_strategy == "update":
        update_statement = f"UPDATE SET {', '.join(['T.' + target_columns[index] + '=S.' + merge_columns[index] for index in range(len(target_columns))])}"
        statement += f" WHEN MATCHED THEN {update_statement}"

    return statement, {}
