from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Optional,
    List,
    TypedDict,
    Dict,
    Tuple,
)

if TYPE_CHECKING:
    from bot.misc.logstool import LogType


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


class PartialIdeasPayload(TypedDict):
    enabled: bool
    channel_suggest_id: int
    message_suggest_id: int
    channel_offers_id: int


class IdeasPayload(PartialIdeasPayload, total=True):
    cooldown: Optional[int]
    channel_approved_id: Optional[int]
    channel_denied_id: Optional[int]
    moderation_role_ids: Optional[List[int]]
    reaction_system: Optional[int]
    thread_delete: Optional[bool]
    allow_image: Optional[bool]
    # User id,  moderator_id, reason
    ban_users: Optional[List[Tuple[int, int, str]]]
    # User id, moderator_id, Timestamp, reason
    muted_users: Optional[List[Tuple[int, int, float, str]]]


class RoleShopPayload(TypedDict):
    role_id: int
    amount: int
    limit: Optional[int]
    name: Optional[str]
    description: Optional[str]
    using_limit: Optional[int]


LogsPayload = Dict[int, List['LogType']]


class ReactionRoleItemPayload(TypedDict):
    reactions: Dict[str, int]
    channel_id: int


ReactionRolePayload = Dict[int, ReactionRoleItemPayload]
