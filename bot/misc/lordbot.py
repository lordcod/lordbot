from __future__ import annotations
import asyncio
import getopt
import logging
import sys
import os
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
from bot.misc.utils import LordTimeHandler
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

    def __init__(
        self,
        *,
        rollout_functions: bool = True,
        allow_bot_command: bool = False
    ) -> None:
        self.allow_bot_command = allow_bot_command

        flags = dict(map(lambda item: (item[0].removeprefix(
            '--'), item[1]), getopt.getopt(sys.argv[1:], '', ['token=', 'shards='])[0]))

        shard_ids, shard_count = (flags.get(
            'shards') or os.getenv('shards') or input("Shared info: ")).split("/")
        shard_count = int(shard_count)
        shard_ids = get_shard_list(shard_ids)

        intents = nextcord.Intents.all()
        intents.presences = False

        super().__init__(
            command_prefix=self.get_command_prefixs,
            intents=intents,
            help_command=None,
            shard_ids=shard_ids,
            shard_count=shard_count,
            rollout_associate_known=rollout_functions,
            rollout_delete_unknown=rollout_functions,
            rollout_register_new=rollout_functions,
            rollout_update_known=rollout_functions,
            rollout_all_guilds=rollout_functions
        )

        self.load_i18n_config()

        loop = asyncio.get_event_loop()

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

    def load_i18n_config(self) -> None:
        i18n.config['locale'] = 'en'
        i18n.from_file("./bot/languages/localization_any.json")

        for lang in ():
            json_resource = i18n._parse_json(i18n._load_file(f"temp_loc_{lang}.json"))
            i18n.resource_dict[lang].update(json_resource)
            i18n.parser(json_resource, lang)

    @property
    def session(self) -> aiohttp.ClientSession:
        if self.__session is None or self.__session.closed:
            self.__session = aiohttp.ClientSession()
        return self.__session

    async def process_commands(self, message: nextcord.Message) -> None:
        """|coro|

        This function processes the commands that have been registered
        to the bot and other groups. Without this coroutine, none of the
        commands will be triggered.

        By default, this coroutine is called inside the :func:`.on_message`
        event. If you choose to override the :func:`.on_message` event, then
        you should invoke this coroutine as well.

        This is built using other low level tools, and is equivalent to a
        call to :meth:`~.Bot.get_context` followed by a call to :meth:`~.Bot.invoke`.

        This also checks if the message's author is a bot and doesn't
        call :meth:`~.Bot.get_context` or :meth:`~.Bot.invoke` if so.

        Parameters
        ----------
        message: :class:`nextcord.Message`
            The message to process commands for.
        """
        if self.allow_bot_command and message.author.bot:
            return

        ctx = await self.get_context(message)
        await self.invoke(ctx)

    @staticmethod
    async def get_command_prefixs(
        bot: commands.Bot,
        msg: nextcord.Message
    ) -> List[str]:
        "Returns a list of prefixes that can be used when using bot commands"
        if msg.guild is None:
            return [DEFAULT_PREFIX, f"<@{bot.user.id}> ", f"<@!{bot.user.id}> "]
        gdb = GuildDateBases(msg.guild.id)
        prefix = await gdb.get('prefix', DEFAULT_PREFIX)
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

    async def register_jino(self):
        async with self.session.get('https://ifconfig.me/ip') as response:
            ipb = await response.read()
            ip = ipb.decode()

        query = "mutation addPostgreSQLRemoteSubnet($subnet: String!, $comment: String, $accountId: String) {\n  me {\n    legacy {\n      addPostgreSQLRemoteSubnet(\n        subnet: $subnet\n        comment: $comment\n        accountId: $accountId\n        validateAll: true\n        camelCaseErrors: true\n      )\n      __typename\n    }\n    __typename\n  }\n}\n"
        data = {
            'operationName': "addPostgreSQLRemoteSubnet",
            'query': query,
            'variables': {'subnet': ip, 'comment': None, 'accountId': "pmeyj"}
        }
        headers = {
            'Authorization': 'Bearer ' + os.getenv('JINO_TOKEN', '')
        }

        async with self.session.post('https://graphql.jino.ru/user/', json=data, headers=headers) as res:
            json = await res.json()

        with_auth = len(json.get('errors', [])) > 0

        if with_auth:
            _log.trace(
                'Successfully adding the IP address %s to the database', ip)
        else:
            _log.warning(
                'The JINO token needs to be updated. The IP address was not added to the database.')

    async def listen_on_ready(self) -> None:
        _log.debug('Listen on ready')

        await self.register_jino()
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
            return
        return super().dispatch(event_name, *args, **kwargs)
