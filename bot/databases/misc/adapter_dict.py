
from psycopg2.extensions import AsIs
import orjson
from typing import Any, Dict, Union


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
        if not isinstance(data, dict):
            return data
        try:
            return orjson.dumps(data).decode()
        except orjson.JSONEncodeError:
            return data


class NumberFormating:
    @staticmethod
    def encode_number(number: Union[int, float]) -> str:
        return f"__CONVERT_NUMBER__ {number}"

    @staticmethod
    def decode_number(value: Any) -> Any:
        if not (isinstance(value, str) and
                value.startswith("__CONVERT_NUMBER__ ")):
            return value

        try:
            return float(value.removeprefix("__CONVERT_NUMBER__ "))
        except ValueError:
            pass
        try:
            return int(value.removeprefix("__CONVERT_NUMBER__ "))
        except ValueError:
            pass

        return value

    @staticmethod
    def loads(data: Dict[str, Any]):
        if not isinstance(data, dict):
            return data
        new_data = {}
        for key, value in data.items():
            new_data[NumberFormating.decode_number(key)] = value
        return new_data

    @staticmethod
    def dumps(data: dict):
        if not isinstance(data, dict):
            return data
        new_data = {}
        for key in data:
            if isinstance(key, (int, float)):
                new_data[NumberFormating.encode_number(key)] = data[key]
            else:
                new_data[key] = data[key]
        return new_data


def adapt_dict(dict_var):
    data = NumberFormating.dumps(dict_var)
    data = Json.dumps(data)
    return AsIs("'" + data + "'")
