from __future__ import annotations
from typing import Any, Mapping, Optional, Sequence
import asyncpg
from bot.misc.logger import Logger
from .misc.adapter_dict import adapt_dict, adapt_list, decode_dict, decode_list


Vars = Sequence[Any] | Mapping[str, Any] | None


class DataBase:
    conn_kwargs: dict

    def __init__(self) -> None:
        self.__connection: Optional[asyncpg.Connection] = None

    async def register_adapter(self) -> None:
        conn = self.__connection
        await conn.set_type_codec(
            'json',
            encoder=adapt_dict,
            decoder=decode_dict,
            schema='pg_catalog'
        )

    async def get_connection(self) -> asyncpg.Connection:
        if not self.__connection or self.__connection.is_closed():
            self.__connection = await asyncpg.connect(**self.conn_kwargs)
            await self.register_adapter()
        return self.__connection

    @classmethod
    async def create_engine(
        cls,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str
    ) -> DataBase:
        Logger.info("Load DataBases")
        conn_kwargs = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database
        }
        self = cls()
        self.conn_kwargs = conn_kwargs
        await self.get_connection()
        return self

    async def execute(
        self,
        query: str | bytes,
        vars: Vars = None
    ) -> None:
        connection = await self.get_connection()
        connection.execute(query, *vars)

    async def fetchall(
        self,
        query: str | bytes,
        vars: Vars = None
    ) -> list[tuple[Any, ...]]:
        connection = await self.get_connection()
        return await connection.fetch(query, *vars)

    async def fetchone(
        self,
        query: str | bytes,
        vars: Vars = None
    ) -> tuple[Any, ...] | None:
        connection = await self.get_connection()
        return await connection.fetchrow(query, *vars)

    async def fetchvalue(
        self,
        query: str | bytes,
        vars: Vars = None
    ) -> Any | None:
        connection = await self.get_connection()
        return await connection.fetchval(query, *vars)
