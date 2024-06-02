

import asyncio
import random


class FutureTest:
    def result(self):
        return random.random()

    def done(self):
        return False

    async def async_fun(self):
        print('Async')

    def __await__(self):
        if not self.done():
            yield asyncio.ensure_future(self.async_fun())
        return self.result()


async def main():
    ft = FutureTest()
    for i in ft.__await__():
        print(i)
    await ft

if __name__ == '__main__':
    asyncio.run(main())
