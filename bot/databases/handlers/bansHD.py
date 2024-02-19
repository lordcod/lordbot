from __future__ import annotations
from typing import Callable, Optional
import nextcord
from psycopg2.extensions import connection as psycoon

from ..misc.utils import Json
from ..misc.error_handler import on_error

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
            cursor.execute('SELECT * FROM bans')

            datas = cursor.fetchall()

            datas = Json.loads(datas)

            return datas

    @on_error()
    def get_as_guild(self):
        with connection().cursor() as cursor:
            cursor.execute(
                ('SELECT member_id, time, reason '
                 'FROM roles WHERE guild_id = %s'),
                [self.guild_id])

            datas = cursor.fetchall()

            return datas

    @on_error()
    def get_as_member(self):
        with connection().cursor() as cursor:
            cursor.execute(
                ('SELECT time, reason FROM bans '
                 'WHERE guild_id = %s AND member_id = %s'),
                (self.guild_id, self.member_id)
            )

            datas = cursor.fetchone()

            return datas

    @on_error()
    def insert(self, time: int, reason: str):
        with connection().cursor() as cursor:
            cursor.execute(
                ('INSERT INTO bans '
                 '(guild_id, member_id, time, reason) '
                 'VALUES (%s, %s, %s, %s)'),
                (self.guild_id, self.member_id, time, reason)
            )

    @on_error()
    def update(self, new_time: int, new_reason: str):
        with connection().cursor() as cursor:
            cursor.execute(
                ('UPDATE roles '
                 'SET time = %s, reason = %s'
                 'WHERE guild_id = %s AND member_id = %s'),
                (new_time, new_reason, self.guild_id, self.member_id)
            )

    @on_error()
    def delete(self):
        with connection().cursor() as cursor:
            cursor.execute(
                ('DELETE FROM roles '
                 'WHERE guild_id = %s AND member_id = %s'),
                (self.guild_id, self.member_id)
            )

    @on_error()
    def remove(self):
        _role_data = self.get_as_member()
        if _role_data is not None:
            self.delete()

    @on_error()
    def set_ban(self, time: int, reason: str) -> None:
        _role_data = self.get_as_member()
        if _role_data is None:
            self.insert(time, reason)
        else:
            self.update(time, reason)

    async def remove_ban(self, member: nextcord.Member, reason: str):
        await member.unban(reason=reason)
        self.remove()
