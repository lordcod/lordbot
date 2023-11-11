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
            
            nextcord.SelectOption(
                label="Auto Reactionsⁿᵉʷ", emoji=Emoji.reactions, value='Reactions'
            ),
            nextcord.SelectOption(
                label="Auto Translateⁿᵉʷ", emoji=Emoji.auto_translate, value='Auto_Translate'
            ),
            nextcord.SelectOption(
                label="Auto Thread-Forum Messageⁿᵉʷ", emoji=Emoji.thread_message, value='Thread_Message'
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
        lister = {
            'Economy': settings.Economy(interaction.guild_id),
            'Color': settings.Color(interaction.guild_id),
            'Languages':settings.Languages(interaction.guild_id),
            'Prefix':settings.Prefix(interaction.guild_id),
            'Reactions':settings.AutoReactions(interaction.guild_id),
            'Auto_Translate':settings.AutoTranslate(interaction.guild_id),
            'Thread_Message':settings.AutoThreadMessage(interaction.guild_id),
        }
        view = lister[value]
        if view.type == 'modal':
            await interaction.response.send_modal(view)
        if view.type == 'view':
            await interaction.response.send_message(**view.content,view=view,ephemeral=True)