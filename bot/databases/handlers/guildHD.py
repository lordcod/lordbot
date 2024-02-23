from __future__ import annotations
from typing import Union
from ..db_engine import DataBase
from ..misc.error_handler import on_error
from ..misc.utils import Json, Formating

engine: DataBase = None

reserved: list = []


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
        value = engine.fetchone(
            f'SELECT {arg} FROM guilds WHERE id = %s', (guild_id,))

        return value

    @on_error()
    def _insert(self, guild_id):
        engine.execute('INSERT INTO guilds (id) VALUES (%s)', (guild_id,))

    @on_error()
    def _update(self, guild_id, arg, value):
        engine.execute(
            f'UPDATE guilds SET {arg} = %s WHERE id = %s', (value,
                                                            guild_id))

    @on_error()
    def get(self, service: str, default: any = None) -> Union[dict, int, str]:
        data = self._get_service(self.guild_id, service)
        data = data[0]
        data = Json.loads(data)
        data = Formating.loads(data)

        if data is None:
            return default
        return data

    @on_error()
    def set(self, service, value):
        value = Formating.dumps(value)
        value = Json.dumps(value)
        self._update(self.guild_id, service, value)

    @on_error()
    def delete(self):
        reserved.remove(self.guild_id)

        engine.execute('DELETE FROM guilds WHERE id = %s',
                       (self.guild_id,))
