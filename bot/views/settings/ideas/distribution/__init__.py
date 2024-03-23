from .approved import ApprovedView
from .moderation_roles import ModerationRolesView
from .offers import OffersView
from .suggest import SuggestView
from .cooldown import CooldownView

distrubuters = {
    'approved': ApprovedView,
    'moderation_roles': ModerationRolesView,
    'offers': OffersView,
    'suggest': SuggestView,
    'cooldown': CooldownView
}
