from __future__ import annotations
import asyncio
import aiohttp
import nextcord
import regex
from nextcord.ext import commands

from bot.misc.utils import LordTimerHandler
from bot.misc import giveaway as misc_giveaway
from bot.languages import i18n
from bot.databases import GuildDateBases
from bot.databases import db
from bot.databases.db import DataBase, establish_connection
from bot.databases.config import host, port, user, password, db_name
from typing import Coroutine, List, Optional, Dict, Any

from bot.resources.info import DEFAULT_PREFIX


def get_shard_list(shard_ids: str):
    res = []
    for shard in shard_ids.split(","):
        if data := regex.fullmatch(r"(\d+)-(\d+)", shard):
            res.extend(range(int(data.group(1)),
                             int(data.group(2))))
        else:
            res.append(int(shard))
    return res


class LordBot(commands.AutoShardedBot):
    engine: DataBase
    ya_requests: Any = None
    invites_data: Dict[int, List[nextcord.Invite]] = {}
    timeouts = {}
    guild_timer_handlers = {}

    @staticmethod
    async def get_command_prefixs(
        bot: commands.Bot,
        msg: nextcord.Message
    ) -> List[str]:
        "Returns a list of prefixes that can be used when using bot commands"
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

    def __init__(self) -> None:
        shard_ids, shard_count = input("Shared info: ").split("/")
        shard_count = int(shard_count)
        shard_ids = get_shard_list(shard_ids)

        super().__init__(
            command_prefix=self.get_command_prefixs,
            intents=nextcord.Intents.all(),
            help_command=None,
            shard_ids=shard_ids,
            shard_count=shard_count
        )
        loop = asyncio.get_event_loop()
        i18n.from_folder("./bot/languages/localization")
        i18n.config['locale'] = 'en'
        self.session = aiohttp.ClientSession()
        self.__with_ready__ = loop.create_future()
        self.lord_handler_timer = LordTimerHandler(self.loop)
        misc_giveaway.Giveaway.set_lord_timer_handler(self.lord_handler_timer)
        self.add_listener(self.listen_on_ready, 'on_ready')

    async def listen_on_ready(self) -> None:
        self.engine = engine = DataBase.create_engine(
            host, port, user, password, db_name)
        establish_connection(engine)
        for t in db._tables:
            t.set_engine(engine)
            t.create()
        self.__with_ready__.set_result(None)
