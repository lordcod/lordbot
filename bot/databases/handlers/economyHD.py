from __future__ import annotations


from bot.databases.misc.simple_task import to_task
from ..db_engine import DataBase
from ..misc.error_handler import on_error

engine: DataBase = None


class EconomyMemberDB:
    def __init__(self, guild_id: int, member_id: int = None) -> None:
        self.guild_id = guild_id
        self.member_id = member_id

    async def get_data(self) -> dict:
        res = await self._get()
        data = dict(res)
        return data

    @on_error()
    async def get_leaderboards(self):
        leaderboard = await engine.fetchall(
            """SELECT member_id, balance, bank, balance+bank as total
                FROM economic
                WHERE guild_id = $1
                ORDER BY total DESC""",
            (self.guild_id,)
        )

        return leaderboard

    @on_error()
    async def _get(self):
        data = await engine.fetchone(
            'SELECT * FROM economic WHERE guild_id = $1 AND member_id = $2',
            (self.guild_id, self.member_id))

        if not data:
            await self.insert()
            data = await self._get()

        return data

    @to_task
    @on_error()
    async def insert(self):
        await engine.execute(
            'INSERT INTO economic (guild_id, member_id) VALUES ($1, $2)', (self.guild_id, self.member_id))

    @to_task
    @on_error()
    async def update(self, arg, value):
        await engine.execute(f'UPDATE economic SET {arg} = $1 WHERE guild_id = $2 AND member_id = $3', (
            value, self.guild_id, self.member_id))

    @to_task
    @on_error()
    async def update_list(self, args: dict):
        keys = ', '.join(
            [f"{a} = ${n}" for n, a in enumerate(args.keys(), start=1)])
        values = [*args.values(), self.guild_id, self.member_id]
        await engine.execute(
            f'UPDATE economic SET {keys} WHERE guild_id = ${len(keys)+1} AND member_id = ${len(keys)+2}', values)

    @to_task
    @on_error()
    async def delete(self):
        await engine.execute(
            'DELETE FROM economic WHERE guild_id = $1 AND member_id = $2', (self.guild_id, self.member_id))

    @to_task
    @on_error()
    async def delete_guild(self):
        await engine.execute(
            'DELETE FROM economic WHERE guild_id = $1', (self.guild_id,))

    async def get(self, __name, __default=None):
        data = await self.get_data()
        return data.get(__name, __default)

    @to_task
    async def set(self, key, value):
        data = await self.get_data()
        data[key] = value
        await self.update(key, value)

    @to_task
    async def increment(self, key, value):
        data = await self.get_data()
        data[key] += value
        await self.update(key, data[key])

    @to_task
    async def decline(self, key, value):
        data = await self.get_data()
        data[key] -= value
        await self.update(key, data[key])

    @to_task
    @staticmethod
    async def increment_for_ids(guild_id, member_ids, key, value):
        await engine.execute(f"""UPDATE economic SET {key} = {key} + $1 
                                 WHERE guild_id = $2 
                                 AND (SELECT ARRAY[member_id] && $3::bigint[])""", (
            value, guild_id, member_ids))

    @to_task
    @staticmethod
    async def decline_for_ids(guild_id, member_ids, key, value):
        await engine.execute(f"""UPDATE economic SET {key} = {key} - $1 
                                 WHERE guild_id = $2 
                                 AND (SELECT ARRAY[member_id] && $3::bigint[])""", (
            value, guild_id, member_ids))
