from __future__ import annotations
from typing import Callable, List
import nextcord
from nextcord.ext import commands

from bot.misc.utils import DataRoleTimerHandlers, DataBanTimerHandlers


class LordBot(commands.Bot):
    timeouts = {}
    role_timer_handlers = DataRoleTimerHandlers()
    ban_timer_handlers = DataBanTimerHandlers()
    guild_timer_handlers = {}

    def __init__(
        self,
        func_prefixs: Callable[[LordBot, nextcord.Message], List[str]]
    ) -> None:
        super().__init__(command_prefix=func_prefixs,
                         intents=nextcord.Intents.all(),
                         help_command=None)
