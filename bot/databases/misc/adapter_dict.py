
from enum import StrEnum
from psycopg2.extensions import AsIs
import orjson
from typing import Any, Dict, Union


class NumberFormatType(StrEnum):
    FLOAT = 'FLOAT'
    INT = 'INTEGER'


class Json:
    @staticmethod
    def loads(data) -> dict:
        if not isinstance(data, str):
            return data
        try:
            return orjson.loads(data)
        except orjson.JSONDecodeError:
            return data

    @staticmethod
    def dumps(data):
        if not isinstance(data, (dict, list)):
            return data
        try:
            return orjson.dumps(data).decode()
        except orjson.JSONEncodeError:
            return data


class NumberFormating:
    @staticmethod
    def encode_number(number: Union[int, float]) -> str:
        if isinstance(number, float):
            return f"__CONVERT_NUMBER__ FLOAT {number}"
        elif isinstance(number, int):
            return f"__CONVERT_NUMBER__ INTEGER {number}"
        return number

    @staticmethod
    def decode_number(value: str) -> Union[int, float]:
        if not (isinstance(value, str) and
                value.startswith("__CONVERT_NUMBER__ ")):
            return value
        numtype = value.split()[1]

        if numtype == NumberFormatType.FLOAT:
            return float(value.removeprefix("__CONVERT_NUMBER__ FLOAT "))
        elif numtype == NumberFormatType.INT:
            return int(value.removeprefix("__CONVERT_NUMBER__ INTEGER "))
        else:
            try:
                return int(value.removeprefix("__CONVERT_NUMBER__ "))
            except ValueError:
                return value

    @staticmethod
    def loads(data: Dict[str, Any]):
        if not isinstance(data, dict):
            return data
        new_data = {}
        for key, value in data.items():
            new_data[NumberFormating.decode_number(
                key)] = NumberFormating.loads(value)
        return new_data

    @staticmethod
    def dumps(data: dict):
        if not isinstance(data, dict):
            return data
        new_data = {}
        for key, value in data.items():
            new_data[NumberFormating.encode_number(
                key)] = NumberFormating.dumps(value)
        return new_data


def adapt_dict(dict_var):
    data = NumberFormating.dumps(dict_var)
    data = Json.dumps(data)
    return AsIs("'" + data + "'")


def adapt_list(list_var):
    data = Json.dumps(list_var)
    return AsIs("'" + data + "'")
