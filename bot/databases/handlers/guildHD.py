from __future__ import annotations
from typing import Any, Union, TypeVar
from ..db_engine import DataBase
from ..misc.error_handler import on_error
from ..misc.adapter_dict import Json, NumberFormating

engine: DataBase = None

reserved: list = []
T = TypeVar("T")


class GuildDateBases:
    def __init__(self, guild_id: int) -> None:
        if guild_id not in reserved:
            reserved.append(guild_id)

            if not self._get(guild_id):
                self._insert(guild_id)
        self.guild_id = guild_id

    @on_error()
    def _get(self, guild_id):
        guild = engine.fetchone(
            'SELECT * FROM guilds WHERE id = %s', (guild_id,))

        return guild

    @on_error()
    def _get_service(self, guild_id, arg):
        value = engine.fetchvalue(
            'SELECT ' + arg + ' FROM guilds WHERE id = %s', (guild_id,))

        return value

    @on_error()
    def _insert(self, guild_id):
        engine.execute('INSERT INTO guilds (id) VALUES (%s)', (guild_id,))

    @on_error()
    def _update(self, guild_id, arg, value):
        engine.execute(
            'UPDATE guilds SET ' + arg + ' = %s WHERE id = %s', (value,
                                                                 guild_id))

    @on_error()
    def get(self, service: str, default: T | None = None) -> Union[T, Any]:
        data = self._get_service(self.guild_id, service)
        data = Json.loads(data)
        data = NumberFormating.loads(data)

        if data is None:
            return default

        return data

    @on_error()
    def set(self, service, value):
        self._update(self.guild_id, service, value)

    @on_error()
    def delete(self):
        reserved.remove(self.guild_id)

        engine.execute('DELETE FROM guilds WHERE id = %s',
                       (self.guild_id,))

    async def adelete(self):
        self.delete()
