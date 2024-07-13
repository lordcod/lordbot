from _connection import connection
from bot.misc import logger
from bot.databases import localdb
import asyncio


async def main():
    with connection.cursor() as cursor:
        cursor.execute(
            """
                        SELECT values
                        FROM mongo 
                        WHERE name = 'ideas'
                    """)

        val = cursor.fetchone()
        localdb.current_updated_task['ideas'] = val[0]
        cache = await localdb.get_table('ideas')
        await cache._callback()
        await localdb.cache.close()


print("Finish")
asyncio.run(main())
connection.close()
