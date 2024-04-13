from typing import Any, TypeVar, overload

data = {}
T = TypeVar("T")


@overload
def get_table(table_name: str, default: T) -> T:
    pass


@overload
def get_table(table_name: str) -> dict:
    pass


def get_table(table_name, default: Any = None):
    data.setdefault(table_name, default)
    return data[table_name]


def get(table_name, key, *, default=None):
    table = get_table(table_name)

    return table.get(key, default)


def set(table_name, key, value):
    table = get_table(table_name)

    table[key] = value
