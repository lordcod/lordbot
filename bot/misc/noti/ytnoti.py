from __future__ import annotations

import asyncio
import logging
import time
from typing import List,  TYPE_CHECKING
import os
import xmltodict
from datetime import datetime

try:
    from .ytypes import Channel, Thumbnail, Stats, Timestamp, Video, ShortChannel, VideoHistory
except ImportError:
    from ytypes import Channel, Thumbnail, Stats, Timestamp, Video, ShortChannel, VideoHistory

if TYPE_CHECKING:
    from bot.misc.lordbot import LordBot

_log = logging.getLogger(__name__)


class YtNoti:
    def __init__(self, bot: LordBot, apikey: str = os.getenv('YOUTUBE_API_KEY')) -> None:
        self.bot = bot
        self.apikey = apikey
        self.channel_ids = ['UC13nzpbDHuNhW4rmAVl7JhA']  # , 'UCPCTEN8OWHdJGxfMggbyGGg']
        self.video_history = VideoHistory()
        self.running = True

        self.heartbeat_timeout = 180
        self.last_heartbeat = time.time()

    async def callback(self, video: Video) -> None:
        _log.debug('%s publish new video: %s (%s)', video.channel.name, video.title, video.url)

        guild = self.bot.get_guild(1252627796929282118)
        channel = guild.get_channel(1252984316485570570)
        await channel.send(f'Тут у {video.channel.name} новое видео вышло, го смотреть?\n'
                           f'{video.url}\n'
                           f'|| {guild.default_role.mention} ||')

    def get_videos_from_body(self, body: dict) -> List[Video]:
        videos = []
        entries = body["feed"]["entry"] if isinstance(body["feed"]["entry"], list) else [body["feed"]["entry"]]

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
                    likes=int(entry["media:group"]["media:community"]["media:starRating"]["@count"]),
                    views=int(entry["media:group"]["media:community"]["media:statistics"]["@views"]),
                )

            timestamp = Timestamp(
                published=datetime.strptime(entry["published"], "%Y-%m-%dT%H:%M:%S%z"),
                updated=datetime.strptime(entry["updated"], "%Y-%m-%dT%H:%M:%S%z")
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

    async def add_channel(self, channel_id: str) -> None:
        videos = await self.get_video_history(channel_id)
        vhd = self.video_history.get_diff(videos)
        self.video_history.extend(vhd)
        self.channel_ids.append(channel_id)

    async def get_video_history(self, channel_id: str) -> List[Video]:
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        async with self.bot.session.get(url) as res:
            body = await res.read()
        json = xmltodict.parse(body.decode())
        return self.get_videos_from_body(json)

    async def get_channel_ids(self, query: str) -> List[Channel]:
        response = {}

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

        url = 'https://www.googleapis.com/youtube/v3/channels'
        params = list({
            'part': 'snippet,id',
            'type': 'channel',
            'maxResults': 15,
            'key': self.apikey
        }.items())
        for data in json['items']:
            channel_id = data['id']['channelId']
            response[channel_id] = {
                'id': channel_id,
                'name': data['snippet']['title'],
                'description': data['snippet']['description'],
                'thumbnail': data['snippet']['thumbnails']['default']['url'],
                'created_at': datetime.fromisoformat(data['snippet']['publishedAt'])
            }
            params.append(('id', channel_id))
        async with self.bot.session.get(url, params=params) as res:
            json = await res.json()
            res.raise_for_status()
        for data in json['items']:
            channel_id = data['id']
            response[channel_id]['custom_url'] = data['snippet']['customUrl']

        return [Channel(**data) for data in response.values()]

    async def parse_youtube(self) -> None:
        for cid in self.channel_ids:
            videos = await self.get_video_history(cid)
            vhd = self.video_history.get_diff(videos)
            self.video_history.extend(vhd)

        while self.running:
            await asyncio.sleep(self.heartbeat_timeout)
            self.last_heartbeat = time.time()

            gvhd = []
            for cid in self.channel_ids:
                videos = await self.get_video_history(cid)
                vhd = self.video_history.get_diff(videos)
                self.video_history.extend(vhd)
                gvhd.extend(vhd)
            await asyncio.gather(*[self.callback(v) for v in gvhd])
