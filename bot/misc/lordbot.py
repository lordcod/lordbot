from __future__ import annotations
import asyncio
import aiohttp
import nextcord
from nextcord.ext import commands

from bot.misc.utils import LordTimerHandler
from bot.languages import i18n
from bot.databases import GuildDateBases
from typing import Coroutine, List, Optional, Dict

from bot.resources.info import DEFAULT_PREFIX


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
        print(f"{msg.author.display_name} sended message!")
        if msg.guild is None:
            return [DEFAULT_PREFIX, f"<@{bot.user.id}> ", f"<@!{bot.user.id}> "]
        gdb = GuildDateBases(msg.guild.id)
        prefix = gdb.get('prefix')
        return [prefix, f"<@{bot.user.id}> ", f"<@!{bot.user.id}> "]

    def set_event(self, coro: Coroutine, name: Optional[str] = None) -> None:
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

            bot.set_event(on_ready)
            bot.set_event(my_message, 'on_message')
        """

        if not asyncio.iscoroutinefunction(coro):
            raise TypeError("event registered must be a coroutine function")

        name = name or coro.__name__

        setattr(self, name, coro)

    def dispatch(self, event_name: asyncio.Any, *args: asyncio.Any, **kwargs: asyncio.Any) -> None:
        print(event_name, args, kwargs)
        return super().dispatch(event_name, *args, **kwargs)

    def __init__(self) -> None:
        shard_id, shard_count = map(int, input("Shared info: ").split("/"))
        super().__init__(
            command_prefix=self.get_command_prefixs,
            intents=nextcord.Intents.all(),
            help_command=None,
            shard_id=shard_id,
            shard_count=shard_count
        )
        i18n.from_folder("./bot/languages/localization")
        i18n.config['locale'] = 'en'
        self.session = aiohttp.ClientSession()
        self.lord_handler_timer = LordTimerHandler(self.loop)
