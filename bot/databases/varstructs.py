from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Optional,
    List,
    TypedDict,
    Dict
)

if TYPE_CHECKING:
    from bot.misc.logstool import LogType

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


LogsPayload = Dict[int, List['LogType']]
