from .music import MusicView
from .ideas import IdeasView
from .welcomer import WelcomerView
from .auto_role import AutoRoleView
from .permisson_command import CommandsDataView
from .thread_message import AutoThreadMessage
from .color import ColorView as Color
from .economy import Economy
from .prefix import PrefixView as Prefix
from .languages import Languages
from .reactions import AutoReactions


moduls = {
    'Economy': Economy,
    'Color': Color,
    'Languages': Languages,
    'Prefix': Prefix,
    'CommandPermission':   CommandsDataView,
    'Music': MusicView,
    'Welcomer': WelcomerView,
    'AutoRoles': AutoRoleView,
    'Reactions': AutoReactions,
    'ThreadMessage': AutoThreadMessage,
    'Ideas': IdeasView,
}
