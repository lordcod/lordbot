from ._view import DefaultSettingsView
from .ideas import IdeasView
from .welcomer import WelcomerView
from .auto_role import AutoRoleView
from .permisson_command import CommandsDataView
from .thread_message import AutoThreadMessage
from .reactions import AutoReactions
from .languages import Languages
from .prefix import PrefixView as Prefix
from .economy import Economy
from .color import ColorView as Color


moduls = {
    'Economy': Economy,
    'Color': Color,
    'Languages': Languages,
    'Prefix': Prefix,
    'CommandPermission':   CommandsDataView,
    'Welcomer': WelcomerView,
    'AutoRoles': AutoRoleView,
    'Reactions': AutoReactions,
    'ThreadMessage': AutoThreadMessage,
    'Ideas': IdeasView,
}
