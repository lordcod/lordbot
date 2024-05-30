

import asyncio
import functools
import time
from typing import Any


def return_yield(func):
    _result = None
    _with_result = False

    def set_result(res: Any) -> None:
        nonlocal _result
        nonlocal _with_result
        _result = res
        _with_result = True

    def has_result() -> bool:
        return _with_result

    async def continue_execution(iterable):
        print('cp')
        async for r in iterable:
            pass

    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        iterable = aiter(func(*args, **kwargs))
        r = await anext(iterable)
        set_result(r)
        asyncio.create_task(continue_execution(iterable))
        return _result
    return wrapped


@return_yield
async def test():
    yield 1
    await asyncio.sleep(1)
    print(2)
    yield None


if __name__ == '__main__':
    r = asyncio.run(test())
    print(r)
    time.sleep(1.2)
    print('Fin')
