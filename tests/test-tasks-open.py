import asyncio

loop = asyncio.get_event_loop()


async def task_1():
    print(1)


async def task_2():
    print(2)


t1 = loop.create_task(task_1())
t2 = loop.create_task(task_2())


def task_done(task):
    print(task)


async def main():
    await asyncio.sleep(1)


t1.add_done_callback(task_done)
t2.add_done_callback(task_done)
loop.run_until_complete(main())
