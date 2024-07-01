
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Channel:
    id: str
    name: str
    url: str
    created_at: datetime


@dataclass
class Thumbnail:
    url: str
    width: int
    height: int


@dataclass
class Stats:
    likes: int
    views: int


@dataclass
class Timestamp:
    published: datetime
    updated: datetime


@dataclass
class Video:
    id: str
    title: str
    description: str
    url: str
    thumbnail: Thumbnail
    stats: Stats | None
    timestamp: Timestamp
    channel: Channel


class VideoHistory:
    def __init__(self) -> None:
        self.videos: list[Video] = []

    def add(self, video: Video):
        self.videos.append(video)

    def has(self, video: Video):
        for v in self.videos:
            if v.id == video.id:
                return True
        return False
