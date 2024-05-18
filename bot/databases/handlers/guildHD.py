from __future__ import annotations
from typing import Any, Self, Union, TypeVar

from bot.databases.misc.simple_task import to_task
from ..db_engine import DataBase
from ..misc.error_handler import on_error

engine: DataBase = None

reserved: list = []
T = TypeVar("T")


def check_registration(func):
    async def wrapped(self: GuildDateBases, *args, **kwargs):
        if not self.__with_reserved__:
            if await self._get(self.guild_id):
                await self._insert(self.guild_id)
            self.__with_reserved__ = False
            reserved.append(self.guild_id)
        return await func(self, *args, **kwargs)
    return wrapped


class GuildDateBases:
    __with_reserved__: bool = False

    def __init__(self, guild_id: int) -> None:
        if guild_id not in reserved:
            self.__with_reserved__ = True
        self.guild_id = guild_id

    @on_error()
    async def _get(self, guild_id):
        guild = await engine.fetchone(
            'SELECT * FROM guilds WHERE id = %s', (guild_id,))

        return guild

    @on_error()
    async def _get_service(self, guild_id, arg):
        value = await engine.fetchvalue(
            'SELECT ' + arg + ' FROM guilds WHERE id = %s', (guild_id,))

        return value

    @to_task
    @on_error()
    async def _insert(self, guild_id):
        await engine.execute('INSERT INTO guilds (id) VALUES (%s)', (guild_id,))

    @to_task
    @on_error()
    async def _update(self, guild_id, arg, value):
        await engine.execute(
            'UPDATE guilds SET ' + arg + ' = %s WHERE id = %s', (value,
                                                                 guild_id))

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
        await self._update(self.guild_id, service, value)

    @to_task
    @on_error()
    async def delete(self):
        reserved.remove(self.guild_id)

        await engine.execute('DELETE FROM guilds WHERE id = %s',
                             (self.guild_id,))
