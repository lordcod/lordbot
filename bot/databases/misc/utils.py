from typing import Any, Dict, Union
import ujson as json
from ..db_engine import DataBase


class Json:
    def on_error(func):
        def wrapped(data: Dict[Any, Any]):
            try:
                result = func(data)
                return result
            except:
                return data
        return wrapped

    @on_error
    def loads(data):
        data = json.loads(data)
        return data

    @on_error
    def dumps(data):
        data = json.dumps(data)
        return data


class Formating:
    def on_error(func):
        def wrapped(data: Dict[Any, Any]):
            try:
                result = func(data)
                return result
            except:
                return data
        return wrapped

    @on_error
    def loads(data: Dict[str, Any]):
        new_data = {}
        for key in data:
            value = data[key]
            if key.isdigit:
                new_data[int(key)] = value
            else:
                new_data[key] = value
        return new_data

    @on_error
    def dumps(data: Dict[Union[str, int], Any]):
        new_data = {}
        for key in data:

            if type(key) == int:
                new_data[str(key)] = data[key]
            else:
                new_data[key] = data[key]
        return new_data


def get_info_colums(table_name: str, database: DataBase) -> Union[list, None]:
    query = """
        SELECT
            column_name,
            ordinal_position,
            data_type,
            column_default
        FROM
            information_schema.columns
        WHERE
            table_name = %s;
    """

    info = database.fetchall(query, (table_name,))

    if not info:
        return None

    return list(info)
