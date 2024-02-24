import asyncio


async def ttask(arg):
    print(arg)


async def main():
    print('start')
    loop = asyncio.get_event_loop()
    th = loop.call_later(-13859, asyncio.create_task, ttask('finish task'))

    await asyncio.sleep(2)
    print(loop.time())
    print(th.when())
    th._args[0].close()
    th.cancel()

    await asyncio.sleep(4)

    print('finish')


def gen_test(iter):
    yield from iter


if __name__ == "__main__":
    for i in gen_test(range(1, 100)):
        print(i)
    # asyncio.run(main())
