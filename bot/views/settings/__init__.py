import nextcord
class DefaultSettingsView(nextcord.ui.View):
    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        print(1)
        if not interaction.user.guild_permissions.manage_guild:
            print(2)
            await interaction.response.send_message('You don\'t have the authority to use the settings',ephemeral=True)
            return False
        print(3)
        return True

from .color import ColorView as Color
from .economy import Economy
from .prefix import PrefixView as Prefix
from .languages import Languages
from .reactions import AutoReactions
from .thread_message import AutoThreadMessage
from .auto_translate import AutoTranslate


