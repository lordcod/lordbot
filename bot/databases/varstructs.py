from typing import (
    Optional,
    Union,
    List,
    TypedDict
)

ParticleIdeasPayload = TypedDict(
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
