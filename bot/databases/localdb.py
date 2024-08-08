
import asyncio
import contextlib
from enum import Enum
import logging
import os
import time
from typing import Optional
import aiocache
from aiocache.base import SENTINEL
from bot.databases.misc.adapter_dict import FullJson


_log = logging.getLogger(__name__)

HEARTBEAT_UPDATE = 180
last_updated = time.time()+HEARTBEAT_UPDATE
handler: Optional[asyncio.TimerHandle] = None
current_updated_task = {}


class UpdatedCache(aiocache.SimpleMemoryCache):
    def __init__(self, name: str, **kwargs) -> None:
        self.__tablename__ = name
        super().__init__(ttl=None, key_builder=self._build_key, **kwargs)

    def _build_key(self, key, namespace=None):
        if namespace is not None:
            return "{}{}".format(namespace, self._ensure_key(key))
        if self.namespace is not None:
            return "{}{}".format(self.namespace, self._ensure_key(key))
        return self._ensure_key(key)

    def _ensure_key(self, key):
        if isinstance(key, Enum):
            return key.value
        else:
            return key

    async def add(self, key, value, ttl=SENTINEL, dumps_fn=None, namespace=None, _conn=None):
        asyncio.create_task(self.callback())
        return await super().add(key, value, ttl, dumps_fn, namespace, _conn)

    async def set(self, key, value, ttl=SENTINEL, dumps_fn=None, namespace=None, _cas_token=None, _conn=None):
        asyncio.create_task(self.callback())
        return await super().set(key, value, ttl, dumps_fn, namespace, _cas_token, _conn)

    async def multi_set(self, pairs, ttl=SENTINEL, dumps_fn=None, namespace=None, _conn=None):
        asyncio.create_task(self.callback())
        return await super().multi_set(pairs, ttl, dumps_fn, namespace, _conn)

    async def increment(self, key, delta=1, namespace=None, _conn=None):
        asyncio.create_task(self.callback())
        return await super().increment(key, delta, namespace, _conn)

    async def delete(self, key, namespace=None, _conn=None):
        asyncio.create_task(self.callback())
        return await super().delete(key, namespace, _conn)

    async def clear(self, namespace=None, _conn=None):
        asyncio.create_task(self.callback())
        return await super().clear(namespace, _conn)

    async def fetch(self) -> dict:
        return self._cache

    async def callback(self) -> None:
        global handler
        current_updated_task[self.__tablename__] = self._cache

        if handler:
            return

        if last_updated > time.time():
            loop = asyncio.get_event_loop()
            handler = loop.call_later(
                last_updated-time.time(), asyncio.create_task, _update_db(self.__tablename__))
            return

        await _update_db(self.__tablename__)


cache = aiocache.RedisCache(
    FullJson(),
    endpoint=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    password=os.environ.get('REDIS_PASSWORD'),
    pool_max_size=100,
)
cache_data = {}


async def _update_db(tablename) -> None:
    global last_updated, handler
    last_updated = time.time()+HEARTBEAT_UPDATE
    handler = None
    _log.trace('Updated %s databases requests from %s',
               ', '.join(current_updated_task.keys()), tablename)
    with contextlib.suppress(BaseException):
        await cache.multi_set(current_updated_task.items())
        current_updated_task.clear()


async def get_table(table_name: str, /, *, namespace=None, timeout=None) -> UpdatedCache:
    if table_name in cache_data:
        return cache_data[table_name]

    data = {}
    db = UpdatedCache(table_name, namespace=None, timeout=None)
    cache_data[table_name] = db
    last_exc: Exception = None

    for i in range(5):
        _log.trace('[%d] A request for fetched database %s was received', i, table_name)
        try:
            data = await cache.get(table_name, {})
        except Exception as exc:
            last_exc = exc
        else:
            _log.trace('Fetched databases %s', table_name)
            data = FullJson().loads(data)
            break
        await asyncio.sleep(1)
    else:
        _log.trace('Getting the database %s ended with an error %s',
                   table_name, type(last_exc).__name__, exc_info=last_exc)
    db._cache = data
    return db
