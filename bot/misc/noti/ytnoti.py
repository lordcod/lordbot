from __future__ import annotations

import asyncio
import logging
import time
from typing import List,  TYPE_CHECKING,  Dict
import os
import nextcord
import xmltodict
from datetime import datetime, timedelta

from bot.databases.handlers.guildHD import GuildDateBases
from bot.misc.utils import get_payload, generate_message, lord_format
from bot.resources.info import DEFAULT_YOUTUBE_MESSAGE

try:
    from .ytypes import Channel, Thumbnail, Stats, Timestamp, Video, ShortChannel, VideoHistory
except ImportError:
    from ytypes import Channel, Thumbnail, Stats, Timestamp, Video, ShortChannel, VideoHistory

if TYPE_CHECKING:
    from bot.misc.lordbot import LordBot

_log = logging.getLogger(__name__)
handler = logging.FileHandler(f"logs/{__name__}.log")
handler.setFormatter(logging.Formatter(
    '[%(asctime)s][%(name)s][%(levelname)s]  %(message)s (%(filename)s:%(lineno)d)', '%m-%d-%Y %H:%M:%S'))
_log.addHandler(handler)


class YtNoti:
    def __init__(self, bot: LordBot, apikey: str = os.getenv('YOUTUBE_API_KEY')) -> None:
        self.bot = bot
        self.apikey = apikey

        self.running = True
        self.channel_ids = set()
        self.video_history = VideoHistory()
        self.directed_data = {}
        self.user_info: Dict[int, Channel] = {}

        self.heartbeat_timeout = 180
        self.last_heartbeat = time.time()

    async def callback(self, video: Video) -> None:
        _log.debug('%s publish new video: %s (%s)',
                   video.channel.name, video.title, video.url)

        if datetime.today()-timedelta(hours=1) > video.timestamp.published:
            _log.debug('load video error (queue violation)',
                       video.channel.name, video.title, video.url)
            return

        for gid in self.directed_data[video.channel.id]:
            guild = self.bot.get_guild(gid)
            gdb = GuildDateBases(gid)
            yt_data = await gdb.get('youtube_notification')
            for id, data in yt_data.items():
                if data['yt_id'] == video.channel.id:
                    channel = self.bot.get_channel(data['channel_id'])
                    payload = get_payload(guild=guild, video=video)
                    mes_data = await generate_message(lord_format(data.get('message', DEFAULT_YOUTUBE_MESSAGE), payload))
                    await channel.send(**mes_data)

    def parse_channel(self, data: dict) -> Channel:
        channel_id = data['id']
        if isinstance(channel_id, dict):
            channel_id = channel_id['channelId']

        channel = Channel(
            id=channel_id,
            name=data['snippet']['title'],
            description=data['snippet']['description'],
            thumbnail=data['snippet']['thumbnails']['default']['url'],
            created_at=datetime.fromisoformat(data['snippet']['publishedAt']),
            custom_url=data['snippet'].get('customUrl', None),
        )
        self.user_info[channel.id] = channel
        return channel

    def get_videos_from_body(self, body: dict) -> List[Video]:
        videos = []
        entries = body["feed"]["entry"] if isinstance(
            body["feed"]["entry"], list) else [body["feed"]["entry"]]

        for entry in entries:
            channel = ShortChannel(
                id=entry["yt:channelId"],
                name=entry["author"]["name"],
                url=entry["author"]["uri"],
                created_at=datetime.fromisoformat(body["feed"]["published"])
            )

            thumbnail = Thumbnail(
                url=entry["media:group"]["media:thumbnail"]["@url"],
                width=int(entry["media:group"]["media:thumbnail"]["@width"]),
                height=int(entry["media:group"]["media:thumbnail"]["@height"]),
            )

            stats = None
            if "media:community" in entry["media:group"]:
                stats = Stats(
                    likes=int(entry["media:group"]["media:community"]
                              ["media:starRating"]["@count"]),
                    views=int(entry["media:group"]["media:community"]
                              ["media:statistics"]["@views"]),
                )

            timestamp = Timestamp(
                published=datetime.strptime(
                    entry["published"], "%Y-%m-%dT%H:%M:%S%z"),
                updated=datetime.strptime(
                    entry["updated"], "%Y-%m-%dT%H:%M:%S%z")
            )

            videos.append(Video(
                id=entry["yt:videoId"],
                title=entry["title"],
                description=entry["media:group"]["media:description"] or "",
                url=entry["link"]["@href"],
                thumbnail=thumbnail,
                stats=stats,
                timestamp=timestamp,
                channel=channel
            ))

        return videos

    async def add_channel(self, guild_id: int, channel_id: str) -> None:
        if channel_id not in self.channel_ids:
            videos = await self.get_video_history(channel_id)
            vhd = self.video_history.get_diff(videos)
            self.video_history.extend(vhd)
            self.channel_ids.add(channel_id)
        self.directed_data.setdefault(channel_id, set())
        self.directed_data[channel_id].add(guild_id)

    async def get_video_history(self, channel_id: str) -> List[Video]:
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        async with self.bot.session.get(url) as res:
            body = await res.read()
        json = xmltodict.parse(body.decode())
        return self.get_videos_from_body(json)

    async def search(self, query: str) -> List[Channel]:
        ret = []

        url = 'https://youtube.googleapis.com/youtube/v3/search'
        params = {
            'part': 'snippet,id',
            'type': 'channel',
            'maxResults': 15,
            'q': query,
            'key': self.apikey
        }

        async with self.bot.session.get(url, params=params) as res:
            json = await res.json()
            res.raise_for_status()

        for data in json['items']:
            ret.append(self.parse_channel(data))

        return ret

    async def get_channel_ids(self, ids: List[str]) -> List[Channel]:
        ret = []

        url = 'https://www.googleapis.com/youtube/v3/channels'
        params = list({
            'part': 'snippet,id',
            'type': 'channel',
            'maxResults': 15,
            'key': self.apikey
        }.items())

        for id in ids:
            params.append(('id', id))

        async with self.bot.session.get(url, params=params) as res:
            json = await res.json()
            res.raise_for_status()

        for data in json['items']:
            ret.append(self.parse_channel(data))

        return ret

    async def get_channel_ids_additionally(self, query: str) -> List[Channel]:
        search_result = await self.search(query)
        geted_result = await self.get_channel_ids([data.id for data in search_result])
        return geted_result

    async def parse_youtube(self) -> None:
        for cid in self.channel_ids:
            videos = await self.get_video_history(cid)
            vhd = self.video_history.get_diff(videos)
            self.video_history.extend(vhd)

        _log.trace('Started youtube parsing, cheking: %s, count of videos found: %s',
                   self.channel_ids,  len(self.video_history.videos))

        while self.running:
            await asyncio.sleep(self.heartbeat_timeout)
            self.last_heartbeat = time.time()

            gvhd = []
            for cid in self.channel_ids:
                videos = await self.get_video_history(cid)
                vhd = self.video_history.get_diff(videos)
                self.video_history.extend(vhd)
                gvhd.extend(vhd)

                _log.trace('Fetched from %s data %s', cid, vhd)
                if videos:
                    _log.trace('%s last video: %s',
                               videos[0].channel.name, videos[0].url)
            await asyncio.gather(*[self.callback(v) for v in gvhd])
