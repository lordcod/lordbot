import nextcord

from bot.resources.languages import Emoji
from . import settings



class SetDropdown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(
                label="Economy", emoji=Emoji.economy, value='Economy'
            ),
            nextcord.SelectOption(
                label="Languages", emoji=Emoji.languages, value='Languages'
            ),
            nextcord.SelectOption(
                label="Prefix", emoji=Emoji.prefix, value='Prefix'
            ),
            nextcord.SelectOption(
                label="Color", emoji=Emoji.colour, value='Color'
            ),
        ]

        super().__init__(
            placeholder="Choose settings...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction):
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message('You don\'t have the authority to use the settings',ephemeral=True)
            return
        
        value = self.values[0]
        view = getattr(settings,value)
        view = view()
        if view.type == 'modal':
            await interaction.response.send_modal(view)
        if view.type == 'view':
            await interaction.response.send_message(**view.content,view=view,ephemeral=True)