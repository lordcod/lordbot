from typing import (
    Optional,
    Union,
    List,
    TypedDict
)

IdeasPayload = TypedDict(
    'IdeasPayload', 
    {
        "enabled": Optional[bool],
        
        "channel-suggest-id": int,
        "message-suggest-id": int,
        
        "channel-offers-id":int,
        "channel-approved-id":int,
        
        "moderation-role-ids":List[int]
    }
)
