from __future__ import annotations
import asyncio
import logging
from typing import Any, Optional, Self, Union, TypeVar

from bot.databases.misc.simple_task import to_task
from ..db_engine import DataBase
from ..misc.error_handler import on_error

_log = logging.getLogger(__name__)

engine: DataBase = None
reserved: dict = {}
T = TypeVar("T")


def check_registration(func):
    async def wrapped(self: GuildDateBases, *args, **kwargs):
        if self.__required_task__:
            await asyncio.wait_for(self.__required_task__, timeout=None)
        if self.__with_reserved__:
            loop = asyncio.get_event_loop()
            self.__required_task__ = loop.create_future()
            if not await self._get(self.guild_id):
                await self._insert(self.guild_id)
            self.__with_reserved__ = False
            self.__required_task__.set_result(None)
            _log.debug(f"Guild {self.guild_id} registration completed")
        return await func(self, *args, **kwargs)
    return wrapped


class GuildDateBases:
    __with_reserved__: bool = False
    __required_task__: Optional[asyncio.Future] = None

    def __new__(cls, guild_id: int) -> Self:
        try:
            __instance = reserved[guild_id]
        except KeyError:
            __instance = object.__new__(cls)
            reserved[guild_id] = __instance
            __instance.__with_reserved__ = True

        return __instance

    def __init__(self, guild_id: int) -> None:
        self.guild_id = guild_id

    @on_error()
    async def _get(self, guild_id):
        guild = await engine.fetchone(
            'SELECT * FROM guilds WHERE id = $1', (guild_id,))

        return guild

    @on_error()
    async def _get_service(self, guild_id, arg):
        value = await engine.fetchvalue(
            'SELECT ' + arg + ' FROM guilds WHERE id = $1', (guild_id,))

        return value

    @to_task
    @on_error()
    async def _insert(self, guild_id):
        await engine.execute('INSERT INTO guilds (id) VALUES ($1)', (guild_id,))

    @check_registration
    @on_error()
    async def get(self, service: str, default: T | None = None) -> Union[T, Any]:
        data = await self._get_service(self.guild_id, service)

        if data is None:
            return default

        return data

    @check_registration
    @on_error()
    async def set(self, service, value):
        await engine.execute(
            'UPDATE guilds SET ' + service + ' = $1 WHERE id = $2', (value,
                                                                     self.guild_id))

    @check_registration
    @on_error()
    async def set_on_json(self, service, key, value):
        data: Optional[dict] = await self.get(service)

        if not data:  # type: ignore
            data = {}

        data[key] = value
        await self.set(service, data)

    @check_registration
    @on_error()
    async def append_on_json(self, service, value):
        data: Optional[list] = await self.get(service)

        if not data:  # type: ignore
            data = []

        data.append(value)
        await self.set(service, data)

    @to_task
    @on_error()
    async def delete(self):
        reserved.remove(self.guild_id)

        await engine.execute('DELETE FROM guilds WHERE id = $1',
                             (self.guild_id,))
