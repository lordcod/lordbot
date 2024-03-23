from typing import (
    Optional,
    List,
    Tuple,
    TypedDict
)


class PartialIdeasPayload(TypedDict):
    enabled: bool
    channel_suggest_id: int
    message_suggest_id: int
    channel_offers_id: int


class IdeasPayload(PartialIdeasPayload, total=True):
    cooldown: Optional[int]
    channel_approved_id: Optional[int]
    moderation_role_ids: Optional[List[int]]
    reaction_system: Optional[int]
    thread_delete: Optional[bool]
    # User id,  moderator_id, reason
    ban_users: Optional[List[Tuple[int, int, str]]]
    # User id, moderator_id, Timestamp, reason
    muted_users: Optional[List[Tuple[int, int, float, str]]]
