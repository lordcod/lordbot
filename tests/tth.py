import asyncio

loop = asyncio.get_event_loop()


async def plan_task(mes):
    print(mes)


async def main():
    print("Coro start")

    th = loop.call_later(5, asyncio.create_task, plan_task("Task start"))

    await asyncio.sleep(2)

    th._run()
    th.cancel()

    await asyncio.sleep(3.5)

    print("Task final")


if __name__ == "__main__":
    res = loop.run_until_complete(main())
