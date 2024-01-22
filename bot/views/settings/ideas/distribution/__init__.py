from .approved import ApprovedView
from .moderation_roles import ModerationRolesView
from .offers import OffersView
from .suggest import SuggestView

distrubuters = {
    'approved': ApprovedView,
    'moderation-roles': ModerationRolesView,
    'offers': OffersView,
    'suggest': SuggestView,
}

