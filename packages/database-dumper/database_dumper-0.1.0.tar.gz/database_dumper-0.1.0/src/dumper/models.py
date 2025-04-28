from __future__ import annotations

from typing import Any


def _str_list(value: str | list[str]) -> list[str]:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [value]
    raise ValueError('Wrong usage: value must be a string or list of strings')


class Table:
    """
    Represents a database table and its relationships.

    This class is used to build a tree of related tables based on foreign key relationships.
    It tracks parent-child relationships and provides methods to add foreign key relationships
    and check if a table is already in the relationship tree.
    """

    def __init__(self, name: str, schema: str = None) -> None:
        self.name = name
        self.schema = schema or 'public'
        self.parent: Table | None = None
        self.parent_columns: list[str] | None = None
        self.related_columns: list[str] | None = None
        self.root = self
        self._foreign_tables: list[Table] = []

    @property
    def foreign_tables(self) -> list[Table]:
        """
        Get the list of foreign tables related to this table.

        Returns:
            A list of Table objects representing the foreign tables
        """
        return self._foreign_tables

    def add_foreign(self, table: Table, table_columns: str | list[str], foreign_columns: str | list[str]) -> None:
        """
        Add a foreign table relationship to this table.

        Args:
            table: The foreign table
            table_columns: The columns in this table that reference the foreign table
            foreign_columns: The columns in the foreign table that are referenced

        Raises:
            ValueError: If the number of table columns and foreign columns don't match
        """
        table_columns, foreign_columns = _str_list(table_columns), _str_list(foreign_columns)
        if len(table_columns) == len(foreign_columns):
            table.parent_columns = table_columns
            table.related_columns = foreign_columns
            table.parent = self
            table.root = self.root
            self._foreign_tables.append(table)
        else:
            raise ValueError('table_columns and foreign_columns must have same columns count')

    def has_table(self, table: Table) -> bool:
        """
        Check if a table is already in the relationship tree.

        Args:
            table: The table to check

        Returns:
            True if the table is in the tree, False otherwise
        """
        return (self.name == table.name and self.schema == table.schema) or any(
            t.has_table(table) for t in self.foreign_tables
        )

    def init_foreign(self, inspector: Any, full_tree: bool) -> Table:
        """
        Initialize foreign key relationships for this table using the SQLAlchemy inspector.

        Args:
            inspector: The SQLAlchemy inspector object

        Returns:
            This table instance with foreign key relationships initialized
        """
        foreign_tables = inspector.get_foreign_keys(self.name, self.schema)
        for table in foreign_tables:
            new_table = Table(table['referred_table'], table['referred_schema'])
            if not self.root.has_table(new_table) or full_tree:
                self.add_foreign(
                    new_table,
                    table['constrained_columns'],
                    table['referred_columns'],
                )
            new_table.init_foreign(inspector, full_tree)
        return self

    def __repr__(self) -> str:
        return f'Table(name={self.name}, schema={self.schema})'
