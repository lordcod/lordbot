from __future__ import annotations
from typing import Optional
import nextcord
from nextcord.state import ConnectionState
from ..db_engine import DataBase
from ..misc.utils import Json
from ..misc.error_handler import on_error

engine: DataBase = None


class BanDateBases:
    def __init__(
        self,
        guild_id: Optional[int] = None,
        member_id: Optional[int] = None
    ) -> None:
        self.guild_id = guild_id
        self.member_id = member_id

    @on_error()
    def get_all(self):
        datas = engine.fetchall('SELECT guild_id, member_id, time FROM bans')

        datas = Json.loads(datas)

        return datas

    @on_error()
    def get_as_guild(self):
        datas = engine.fetchall(
            ('SELECT member_id, time FROM bans '
             'WHERE guild_id = %s'),
            [self.guild_id])

        return datas

    @on_error()
    def get_as_member(self):
        data = engine.fetchone(
            ('SELECT time FROM bans '
             'WHERE guild_id = %s AND member_id = %s'),
            (self.guild_id, self.member_id)
        )

        return data

    @on_error()
    def insert(self, time: int):
        engine.execute(
            ('INSERT INTO bans '
             '(guild_id, member_id, time) '
             'VALUES (%s, %s, %s)'),
            (self.guild_id, self.member_id, time)
        )

    @on_error()
    def update(self, new_time: int):
        engine.execute(
            ('UPDATE bans '
             'SET time = %s '
             'WHERE guild_id = %s AND member_id = %s'),
            (new_time, self.guild_id, self.member_id)
        )

    @on_error()
    def delete(self):
        engine.execute(
            ('DELETE FROM bans '
             'WHERE guild_id = %s AND member_id = %s'),
            (self.guild_id, self.member_id)
        )

    async def remove_ban(self, _state: ConnectionState, reason: Optional[str] = None):
        self.delete()
        try:
            await _state.http.unban(self.member_id,
                                    self.guild_id,
                                    reason=reason)
        except nextcord.NotFound:
            pass
