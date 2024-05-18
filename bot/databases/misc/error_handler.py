from typing import Any, Callable
from bot.misc.logger import Logger
import psycopg2


def on_error():
    def wrapped(func: Callable) -> Any:
        async def inner(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                return result
            except psycopg2.errors.OperationalError:
                Logger.error(f"[ON_ERROR][{func.__name__}] server closed")
                return await inner(*args, **kwargs)
        return inner
    return wrapped
