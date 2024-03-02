from __future__ import annotations
from psycopg2.extras import DictCursor
from ..db_engine import DataBase
from ..misc.error_handler import on_error

engine: DataBase = None


class EconomyMemberDB:
    def __init__(self, guild_id: int, member_id: int = None) -> None:
        self.guild_id = guild_id
        self.member_id = member_id

        self.data = self._get()

    @on_error()
    def get_leaderboards(self):
        leaderboard = engine.fetchall(
            """SELECT member_id, balance, bank, balance+bank as total
                FROM economic
                WHERE guild_id = %s
                ORDER BY total DESC""",
            (self.guild_id,)
        )

        return leaderboard

    @on_error()
    def _get(self):
        with engine.connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                'SELECT * FROM economic WHERE guild_id = %s AND member_id = %s',
                (self.guild_id, self.member_id))
            data = cursor.fetchone()

        if not data:
            self.insert()
            data = self._get()

        return data

    @on_error()
    def insert(self):
        engine.execute(
            'INSERT INTO economic (guild_id, member_id) VALUES (%s,%s)', (self.guild_id, self.member_id))

    @on_error()
    def update(self, arg, value):
        engine.execute(f'UPDATE economic SET {arg} = %s WHERE guild_id = %s AND member_id = %s', (
            value, self.guild_id, self.member_id))

    @on_error()
    def update_list(self, args: dict):
        keys = ', '.join([f"{a} = %s" for a in args.keys()])
        values = [*args.values(), self.guild_id, self.member_id]
        engine.execute(
            f'UPDATE economic SET {keys} WHERE guild_id = %s AND member_id = %s', values)

    @on_error()
    def delete(self):
        engine.execute(
            'DELETE FROM economic WHERE guild_id = %s AND member_id = %s', (self.guild_id, self.member_id))

    @on_error()
    def delete_guild(self):
        engine.execute(
            'DELETE FROM economic WHERE guild_id = %s', (self.guild_id,))

    def get(self, __name, __default=None):
        return self.data.get(__name, __default)

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.data[key] = value
        self.update(key, value)
