import asyncio
from functools import wraps


def to_task(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.create_task(func(*args, **kwargs))
        return None
    return wrapped
