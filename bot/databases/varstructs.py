from __future__ import annotations


from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Optional,
    List,
    TypedDict,
    Dict,
    Tuple,
    Union,
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

Message = Union[str, Dict[str, Any]]


class TicketsMessagesPayload(TypedDict):
    panel: Message
    open: Message
    close: Message
    reopen: Message
    delete: Message


class TicketsNamesPayload(TypedDict):
    open: Optional[str]
    close: Optional[str]


class ButtonPayload(TypedDict):
    label: Optional[str]
    emoji: Optional[str]
    style: Optional[Literal[1, 2, 3, 4, 5]]


class SelectOptionPayload(TypedDict):
    label: str
    description: Optional[str]
    emoji: Optional[str]


class TicketsButtonsPayload(TypedDict):
    category_placeholder: str
    modal_placeholder: str
    faq_placeholder: str
    faq_option: SelectOptionPayload
    faq_button_open: ButtonPayload
    faq_button_create: ButtonPayload
    delete_button: ButtonPayload
    reopen_button: ButtonPayload
    close_button: ButtonPayload


class FaqItemPayload(SelectOptionPayload, total=True):
    response: Message


class FaqPayload(TypedDict):
    type: Optional[Literal[1, 2]]
    items:  List[FaqItemPayload]


class ModalItemPayload(TypedDict):
    label: str
    style: Optional[Literal[1, 2]]
    required: Optional[bool]
    placeholder: Optional[str]
    default_value: Optional[str]
    min_lenght: Optional[int]
    max_lenght: Optional[int]


class ButtonActionPayload(ButtonPayload, total=True):
    action: str
    data: Any


class PartialCategoryPayload(TypedDict):
    names: TicketsNamesPayload
    messages: TicketsMessagesPayload
    buttons: TicketsButtonsPayload
    actions_buttons: List[ButtonActionPayload]
    type: Optional[Literal[1, 2]]
    permissions: Optional[Dict[int, Tuple[int, int]]]
    category_id: Optional[int]
    closed_category_id: Optional[int]
    moderation_roles: Optional[List[int]]
    user_closed: Optional[bool]
    moderation_mention: Optional[bool]
    approved_roles: Optional[List[int]]
    saving_history: Optional[bool]
    auto_archived: Optional[int]
    modals: Optional[List[ModalItemPayload]]
    creating_embed_inputs: Optional[bool]
    user_tickets_limit: Optional[int]


class CategoryPayload(PartialCategoryPayload, ButtonPayload, total=True):
    channel_id: Optional[int] = None
    description: Optional[str] = None


class TicketsItemPayload(PartialCategoryPayload, total=True):
    channel_id: int
    message_id: int
    enabled: Optional[bool]
    faq: Optional[FaqPayload]
    category_type: Optional[int]
    categories: Optional[List[CategoryPayload]]
    global_user_tickets_limit: Optional[int]


TicketsPayload = Dict[int, TicketsItemPayload]


class UserTicketPayload(TypedDict):
    owner_id: int
    channel_id: int
    ticket_id: int
    category: CategoryPayload
    inputs: Dict[str, str]
    status: int
    index: int
    messages: Optional[List[dict]]


class TempChannelsPayload(TypedDict):
    channel_id: int
    category_id: int
    panel_channel_id: Optional[int]
    panel_message_id: Optional[int]
    enabled: Optional[bool]
    channel_name: Optional[str]
    channel_limit: Optional[int]
    advance_panel: Optional[bool]
    type_panel: Optional[int]
    type_message_panel: Optional[int]
    removed_mutes:  Optional[List[int]]


class TempChannelsItemPayload(TypedDict):
    channel_id: int
    owner_id: int
    status: int
    mutes: Optional[Dict[int, bool]]


class TwitchNotifiItemPayload(TypedDict):
    id: str
    channel_id: int
    username: str
    message: str


TwitchNotifiPayload = Dict[str, TwitchNotifiItemPayload]


class YoutubeNotifiItemPayload(TypedDict):
    id: str
    channel_id: int
    yt_name: str
    yt_id: str
    message: str


YoutubeNotifiPayload = Dict[str, YoutubeNotifiItemPayload]
