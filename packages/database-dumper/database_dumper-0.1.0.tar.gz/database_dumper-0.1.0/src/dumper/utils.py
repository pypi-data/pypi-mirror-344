import math

from .db_inspector import source_inspector
from .models import Table


TABLE_NAME_INTERVAL = 5

EMPTY_SEP = ' '


def draw(
    table: Table,
    lines: list[str] = None,
    current_line: int = 0,
    sep: list[str] = None,
):
    if lines is None:
        lines = []
    if sep is None:
        sep = []
    if len(lines) - 1 < current_line:
        lines.append('')
        sep.append('')
    for child in table.foreign_tables:
        draw(child, lines, current_line + 1, sep)
    block_len = len(table.name)
    if current_line + 1 < len(lines):
        block_len = max(block_len, len(lines[current_line + 1]) - len(lines[current_line]))
    empty = math.ceil((block_len - len(table.name)) / 2)
    if lines[current_line]:
        lines[current_line] += EMPTY_SEP * TABLE_NAME_INTERVAL
        sep[current_line] += EMPTY_SEP * TABLE_NAME_INTERVAL
    lines[current_line] += EMPTY_SEP * empty + table.name + EMPTY_SEP * empty
    empty += len(table.name) // 2
    sep[current_line] += EMPTY_SEP * empty + '|' + EMPTY_SEP * empty
    i = 1
    while current_line + i < len(lines) and len(lines[current_line]) - len(lines[current_line + i]) > 0:
        diff = len(lines[current_line]) - len(lines[current_line + i]) > 0
        lines[current_line + i] += EMPTY_SEP * diff
        sep[current_line + i] += EMPTY_SEP * diff
    return lines, sep


def get_table_chain(table: Table):
    """
    Generate a string representation of the table chain.
    """

    lines, sep = draw(table)
    result = ['-' * len(lines[0])]
    sep = sep[1:]
    for i, line in enumerate(lines):
        result.append(line)
        if i < len(sep):
            result.append(sep[i])
    result.append('-' * len(lines[0]))
    return '\n'.join(result)


def get_all_related_chain(table: str, schema: str | None = None, *, full_tree: bool) -> Table:
    """
    Build a complete chain of related tables starting from the given table name.

    This function uses a breadth-first search algorithm to find all tables
    related to the given table through foreign key relationships.

    Args:
        table_name: The name of the table to start from

    Returns:
        A Table object representing the root of the relationship tree
    """

    return Table(table, schema).init_foreign(source_inspector, full_tree)
