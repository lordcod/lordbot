from __future__ import annotations
from typing import Callable
from psycopg2.extensions import connection as psycoon
from ..misc.error_handler import on_error
from ..misc.utils import Json

connection: Callable[[], psycoon]


class MongoDB:
    def __init__(self, table_name: str) -> None:
        self.table_name = table_name

        self.check_table()

    def create(self):
        with connection().cursor() as cursor:
            cursor.execute(
                """
                    INSERT INTO mongo (name) 
                    VALUES (%s)
                """,
                (self.table_name, )
            )

    def check_table(self):
        with connection().cursor() as cursor:
            cursor.execute(
                """
                    SELECT * 
                    FROM mongo 
                    WHERE name = %s
                """,
                (self.table_name, )
            )

            data = cursor.fetchone()

            if data is None:
                self.create()

    @on_error()
    def get(self, key: str, default=None) -> dict:
        key = str(key)

        with connection().cursor() as cursor:
            cursor.execute(
                """
                    SELECT values ->> %s 
                    FROM mongo 
                    WHERE name = %s
                """,
                (key, self.table_name)
            )

            data = cursor.fetchone()
            if not data[0]:
                return default
            data_new = Json.loads(data[0])
            return data_new

    @on_error()
    def set(self, key, value):
        key = str(key)

        value = Json.dumps(value)
        wkey = (
            '{'
            f'{key}'
            '}'
        )

        with connection().cursor() as cursor:
            cursor.execute(
                """
                    UPDATE 
                        mongo
                    SET 
                        values = jsonb_set(values ::jsonb, %s, %s) 
                    WHERE 
                        name = %s
                """,
                (wkey, value, self.table_name, )
            )
