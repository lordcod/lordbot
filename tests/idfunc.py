import asyncio


async def main():
    loop = asyncio.get_event_loop()
    print(main == main)
    print(asyncio.create_task == asyncio.create_task)
    print(asyncio.create_task == loop.create_task)
    print(main() == main())

if __name__ == "__main__":
    asyncio.run(main())
