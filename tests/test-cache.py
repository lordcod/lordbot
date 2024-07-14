import asyncio
import aiocache


async def main():
    cache = aiocache.Cache()
    await cache.set('key', 'value')
    print(await cache.get('key'))
asyncio.run(main())
