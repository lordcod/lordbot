from typing import Any, TypeVar, overload

T = TypeVar("T")

data = {
    "voice_state": {
        636824998123798531: 3869.29025,
        1150081384099098735: 156.52905,
        819415400772141087: 852.2924,
        1134187898162401291: 1675.241895
    }
}


@overload
def get_table(table_name, default: T) -> T:
    ...


@overload
def get_table(table_name) -> dict:
    ...


def get_table(table_name, default: Any = None) -> Any:
    if table_name not in data:
        data[table_name] = {} if default is None else default
    return data[table_name]


def get(table_name, key, *, default=None):
    table = get_table(table_name)

    return table.get(key, default)


def set(table_name, key, value):
    table = get_table(table_name)

    table[key] = value
