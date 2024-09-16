from typing import Dict

from bot.misc.utils import AsyncSterilization
from bot.views.settings.ideas.distribution.alllow_image import AllowImageFunc
from bot.views.settings.ideas.distribution.threads import IdeasThreadsView

from .base import OptionItem
from .approved import ApprovedView
from .moderation_roles import ModerationRolesView
from .offers import OffersView
from .suggest import SuggestView
from .cooldown import CooldownView

distrubuters: Dict[str, AsyncSterilization[OptionItem]] = {
    'approved': ApprovedView,
    'mod_roles': ModerationRolesView,
    'offers': OffersView,
    'suggest': SuggestView,
    'cooldown': CooldownView,
    'allow_image': AllowImageFunc,
    'threads': IdeasThreadsView
}
