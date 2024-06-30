
import functools
import logging
from typing import Any, Callable


_log = logging.getLogger(__name__)


def on_error():
    def wrapped(func: Callable) -> Any:
        @functools.wraps(func)
        async def inner(*args, **kwargs):
            for i in range(3):
                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as exc:
                    _log.error(f"[ON_ERROR][{func.__name__}][{exc.__class__.__name__}]: Attempt: {i+1}/3", exc_info=exc)
            _log.debug(
                f"[ON_ERROR][ADDITIONALLY INFO]: {', '.join(map(str, args + tuple(f'{k}-{v}' for k,v in kwargs.items())))}")
        return inner
    return wrapped
