from typing import Any, Callable
from bot.misc.logger import Logger
import psycopg2


class on_error:
    def __init__(self) -> None:
        pass

    def __call__(self, func: Callable) -> Any:
        def wrapped(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except psycopg2.errors.OperationalError:
                Logger.error(f"[ON_ERROR][{func.__name__}] server closed")
                return wrapped(*args, **kwargs)
        return wrapped

class on_aioerror:
    def __init__(self) -> None:
        pass

    def __call__(self, func: Callable) -> Any:
        async def wrapped(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except psycopg2.errors.OperationalError:
                Logger.error(f"[ON_ERROR][{func.__name__}] server closed")
                return wrapped(*args, **kwargs)
        return wrapped
