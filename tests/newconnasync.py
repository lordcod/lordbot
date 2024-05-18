import asyncio
import asyncpg


host = 'postgresql.879043c3234e.hosting.myjino.ru'
port = 5432
password = 'fd5-DVv-pf5-6bx'
user = 'j5191558_test'
db_name = 'j5191558_test'

guild_id = 1179069504186232852
member_id = 636824998123798531


async def run():
    conn: asyncpg.Connection = await asyncpg.connect(user=user, password=password,
                                                     database=db_name, host=host,
                                                     port=port)
    data = await conn.fetchrow(
        """SELECT * FROM economic WHERE guild_id = $1 AND member_id = $2""", guild_id, member_id)
    await conn.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
