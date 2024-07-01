

from typing import TYPE_CHECKING

import orjson
from bot.languages.help import commands
from nextcord.ext.ipc.server import IpcServerResponse

if TYPE_CHECKING:
    from bot.misc.lordbot import LordBot
    bot: LordBot
else:
    bot = None


handlers = []


def ipc_route(func):
    handlers.append(func)
    return func


def get_handlers(_bot):
    global bot
    bot = _bot
    return handlers


@ipc_route
async def get_guilds_count(data: IpcServerResponse):
    return len(bot.guilds)


@ipc_route
async def get_command_data(data: IpcServerResponse):
    return commands
