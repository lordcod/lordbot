from typing import (
    Optional,
    List,
    TypedDict
)

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


class RoleShopPayload(TypedDict):
    role_id: int
    amount: int
    limit: Optional[int]
    name: Optional[str]
    description: Optional[str]
    using_limit: Optional[int]
