from __future__ import annotations
import asyncio
import functools
import logging
from typing import Any, Mapping, Optional, Sequence
import psycopg2
import psycopg2._json
import psycopg2.extras
from bot.databases.misc.error_handler import on_error
from .misc.adapter_dict import adapt_dict, decode_dict


_lock = asyncio.Lock()
_log = logging.getLogger(__name__)

Vars = Sequence[Any] | Mapping[str, Any] | None

psycopg2.extensions.register_adapter(dict, adapt_dict)
psycopg2.extensions.register_adapter(list, adapt_dict)
psycopg2._json.register_default_json(loads=decode_dict)
psycopg2._json.register_default_jsonb(loads=decode_dict)


def on_lock_complete(func):
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        async with _lock:
            return await func(*args, **kwargs)
    return wrapped


class DataBase:
    conn_url: str

    def __init__(self) -> None:
        self.__connection: Optional[psycopg2.extensions.connection] = None

    async def get_connection(self):
        if not self.__connection or self.__connection.closed:
            self.__connection = psycopg2.connect(self.conn_url)
            self.__connection.autocommit = True
            _log.debug('Database pool connection opened')
        return self.__connection

    @classmethod
    async def create_engine(
        cls,
        url: str
    ) -> DataBase:
        _log.debug("Load DataBases")
        self = cls()
        self.conn_url = url
        await self.get_connection()
        return self

    @on_error()
    @on_lock_complete
    async def execute(
        self,
        query: str | bytes,
        vars: Vars = None
    ) -> None:
        vars = vars if vars is not None else []
        conn = await self.get_connection()

        with conn.cursor() as cursor:
            cursor.execute(query, vars)

    @on_error()
    @on_lock_complete
    async def fetchall(
        self,
        query: str | bytes,
        vars: Vars = None
    ) -> list[tuple[Any, ...]]:
        vars = vars if vars is not None else []
        conn = await self.get_connection()

        with conn.cursor() as cursor:
            cursor.execute(query, vars)
            return cursor.fetchall()

    @on_error()
    @on_lock_complete
    async def fetchone(
        self,
        query: str | bytes,
        vars: Vars = None
    ) -> tuple[Any, ...] | None:
        vars = vars if vars is not None else []
        conn = await self.get_connection()

        with conn.cursor() as cursor:
            cursor.execute(query, vars)
            return cursor.fetchone()

    @on_error()
    @on_lock_complete
    async def fetchvalue(
        self,
        query: str | bytes,
        vars: Vars = None
    ) -> Any | None:
        vars = vars if vars is not None else []
        conn = await self.get_connection()

        with conn.cursor() as cursor:
            cursor.execute(query, vars)
            data = cursor.fetchone()

            if data is None:
                return

            return data[0]

    @on_error()
    @on_lock_complete
    async def fetchone_dict(
        self,
        query: str | bytes,
        vars: Vars = None
    ) -> dict:
        vars = vars if vars is not None else []
        conn = await self.get_connection()

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(query, vars)
            val = cursor.fetchone()
            if val is None:
                return None
            return dict(val)


# class MyConnection(asyncpg.Connection):
#     _codecs_installed = False

#     async def register_adapter(self) -> None:
#         try:
#                 if self._codecs_installed:
#                     return
#                 await self.set_type_codec(
#                     'json',
#                     encoder=adapt_dict,
#                     decoder=decode_dict,
#                     schema='pg_catalog'
#                 )
#                 await self.set_type_codec(
#                     'jsonb',
#                     encoder=adapt_dict,
#                     decoder=decode_dict,
#                     schema='pg_catalog'
#                 )
#                 self._codecs_installed = True
#         except Exception as e:
#             _log.error(f'[REGISTER ADAPTER]: {e}')


# class DataBase:
#     conn_kwargs: dict

#     def __init__(self) -> None:
#         self.__connection: Optional[asyncpg.Pool] = None

#     async def get_connection(self) -> asyncpg.Pool:
#         if not self.__connection or self.__connection.is_closing():
#             self.__connection = await asyncpg.create_pool(**self.conn_kwargs, command_timeout=60, connection_class=MyConnection)
#             _log.debug('Database pool connection opened')
#         return self.__connection

#     @classmethod
#     async def create_engine(
#         cls,
#         host: str,
#         port: int,
#         user: str,
#         password: str,
#         database: str
#     ) -> DataBase:
#         _log.debug("Load DataBases")
#         conn_kwargs = {
#             "host": host,
#             "port": port,
#             "user": user,
#             "password": password,
#             "database": database
#         }
#         self = cls()
#         self.conn_kwargs = conn_kwargs
#         await self.get_connection()
#         return self

#     @on_error()
#     async def execute(
#         self,
#         query: str | bytes,
#         vars: Vars = None
#     ) -> None:
#         vars = vars if vars is not None else []
#         pool = await self.get_connection()
#         con = await pool.acquire()

#         try:
#             await con.register_adapter()
#             await con.execute(query, *vars)
#         finally:
#             await pool.release(con)

#     @on_error()
#     async def fetchall(
#         self,
#         query: str | bytes,
#         vars: Vars = None
#     ) -> list[tuple[Any, ...]]:
#         vars = vars if vars is not None else []
#         pool = await self.get_connection()
#         con = await pool.acquire()

#         try:
#             await con.register_adapter()
#             return await con.fetch(query, *vars)
#         finally:
#             await pool.release(con)

#     @on_error()
#     async def fetchone(
#         self,
#         query: str | bytes,
#         vars: Vars = None
#     ) -> tuple[Any, ...] | None:
#         vars = vars if vars is not None else []
#         pool = await self.get_connection()
#         con = await pool.acquire()

#         try:
#             await con.register_adapter()
#             return await con.fetchrow(query, *vars)
#         finally:
#             await pool.release(con)

#     @on_error()
#     async def fetchvalue(
#         self,
#         query: str | bytes,
#         vars: Vars = None
#     ) -> Any | None:
#         vars = vars if vars is not None else []
#         pool = await self.get_connection()
#         con = await pool.acquire()

#         try:
#             await con.register_adapter()
#             return await con.fetchval(query, *vars)
#         finally:
#             await pool.release(con)
