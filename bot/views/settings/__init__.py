import nextcord

class DefaultSettingsView(nextcord.ui.View):
    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message('You don\'t have the authority to use the settings',ephemeral=True)
            return False
        return True


from .color import ColorView as Color
from .economy import Economy
from .prefix import PrefixView as Prefix
from .languages import Languages
from .reactions import AutoReactions
from .thread_message import AutoThreadMessage
from .permisson_command import CommandsDataView
from .greeting import Greeting 
from .ideas import IdeasView


moduls = {
    'Economy': Economy,
    
    'Color': Color,
    'Languages': Languages,
    'Prefix': Prefix,
    
    'CommandPermission': CommandsDataView,
    
    'Greeting':Greeting,
    'Reactions': AutoReactions,
    'ThreadMessage': AutoThreadMessage,
    
    'Ideas': IdeasView,
}