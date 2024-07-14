from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: str
    login: str
    display_name: str
    type: str
    broadcaster_type: str
    description: str
    profile_image_url: str
    offline_image_url: str
    view_count: int
    created_at: str


@dataclass
class Stream:
    id: str
    user_id: str
    user_login: str
    user_name: str
    type: str
    title: str
    viewer_count: int
    started_at: str
    language: str
    thumbnail_url: str
    tag_ids: list
    tags: list
    is_mature: bool
    game_name: Optional[str] = None
    game_id: Optional[str] = None

    @property
    def url(self):
        return f'https://www.twitch.tv/{self.user_login}'
