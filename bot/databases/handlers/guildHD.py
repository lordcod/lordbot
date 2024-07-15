from __future__ import annotations
import asyncio
from collections import defaultdict
import functools
import logging
from typing import Any, Dict, List, Optional, Union, TypeVar

from bot.databases.misc.simple_task import to_task
from ..db_engine import DataBase
from ..misc.error_handler import on_error

_log = logging.getLogger(__name__)

engine: DataBase = None
reserved = []
collectable_hashable_data: List[str] = ['language', 'color']
hashable_data: Dict[int, Dict[str, Any]] = defaultdict(dict)
T = TypeVar("T")


def check_registration(func):
    @functools.wraps(func)
    async def wrapped(self: GuildDateBases, *args, **kwargs):
        await self.register()
        return await func(self, *args, **kwargs)
    return wrapped


class GuildDateBases:
    def __init__(self, guild_id: int) -> None:
        self.guild_id = guild_id

    @on_error()
    async def register(self):
        if self.guild_id in reserved:
            return
        reserved.append(self.guild_id)
        if not await self._get(self.guild_id):
            await self._insert(self.guild_id)
            _log.trace(f"Guild {self.guild_id} registration completed")

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

    @on_error()
    async def _insert(self, guild_id):
        await engine.execute('INSERT INTO guilds (id) VALUES (%s)', (guild_id,))

    @check_registration
    @on_error()
    async def get(self, service: str, default: T | None = None) -> Union[T, Any]:
        data = await self._get_service(self.guild_id, service)

        if service in collectable_hashable_data:
            hashable_data[self.guild_id][service] = data

        if data is None:
            return default

        return data

    def get_hash(self, service: str, default: T | None = None) -> Union[T, Any]:
        return hashable_data[self.guild_id].get(service, default)

    @check_registration
    @on_error()
    async def set(self, service, value):
        if service in collectable_hashable_data:
            hashable_data[self.guild_id][service] = value

        await engine.execute(
            'UPDATE guilds SET ' + service + ' = %s WHERE id = %s', (value,
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

    @on_error()
    async def delete(self):
        reserved.pop(self.guild_id, None)

        await engine.execute('DELETE FROM guilds WHERE id = %s',
                             (self.guild_id,))

    @on_error()
    @staticmethod
    async def get_deleted():
        return await engine.fetchall('SELECT id, delete_task FROM guilds WHERE delete_task IS NOT NULL')
