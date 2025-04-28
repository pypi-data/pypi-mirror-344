import geoalchemy2  # noqa: F401
from sqlalchemy import Table as AlchemyTable
from sqlalchemy import insert, select, text

from .db_inspector import source_engine, source_metadata, target_engine, target_metadata
from .models import Table


def dump_data(table: Table, cut_columns: bool, delete_data: bool):
    for child in table.foreign_tables:
        dump_data(child, cut_columns, delete_data)
    table_name = f'{table.schema}.{table.name}'
    if delete_data:
        with target_engine.connect() as connection:
            connection.execute(text(f'TRUNCATE {table_name} CASCADE'))
            connection.commit()
            print(f'Success truncate {table}')

    source_table = AlchemyTable(table.name, source_metadata, autoload_with=source_engine, schema=table.schema)
    target_table = AlchemyTable(table.name, target_metadata, autoload_with=target_engine, schema=table.schema)
    if cut_columns:
        for col_to_remove in [
            value
            for column, value in source_table._columns.items()  # noqa: SIM118
            if column not in target_table._columns
        ]:
            source_table._columns.remove(col_to_remove)
    with source_engine.connect() as source_conn, target_engine.begin() as target_conn:
        stmt = select(source_table)
        result = source_conn.execute(stmt)
        rows = result.fetchall()

        if not rows:
            print(f"No data to copy in table '{table_name}'")
            return

        insert_stmt = insert(target_table).values([dict(row._mapping) for row in rows])
        target_conn.execute(insert_stmt)

    print(f'Success dump {table}')
