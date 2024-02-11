import asyncio
import asyncpg


host = 'postgresql.879043c3234e.hosting.myjino.ru'
port = 5432
password = 'fd5-DVv-pf5-6bx'
user = 'j5191558_test'
db_name = 'j5191558_test'


async def run():
    conn = await asyncpg.connect(user=user, password=password,
                                 database=db_name, host=host,
                                 port=port)
    values = await conn.fetchval(
        'SELECT * FROM guilds'
    )
    print(values)
    await conn.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
