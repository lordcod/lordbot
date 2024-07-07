from __future__ import annotations
import asyncio
import logging
import sys
import aiohttp
import nextcord
import regex
from typing import Coroutine, List, Optional, Dict, Any

from nextcord.ext import commands

from bot.databases import GuildDateBases
from bot.databases import db
from bot.databases.db import DataBase, establish_connection
from bot.databases.config import host, port, user, password, db_name
from bot.misc.api_site import ApiSite
from bot.misc.ipc_handlers import handlers
from bot.resources.info import DEFAULT_PREFIX
from bot.misc.utils import LordTimeHandler,  translate_flags
from bot.languages import i18n
from bot.misc.noti import TwitchNotification, YoutubeNotification


_log = logging.getLogger(__name__)


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

    def __init__(self) -> None:
        flags = translate_flags(' '.join(sys.argv[1:]))
        shard_ids, shard_count = (flags.get(
            'shards') or input("Shared info: ")).split("/")
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

        i18n.from_file("./bot/languages/localization_any.json")
        i18n.config['locale'] = 'en'

        self.__session = None
        self.apisite = ApiSite(self, handlers)

        self.twnoti = TwitchNotification(self)
        self.ytnoti = YoutubeNotification(self)

        self.__with_ready__ = loop.create_future()
        self.__with_ready_events__ = []

        self.lord_handler_timer: LordTimeHandler = LordTimeHandler(loop)

        self.add_listener(self.listen_on_ready, 'on_ready')
        self.add_listener(self.apisite._ApiSite__run, 'on_ready')
        self.add_listener(self.twnoti.parse_twitch, 'on_ready')
        self.add_listener(self.ytnoti.parse_youtube, 'on_ready')

    @property
    def session(self) -> aiohttp.ClientSession:
        if self.__session is None or self.__session.closed:
            self.__session = aiohttp.ClientSession()
        return self.__session

    @staticmethod
    async def get_command_prefixs(
        bot: commands.Bot,
        msg: nextcord.Message
    ) -> List[str]:
        "Returns a list of prefixes that can be used when using bot commands"
        if msg.guild is None:
            return [DEFAULT_PREFIX, f"<@{bot.user.id}> ", f"<@!{bot.user.id}> "]
        gdb = GuildDateBases(msg.guild.id)
        prefix = await gdb.get('prefix') or DEFAULT_PREFIX
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

    async def listen_on_ready(self) -> None:
        try:
            self.engine = engine = await DataBase.create_engine(
                host, port, user, password, db_name)
        except Exception as exc:
            _log.error("Couldn't connect to the database", exc_info=exc)
            await self.close()
            await self.session.close()
            return

        establish_connection(engine)

        for t in db._tables:
            t.set_engine(engine)
            await t.create()

        if not self.__with_ready__.done():
            self.__with_ready__.set_result(None)

        for event_data in self.__with_ready_events__:
            self.dispatch(event_data[0], *event_data[1], **event_data[2])

    def dispatch(self, event_name: str, *args: Any, **kwargs: Any) -> None:
        if not self.__with_ready__.done() and event_name.lower() != 'ready':
            self.__with_ready_events__.append((event_name, args, kwargs))
            _log.trace('Postponed event %s', event_name)
            return
        return super().dispatch(event_name, *args, **kwargs)
