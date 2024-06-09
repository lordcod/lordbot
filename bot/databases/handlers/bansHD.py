from __future__ import annotations
from typing import Optional
import nextcord
from nextcord.state import ConnectionState

from ..db_engine import DataBase
from ..misc.simple_task import to_task
from ..misc.adapter_dict import Json
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
    async def get_all(self):
        datas = await engine.fetchall('SELECT guild_id, member_id, time FROM bans')
        return datas

    @on_error()
    async def get_as_guild(self):
        datas = engine.fetchall(
            ('SELECT member_id, time FROM bans '
             'WHERE guild_id = $1'),
            [self.guild_id])

        return datas

    @on_error()
    async def get_as_member(self):
        data = await engine.fetchone(
            ('SELECT time FROM bans '
             'WHERE guild_id = $1 AND member_id = $2'),
            (self.guild_id, self.member_id)
        )

        return data

    @to_task
    @on_error()
    async def insert(self, time: int):
        await engine.execute(
            ('INSERT INTO bans '
             '(guild_id, member_id, time) '
             'VALUES ($1, $2, $3)'),
            (self.guild_id, self.member_id, time)
        )

    @to_task
    @on_error()
    async def update(self, new_time: int):
        await engine.execute(
            ('UPDATE bans '
             'SET time = $1 '
             'WHERE guild_id = $2 AND member_id = $3'),
            (new_time, self.guild_id, self.member_id)
        )

    @to_task
    @on_error()
    async def delete(self):
        await engine.execute(
            ('DELETE FROM bans '
             'WHERE guild_id = $1 AND member_id = %s'),
            (self.guild_id, self.member_id)
        )

    @to_task
    async def remove_ban(self, _state: ConnectionState, reason: Optional[str] = None):
        await self.delete()
        try:
            await _state.http.unban(self.member_id,
                                    self.guild_id,
                                    reason=reason)
        except nextcord.NotFound:
            pass
