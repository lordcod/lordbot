import asyncio
import time


async def addt_task(num: int):
    await asyncio.sleep(0.5)
    print(num)


async def main():
    tasks = [addt_task(i) for i in range(4)]
    time1 = time.time()
    await asyncio.gather(*tasks)
    time2 = time.time()

    print(time2-time1)

if __name__ == '__main__':
    asyncio.run(main())
