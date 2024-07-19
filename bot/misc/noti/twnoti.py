from __future__ import annotations

import asyncio
import os
import time
import logging
from typing import TYPE_CHECKING, Optional, Tuple

from aiohttp.web_exceptions import HTTPUnauthorized
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
handler = logging.FileHandler(f"logs/{__name__}.log")
handler.setFormatter(logging.Formatter(
    '[%(asctime)s][%(name)s][%(levelname)s]  %(message)s (%(filename)s:%(lineno)d)', '%m-%d-%Y %H:%M:%S'))
_log.addHandler(handler)


class TwNoti:
    twitch_api_access_token: Optional[str] = None
    twitch_api_refresh_token: Optional[str] = None
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

        self.running = True
        self.usernames = set()
        self.twitch_streaming = set()
        self.user_info = {}
        self.directed_data = {}

        self.heartbeat_timeout = 180
        self.last_heartbeat = time.time()

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
                    mes_data = await generate_message(lord_format(data.get('message', DEFAULT_TWITCH_MESSAGE), payload))
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
        if self.twitch_api_access_token is None:
            await self.get_oauth_token()
        if time.time() > self.twitch_api_access_token_end:
            try:
                await self.refresh_oauth_token()
            except HTTPUnauthorized:
                await self.get_oauth_token()

    async def get_oauth_token(self) -> None:
        url = 'https://id.twitch.tv/oauth2/token'
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        async with self.bot.session.post(url, data=data) as response:
            response.raise_for_status()
            json = await response.json()

        self.twitch_api_access_token_end = json['expires_in']+time.time()
        self.twitch_api_access_token = json['access_token']
        self.twitch_api_refresh_token = json['refresh_token']

    async def refresh_oauth_token(self) -> None:
        url = 'https://id.twitch.tv/oauth2/token'
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.twitch_api_refresh_token
        }
        async with self.bot.session.post(url, data=data) as response:
            response.raise_for_status()
            json = await response.json()

        self.twitch_api_access_token_end = json['expires_in']+time.time()
        self.twitch_api_access_token = json['access_token']
        self.twitch_api_refresh_token = json['refresh_token']

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
        async with self.bot.session.get(url, params=params, headers=headers) as response:
            data = await response.json()
            if response.status == 401:
                await self.refresh_oauth_token()
            if not response.ok:
                _log.trace('It was not possible to get data from the api, status: %s, data: %s', response.status, data)
                return

        if len(data['data']) > 0:
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
        async with self.bot.session.get(url, params=params, headers=headers) as response:
            data = await response.json()
            if response.status == 401:
                await self.refresh_oauth_token()
            if not response.ok:
                _log.trace('It was not possible to get data from the api, status: %s, data: %s', response.status, data)
                return False, None

        if len(data['data']) > 0:
            return True, Stream(**data['data'][0])
        else:
            return False, None

    async def parse_twitch(self) -> None:
        if self.client_id is None or self.client_secret is None:
            return
        await self.check_token()

        for uid in self.usernames:
            with_started, _ = await self.is_streaming(uid)
            if with_started:
                self.twitch_streaming.add(uid)

        _log.trace('Started twitch parsing, cheking: %s, current strems: %s',
                   self.usernames,  self.twitch_streaming)

        while self.running:
            await asyncio.sleep(self.heartbeat_timeout)
            self.last_heartbeat = time.time()

            tasks = []
            for uid in self.usernames:
                with_started, data = await self.is_streaming(uid)

                _log.trace('Fetched from %s data %s %s',
                           uid, with_started, data)

                if with_started and uid not in self.twitch_streaming:
                    self.twitch_streaming.add(uid)
                    tasks.append(self.callback_on_start(data))
                if not with_started and uid in self.twitch_streaming:
                    self.twitch_streaming.remove(uid)
                    tasks.append(self.callback_on_stop(uid))
            await asyncio.gather(*tasks)
