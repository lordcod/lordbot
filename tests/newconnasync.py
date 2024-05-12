import asyncio
import asyncpg


host = 'postgresql.879043c3234e.hosting.myjino.ru'
port = 5432
password = 'fd5-DVv-pf5-6bx'
user = 'j5191558_test'
db_name = 'j5191558_test'


async def run():
    conn: asyncpg.Connection = await asyncpg.connect(user=user, password=password,
                                                     database=db_name, host=host,
                                                     port=port)
    print(await conn.fetchval(
        """SELECT member_id, 
                  balance, 
                  bank, 
                  balance+bank as total
         FROM economic
        WHERE guild_id = '1179069504186232852'
        ORDER BY total DESC;"""))
    await conn.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
