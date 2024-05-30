
import traceback
from typing import Any, Callable

import asyncpg
from bot.misc.logger import Logger


def on_error():
    def wrapped(func: Callable) -> Any:
        async def inner(*args, **kwargs):
            for i in range(3):
                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as exc:
                    Logger.error(
                        f"[ON_ERROR][{func.__name__}][{exc.__class__.__name__}]: Attempt: {i+1}/3\n"
                        f"{traceback.format_exc()}"
                    )
            Logger.info(
                f"[ON_ERROR][ADDITIONALLY INFO]: {', '.join(args + (f'{k}-{v}' for k,v in kwargs.items()))}")
        return inner
    return wrapped
