from __future__ import annotations
from typing import Callable, Optional
import nextcord
from psycopg2.extensions import connection as psycoon

from ..misc.utils import Json
from ..misc.error_handler import on_error, on_aioerror

connection: Callable[[], psycoon]


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
        with connection().cursor() as cursor:
            cursor.execute('SELECT guild_id, member_id, time FROM bans')

            datas = cursor.fetchall()

            datas = Json.loads(datas)

            return datas

    @on_error()
    def get_as_guild(self):
        with connection().cursor() as cursor:
            cursor.execute(
                ('SELECT member_id, time FROM bans '
                 'WHERE guild_id = %s'),
                [self.guild_id])

            datas = cursor.fetchall()

            return datas

    @on_error()
    def get_as_member(self):
        with connection().cursor() as cursor:
            cursor.execute(
                ('SELECT time FROM bans '
                 'WHERE guild_id = %s AND member_id = %s'),
                (self.guild_id, self.member_id)
            )

            datas = cursor.fetchone()

            return datas

    @on_error()
    def insert(self, time: int):
        with connection().cursor() as cursor:
            cursor.execute(
                ('INSERT INTO bans '
                 '(guild_id, member_id, time) '
                 'VALUES (%s, %s, %s)'),
                (self.guild_id, self.member_id, time)
            )

    @on_error()
    def update(self, new_time: int):
        with connection().cursor() as cursor:
            cursor.execute(
                ('UPDATE bans '
                 'SET time = %s '
                 'WHERE guild_id = %s AND member_id = %s'),
                (new_time, self.guild_id, self.member_id)
            )

    @on_error()
    def delete(self):
        with connection().cursor() as cursor:
            cursor.execute(
                ('DELETE FROM bans '
                 'WHERE guild_id = %s AND member_id = %s'),
                (self.guild_id, self.member_id)
            )

    async def remove_ban(self, _state, reason="Temp-ban"):
        self.delete()
        try:
            await _state.http.unban(self.member_id, self.guild_id, reason=reason)
        except nextcord.NotFound:
            pass
