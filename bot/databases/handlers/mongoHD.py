from __future__ import annotations
from typing import TypeVar, overload
from ..db_engine import DataBase
from ..misc.error_handler import on_error
from ..misc.adapter_dict import Json

T = TypeVar("T")
engine: DataBase = None


class MongoDB:
    def __init__(self, table_name: str) -> None:
        self.table_name = table_name

        self.check_table()

    def create(self):
        engine.execute(
            "INSERT INTO mongo (name) VALUES (%s)",
            (self.table_name, )
        )

    def check_table(self):
        data = engine.fetchone(
            """SELECT * FROM mongo 
                   WHERE name = %s
                """,
            (self.table_name, )
        )

        if data is None:
            self.create()

    @overload
    def get(self, key: str) -> dict | None: ...

    @overload
    def get(self, key: str, default: T) -> dict | T: ...

    @on_error()
    def get(self, key: str, default: T = None) -> dict | T:
        key = str(key)

        data = engine.fetchone(
            """
                    SELECT values ->> %s 
                    FROM mongo 
                    WHERE name = %s
                """,
            (key, self.table_name)
        )

        if not data[0]:
            return default
        data_new = Json.loads(data[0])
        return data_new

    @on_error()
    def set(self, key, value):
        key = str(key)

        value = Json.dumps(value)

        engine.execute(
            """
                    UPDATE mongo
                    SET values = jsonb_set(values ::jsonb, %s, %s) 
                    WHERE name = %s
                """,
            ('{'+key+'}', value, self.table_name, )
        )
