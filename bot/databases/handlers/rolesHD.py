from __future__ import annotations
import nextcord
from typing import Optional
from ..db_engine import DataBase

from ..misc.adapter_dict import Json
from ..misc.error_handler import on_error

engine: DataBase = None


class RoleDateBases:
    def __init__(
        self,
        guild_id: Optional[int] = None,
        member_id: Optional[int] = None
    ) -> None:
        self.guild_id = guild_id
        self.member_id = member_id

    @on_error()
    def get_all(self):
        datas = engine.fetchall('SELECT * FROM roles')

        datas = Json.loads(datas)

        return datas

    @on_error()
    def get_as_guild(self):
        datas = engine.fetchall(
            ('SELECT member_id, role_id, time '
             'FROM roles WHERE guild_id = %s'),
            [self.guild_id])

        return datas

    @on_error()
    def get_as_member(self):
        datas = engine.fetchall(
            ('SELECT member_id, role_id, time FROM roles '
             'WHERE guild_id = %s AND member_id = %s'),
            (self.guild_id, self.member_id)
        )

        return datas

    @on_error()
    def get_as_role(self, role_id: int):
        data = engine.fetchone(
            ('SELECT time FROM roles '
             'WHERE guild_id = %s AND member_id = %s AND role_id = %s'),
            (self.guild_id, self.member_id, role_id)
        )

        return data

    @on_error()
    def insert(self, role_id: int, time: int):
        engine.execute(
            ('INSERT INTO roles '
             '(guild_id, member_id, role_id, time) '
             'VALUES (%s, %s, %s, %s)'),
            (self.guild_id, self.member_id, role_id, time)
        )

    @on_error()
    def update(self, role_id: int, time: int):
        engine.execute(
            ('UPDATE roles '
             'SET time = %s '
             'WHERE guild_id = %s AND member_id = %s AND role_id = %s'),
            (time, self.guild_id, self.member_id, role_id)
        )

    @on_error()
    def delete(self, role_id: int):
        engine.execute(
            ('DELETE FROM roles '
             'WHERE guild_id = %s AND member_id = %s AND role_id = %s'),
            (self.guild_id, self.member_id, role_id)
        )

    @on_error()
    def remove(self, role_id):
        _role_data = self.get_as_role(role_id)
        if _role_data is not None:
            self.delete(role_id)

    @on_error()
    def set_role(self, role_id: int, time: int) -> None:
        _role_data = self.get_as_role(role_id)
        if _role_data is None:
            self.insert(role_id, time)
        else:
            self.update(role_id, time)

    async def remove_role(self, member: nextcord.Member, role: nextcord.Role):
        await member.remove_roles(role)
        self.remove(role.id)
