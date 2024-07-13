from __future__ import annotations

import asyncio
import os
import time
import logging
from typing import TYPE_CHECKING, Optional, Tuple

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

    def __init__(
        self,
        bot: LordBot,
        client_id: str = os.getenv('TWITCH_CLIENT_ID'),
        client_secret: str = os.getenv('TWITCH_CLIENT_SECRET')
    ) -> None:
        self.bot = bot
        self.client_id = client_id
        self.client_secret = client_secret
        self.usernames = ['f1ll666', 'dy6fuo']
        self.twitch_streaming = []
        self.running = True
        self.heartbeat_timeout = 180
        self.last_heartbeat = time.time()

    async def callback_on_start(self, stream: Stream):
        _log.debug('%s started stream', stream.user_name)
        if stream.user_name == 'f1ll666':
            guild = self.bot.get_guild(1179069504186232852)
            channel = guild.get_channel(1260965150953967637)
        else:
            guild = self.bot.get_guild(1252627796929282118)
            channel = guild.get_channel(1252984316485570570)

        await channel.send(f'{stream.user_name} запустил стрим, скорее присоединяйся\n'
                           f'{stream.url}\n'
                           f'|| {guild.default_role.mention} ||')

    async def callback_on_stop(self, username: str):
        ...

    async def add_channel(self, username: str) -> None:
        with_started, _ = await self.is_streaming(username)
        if with_started:
            self.twitch_streaming.append(username)
        self.usernames.append(username)

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
        self.twitch_api_access_token = json['access_token']

    async def get_user_info(self, username: str) -> Optional[User]:
        url = 'https://api.twitch.tv/helix/users'
        params = {
            'login': username
        }
        headers = {
            'Client-ID': self.client_id,
            'Authorization': 'Bearer ' + self.twitch_api_access_token
        }
        async with self.bot.session.get(url, params=params, headers=headers) as response:
            if not response.ok:
                return
            data = await response.json()

        if len(data['data']) > 0:
            return User(**data['data'][0])

    async def is_streaming(self, username: str) -> Tuple[bool, Optional[Stream]]:
        url = 'https://api.twitch.tv/helix/streams'
        params = {
            'user_login': username
        }
        headers = {
            'Client-ID': self.client_id,
            'Authorization': 'Bearer ' + self.twitch_api_access_token
        }
        async with self.bot.session.get(url, params=params, headers=headers) as response:
            if not response.ok:
                return False, None
            data = await response.json()

        if len(data['data']) > 0:
            return True, Stream(**data['data'][0])
        else:
            return False, None

    async def parse_twitch(self) -> None:
        if self.twitch_api_access_token is None:
            await self.get_oauth_token()

        for uid in self.usernames:
            with_started, _ = await self.is_streaming(uid)
            if with_started:
                self.twitch_streaming.append(uid)

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
                    self.twitch_streaming.append(uid)
                    tasks.append(self.callback_on_start(data))
                if not with_started and uid in self.twitch_streaming:
                    self.twitch_streaming.remove(uid)
                    tasks.append(self.callback_on_stop(uid))
            await asyncio.gather(*tasks)
