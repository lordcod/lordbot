import asyncio
import timeit
import random


async def ttask(arg):
    print(arg)


def sstest(*args):
    print(*args)


ft = filter(lambda item: item is not None, [None, 1, 0, None])

sstest(*ft)


async def main():
    print('start')
    loop = asyncio.get_event_loop()
    th = loop.call_later(5, asyncio.create_task, ttask('finish task'))

    await asyncio.sleep(2)

    th._args[0].close()
    th.cancel()

    await asyncio.sleep(4)

    print('finish')

if __name__ == "__main__":
    asyncio.run(main())
