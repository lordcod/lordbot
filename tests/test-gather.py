import asyncio
import random


async def addtionally_task(i: int):
    print('Start func', i)
    await asyncio.sleep(random.randint(1, 10))
    return i


async def main():
    loop = asyncio.get_event_loop()
    tasks = [addtionally_task(i) for i in range(10)]
    res = await asyncio.gather(*tasks)
    print(res)

if __name__ == "__main__":
    asyncio.run(main())
