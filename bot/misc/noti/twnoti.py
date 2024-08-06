from __future__ import annotations

import asyncio
import os
import time
import logging
from typing import TYPE_CHECKING, Optional, Tuple

from bot.databases.handlers.guildHD import GuildDateBases
from bot.misc.utils import get_payload, generate_message, lord_format
from bot.resources.info import DEFAULT_TWITCH_MESSAGE

try:
    from .twtypes import Stream, User
except ImportError:
    from twtypes import Stream, User

if TYPE_CHECKING:
    from bot.misc.lordbot import LordBot

_log = logging.getLogger(__name__)


class TwNoti:
    twitch_api_access_token: Optional[str] = None
    twitch_api_access_token_end: Optional[int] = None

    def __init__(
        self,
        bot: LordBot,
        client_id: str = os.getenv('TWITCH_CLIENT_ID'),
        client_secret: str = os.getenv('TWITCH_CLIENT_SECRET')
    ) -> None:
        self.bot = bot
        self.client_id = client_id
        self.client_secret = client_secret

        self.usernames = set()
        self.twitch_streaming = set()
        self.user_info = {}
        self.directed_data = {}

        self.__running: bool = False

        self.heartbeat_timeout = 180
        self.last_heartbeat = time.time()

    @property
    def running(self) -> bool:
        return self.__running and self.last_heartbeat > time.time() - self.heartbeat_timeout

    @running.setter
    def running(self, __value: bool) -> None:
        if not isinstance(__value, bool):
            raise TypeError('The %s type is not supported' % (type(__value).__name__,))
        self.__running = __value

    async def request(self, method: str, url: str, with_auth: bool = True, **kwargs):
        async with self.bot.session.request(method, url, **kwargs) as response:
            content_type = response.headers.get('Content-Type')
            if content_type == 'application/json' or 'application/json' in content_type:
                data = await response.json()
            else:
                data = await response.read()

        if with_auth and response.status == 401:
            await self.get_oauth_token()
        if not response.ok:
            _log.error('It was not possible to get data from the api, status: %s, data: %s', response.status, data)
            return None

        return data

    async def callback_on_start(self, stream: Stream):
        _log.debug('%s started stream', stream.user_name)

        if stream.user_name not in self.user_info:
            user = await self.get_user_info(stream.user_name)
        else:
            user = self.user_info[stream.user_name]

        for gid in self.directed_data[stream.user_name]:
            guild = self.bot.get_guild(gid)
            gdb = GuildDateBases(gid)
            twitch_data = await gdb.get('twitch_notification')
            for id, data in twitch_data.items():
                if data['username'] == stream.user_name:
                    channel = self.bot.get_channel(data['channel_id'])
                    payload = get_payload(guild=guild, stream=stream, user=user)
                    mes_data = generate_message(lord_format(data.get('message', DEFAULT_TWITCH_MESSAGE), payload))
                    await channel.send(**mes_data)

    async def callback_on_stop(self, username: str):
        ...

    async def add_channel(self, guild_id: int, username: str) -> None:
        if username not in self.usernames:
            with_started, _ = await self.is_streaming(username)
            if with_started:
                self.twitch_streaming.add(username)
            self.usernames.add(username)

        self.directed_data.setdefault(username, set())
        self.directed_data[username].add(guild_id)

    async def check_token(self) -> None:
        if self.twitch_api_access_token is None or time.time() > self.twitch_api_access_token_end:
            await self.get_oauth_token()

    async def get_oauth_token(self) -> None:
        url = 'https://id.twitch.tv/oauth2/token'
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        json = await self.request('POST', url, with_auth=False, data=data)

        if json is None:
            return

        self.twitch_api_access_token_end = json['expires_in']+time.time()
        self.twitch_api_access_token = json['access_token']

    async def get_user_info(self, username: str) -> Optional[User]:
        await self.check_token()

        url = 'https://api.twitch.tv/helix/users'
        params = {
            'login': username
        }
        headers = {
            'Client-ID': self.client_id,
            'Authorization': 'Bearer ' + self.twitch_api_access_token
        }

        data = await self.request('GET', url, params=params, headers=headers)

        if data is not None and len(data['data']) > 0:
            user = User(**data['data'][0])
            self.user_info[username] = user
            return user

    async def is_streaming(self, username: str) -> Tuple[bool, Optional[Stream]]:
        await self.check_token()

        url = 'https://api.twitch.tv/helix/streams'
        params = {
            'user_login': username
        }
        headers = {
            'Client-ID': self.client_id,
            'Authorization': 'Bearer ' + self.twitch_api_access_token
        }
        data = await self.request('GET', url, params=params, headers=headers)

        if data is not None and len(data['data']) > 0:
            return True, Stream(**data['data'][0])
        else:
            return False, None

    async def parse_twitch(self) -> None:
        if self.__running:
            return

        if self.client_id is None or self.client_secret is None:
            return
        await self.check_token()

        _log.debug('Started twitch parsing')

        for uid in self.usernames:
            with_started, _ = await self.is_streaming(uid)
            if with_started:
                self.twitch_streaming.add(uid)

        self.__running = True
        while True:
            await asyncio.sleep(self.heartbeat_timeout)
            if not self.__running:
                return
            self.last_heartbeat = time.time()

            tasks = []
            for uid in self.usernames:
                try:
                    with_started, data = await self.is_streaming(uid)
                except Exception as exp:
                    _log.error('An error was received when executing the request (%s)',
                               uid,
                               exc_info=exp)
                    with_started, data = False, None

                if with_started and uid not in self.twitch_streaming:
                    self.twitch_streaming.add(uid)
                    tasks.append(self.callback_on_start(data))
                if not with_started and uid in self.twitch_streaming:
                    self.twitch_streaming.remove(uid)
                    tasks.append(self.callback_on_stop(uid))
            await asyncio.gather(*tasks)
