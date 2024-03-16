data = {}


def get_table(table_name) -> dict:
    data.setdefault(table_name, {})
    return data[table_name]


def get(table_name, key, *, default=None):
    table = get_table(table_name)

    return table.get(key, default)


def set(table_name, key, value):
    table = get_table(table_name)

    table[key] = value
