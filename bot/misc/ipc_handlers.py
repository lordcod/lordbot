from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from bot.languages.help import commands


if TYPE_CHECKING:
    from bot.misc.lordbot import LordBot


handlers = {}


def ipc_route(name: Optional[str] = None, ratelimit: Optional[int] = None):
    def wrapped(func):
        _name = name or func.__name__
        func.__limit__ = ratelimit
        handlers[_name] = func
        return func
    return wrapped


@ipc_route(ratelimit=60)
async def get_guilds_count(bot: LordBot, data: dict):
    return {
        'guilds_count': len(bot.guilds)
    }


@ipc_route(ratelimit=60)
async def get_members_count(bot: LordBot, data: dict):
    return {
        'members_count': len(list(bot.get_all_members()))
    }


@ipc_route(ratelimit=60)
async def get_command_data(bot: LordBot, data: dict):
    return commands
