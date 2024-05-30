from __future__ import annotations
from typing import TypeVar, overload

from bot.databases.misc.simple_task import to_task
from ..db_engine import DataBase
from ..misc.error_handler import on_error
from ..misc.adapter_dict import Json

T = TypeVar("T")
engine: DataBase = None


def check_table(func):
    async def wrapped(self: MongoDB, *args, **kwargs):
        if not self.__with_reserved__:
            await self._check_table()
            self.__with_reserved__ = True
        return await func(self, *args, **kwargs)
    return wrapped


class MongoDB:
    __with_reserved__: bool = False

    def __init__(self, table_name: str) -> None:
        self.table_name = table_name

    @to_task
    @on_error()
    async def create(self):
        await engine.execute(
            "INSERT INTO mongo (name) VALUES ($1)",
            (self.table_name, )
        )

    @to_task
    @on_error()
    async def _check_table(self):
        data = await engine.fetchone(
            """SELECT * FROM mongo 
                   WHERE name = $1
                """,
            (self.table_name, )
        )

        if data is None:
            await self.create()

    @overload
    async def get(self, key: str) -> dict | None: ...

    @overload
    async def get(self, key: str, default: T) -> dict | T: ...

    @check_table
    @on_error()
    async def get(self, key: str, default: T = None) -> dict | T:
        key = str(key)
        data = await engine.fetchvalue(
            """
                    SELECT values ->> $1 
                    FROM mongo 
                    WHERE name = $2
                """,
            (key, self.table_name)
        )

        if data is None:
            return default
        return data

    @to_task
    @check_table
    @on_error()
    async def set(self, key, value):
        key = str(key)
        await engine.execute(
            """
                    UPDATE mongo
                    SET values = jsonb_set(values ::jsonb, $1, $2) 
                    WHERE name = $3
                """,
            ('{'+key+'}', value, self.table_name, )
        )
