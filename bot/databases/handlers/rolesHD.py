from __future__ import annotations
from typing import Callable
from psycopg2.extensions import connection as psycoon

from ..misc.utils import Json, Formating
from ..misc.error_handler import on_error

connection: Callable[[], psycoon]


class RoleDateBases:
    def __init__(
        self,
        guild_id: int = None,
        member_id: int = None
    ) -> None:
        self.guild_id = guild_id
        self.member_id = member_id

    @on_error()
    def get_all(self):
        with connection().cursor() as cursor:
            cursor.execute(f'SELECT * FROM roles')

            datas = cursor.fetchall()

            datas = Json.loads(datas)

            return datas

    @on_error()
    def get_as_guild(self):
        with connection().cursor() as cursor:
            cursor.execute(
                'SELECT * FROM roles WHERE guild_id = %s', [self.guild_id])

            datas = cursor.fetchall()

            datas = Json.loads(datas)

            return datas

    @on_error()
    def get_as_member(self):
        with connection().cursor() as cursor:
            cursor.execute(
                'SELECT * FROM roles WHERE guild_id = %s AND member_id = %s',
                (self.guild_id, self.member_id)
            )

            data = cursor.fetchone()

            data = Json.loads(data)

            return data

    @on_error()
    def insert(self, roles):
        with connection().cursor() as cursor:
            cursor.execute(
                'INSERT INTO roles (guild_id, member_id, roles) VALUES (%s, %s, %s)',
                (self.guild_id, self.member_id, roles)
            )

    @on_error()
    def update(self, roles):
        try:
            with connection().cursor() as cursor:
                cursor.execute(
                    f'UPDATE roles SET roles = %s WHERE guild_id = %s AND member_id = %s',
                    (roles, self.guild_id, self.member_id)
                )
        except Exception as err:
            print('err hand', err)

    @on_error()
    def add(self, role_data) -> None:
        _roles_dat = self.get_as_member()

        if not _roles_dat:
            roles_ids = [role_data]
            role_datas = Json.dumps(roles_ids)
            self.insert(role_datas)
            return

        roles_ids = list(_roles_dat[2])
        if role_data in roles_ids:
            return

        roles_ids.append(role_data)

        role_datas = Json.dumps(roles_ids)
        self.update(role_datas)

    @on_error()
    def remove(self, role_data):
        _roles_dat = self.get_as_member()
        if not _roles_dat:
            return

        roles_ids = list(_roles_dat[2])
        if role_data not in roles_ids:
            return

        roles_ids.remove(role_data)

        role_datas = Json.dumps(roles_ids)
        self.update(role_datas)

    async def aremove(self, role_data):
        self.remove(role_data)
