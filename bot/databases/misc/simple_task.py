import asyncio
from functools import wraps


def to_task(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        print(func)
        if not asyncio.iscoroutinefunction(func):
            return None
        loop = asyncio.get_event_loop()
        loop.create_task(func(*args, **kwargs))
        return None
    wrapped.__func__ = func
    return wrapped
