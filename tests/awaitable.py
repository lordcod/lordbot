import asyncio
import functools


def transfer_to_async(cls):
    @functools.wraps(cls)
    async def wrapped(*args, **kwargs):
        self = cls(*args, **kwargs)
        await self.__await__()
        return self
    return wrapped


@transfer_to_async
class Test:
    "| Coroutine |"

    def __init__(self, mes):
        self.mes = mes

    async def __await__(self):
        return self.mes


async def main():
    t = Test("l")
    print(t)
    print(await t)

if __name__ == "__main__":
    asyncio.run(main())
