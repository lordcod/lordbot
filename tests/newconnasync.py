import asyncio
import asyncpg
import orjson


host = 'postgresql.879043c3234e.hosting.myjino.ru'
port = 5432
password = 'fd5-DVv-pf5-6bx'
user = 'j5191558_test'
db_name = 'j5191558_test'

key = 'bank'
value = 100
member_ids = [636824998123798531, 804950325265825815]
guild_id = 1179069504186232852
member_id = 636824998123798531


async def run():
    conn: asyncpg.Connection = await asyncpg.connect(user=user, password=password,
                                                     database=db_name, host=host,
                                                     port=port)
    insert_info = ', '.join(map(str, [(guild_id, id) for id in member_ids]))
    r = await conn.fetchval(f'INSERT INTO economic (guild_id, member_id) VALUES {insert_info}', )
    print(r)
    await conn.close()
loop = asyncio.get_event_loop()
loop.run_until_complete(run())
