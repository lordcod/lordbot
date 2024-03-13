from __future__ import annotations
import asyncio
import aiohttp
import nextcord
from nextcord.ext import commands

from bot.misc.utils import LordTimerHandler
from bot.languages import i18n
from bot.databases import GuildDateBases
from typing import Coroutine, List, Optional, Dict


class LordBot(commands.Bot):
    invites_data: Dict[int, List[nextcord.Invite]] = {}
    timeouts = {}
    guild_timer_handlers = {}

    @staticmethod
    async def get_command_prefixs(
        bot: commands.Bot,
        msg: nextcord.Message
    ) -> List[str]:
        "Returns a list of prefixes that can be used when using bot commands"
        gdb = GuildDateBases(msg.guild.id)
        prefix = gdb.get('prefix')
        return [prefix, f"<@{bot.user.id}> ", f"<@!{bot.user.id}> "]

    def add_event(self, coro: Coroutine, name: Optional[str] = None) -> None:
        """A decorator that registers an event to listen to.

        You can find more info about the events on the :ref:`documentation below <discord-api-events>`.

        The events must be a :ref:`coroutine <coroutine>`, if not, :exc:`TypeError` is raised

        Raises
        ------
        TypeError
            The coroutine passed is not actually a coroutine.

        Example
        -------

        .. code-block:: python3

            async def on_ready(): pass
            async def my_message(message): pass

            bot.add_event(on_ready)
            bot.add_event(my_message, 'on_message')
        """

        if not asyncio.iscoroutinefunction(coro):
            raise TypeError("event registered must be a coroutine function")

        name = name or coro.__name__

        setattr(self, name, coro)

    def __init__(self) -> None:
        super().__init__(command_prefix=self.get_command_prefixs,
                         intents=nextcord.Intents.all(),
                         help_command=None)
        i18n.from_folder("./bot/languages/localization")
        i18n.config['locale'] = 'en'
        self.session = aiohttp.ClientSession()
        self.lord_handler_timer = LordTimerHandler(self.loop)
