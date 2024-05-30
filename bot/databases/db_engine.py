from __future__ import annotations
from typing import Any, Mapping, Optional, Sequence
import asyncpg
from bot.databases.misc.error_handler import on_error
from bot.misc.logger import Logger
from .misc.adapter_dict import adapt_dict, decode_dict


Vars = Sequence[Any] | Mapping[str, Any] | None


class MyConnection(asyncpg.Connection):
    _codecs_installed = False

    async def register_adapter(self) -> None:
        try:
            if self._codecs_installed:
                return
            await self.set_type_codec(
                'json',
                encoder=adapt_dict,
                decoder=decode_dict,
                schema='pg_catalog'
            )
            self._codecs_installed = True
        except Exception as e:
            Logger.error(f'[REGISTER ADAPTER]: {e}')


class DataBase:
    conn_kwargs: dict

    def __init__(self) -> None:
        self.__connection: Optional[asyncpg.Pool] = None

    async def get_connection(self) -> asyncpg.Pool:
        if not self.__connection or self.__connection.is_closing():
            self.__connection = await asyncpg.create_pool(**self.conn_kwargs, command_timeout=60, connection_class=MyConnection)
            Logger.info('Database pool connection opened')
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

    @on_error()
    async def execute(
        self,
        query: str | bytes,
        vars: Vars = None
    ) -> None:
        vars = vars if vars is not None else []
        pool = await self.get_connection()
        con = await pool.acquire()

        try:
            await con.register_adapter()
            await con.execute(query, *vars)
        finally:
            await pool.release(con)

    @on_error()
    async def fetchall(
        self,
        query: str | bytes,
        vars: Vars = None
    ) -> list[tuple[Any, ...]]:
        vars = vars if vars is not None else []
        pool = await self.get_connection()
        con = await pool.acquire()

        try:
            await con.register_adapter()
            return await con.fetch(query, *vars)
        finally:
            await pool.release(con)

    @on_error()
    async def fetchone(
        self,
        query: str | bytes,
        vars: Vars = None
    ) -> tuple[Any, ...] | None:
        vars = vars if vars is not None else []
        pool = await self.get_connection()
        con = await pool.acquire()

        try:
            await con.register_adapter()
            return await con.fetchrow(query, *vars)
        finally:
            await pool.release(con)

    @on_error()
    async def fetchvalue(
        self,
        query: str | bytes,
        vars: Vars = None
    ) -> Any | None:
        vars = vars if vars is not None else []
        pool = await self.get_connection()
        con = await pool.acquire()

        try:
            await con.register_adapter()
            return await con.fetchval(query, *vars)
        finally:
            await pool.release(con)
