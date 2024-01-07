from .approved import ApprovedView
from .moderation_roles import ModerationRolesView
from .offers import OffersView
from .suggest import SuggestView

distrubuters = {
    'approved': OffersView,
    'moderation-roles': ModerationRolesView,
    'offers': ModerationRolesView,
    'suggest': ApprovedView,
}

