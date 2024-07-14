from __future__ import annotations

from typing import TYPE_CHECKING, Optional
import orjson
from bot.languages.help import commands


if TYPE_CHECKING:
    from bot.misc.lordbot import LordBot


handlers = {}


def ipc_route(name: Optional[str] = None):
    def wrapped(func):
        _name = name or func.__name__
        handlers[_name] = func
        return func
    return wrapped


@ipc_route()
async def get_guilds_count(bot: LordBot, data: dict):
    return str(len(bot.guilds))


@ipc_route()
async def get_members_count(bot: LordBot, data: dict):
    return str(len(list(bot.get_all_members())))


@ipc_route()
async def get_command_data(bot: LordBot, data: dict):
    return orjson.dumps(commands).decode()
