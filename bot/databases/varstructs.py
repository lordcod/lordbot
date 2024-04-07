from typing import (
    Optional,
    List,
    TypedDict
)


class GiveawayData(TypedDict):
    guild_id: int
    channel_id: int
    sponsor_id: int
    prize: str
    description: Optional[str]
    quantity: int
    date_end: int | float
    types: List[int]
    entries_ids: List[int]
    completed: bool
    winners: Optional[List[int]]
    key: str
    token: str


IdeasPayload = TypedDict(
    'IdeasPayload',
    {
        "enabled": Optional[bool],
        "cooldown": Optional[int],

        "channel-suggest-id": int,
        "message-suggest-id": int,

        "channel-offers-id": int,
        "channel-approved-id": int,

        "moderation-role-ids": List[int]
    }
)
