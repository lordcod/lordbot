import nextcord
from bot.databases.db import GuildDateBases
from bot.misc.utils import is_emoji
from  .. import reactions
from ...settings import DefaultSettingsView
from .modalBuilder import ModalsBuilder
from bot.languages.settings import (
    reactions as reaction_langs,
    button as button_name
)

class DropDownBuilder(nextcord.ui.ChannelSelect):
    def __init__(self,guild_id) -> None:
        self.gdb = GuildDateBases(guild_id)
        locale = self.gdb.get('language')
        
        super().__init__(
            placeholder=reaction_langs.addres.ph.get(locale)
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel: nextcord.TextChannel = self.values[0]
        reacts: dict  = self.gdb.get('reactions')
        locale: str = self.gdb.get('language')
        
        if channel.id in reacts:
            await interaction.response.send_message(reaction_langs.addres.cherror.get(locale))
            return
        
        modal = ModalsBuilder(interaction.guild_id,channel.id) 
        
        await interaction.response.send_modal(modal)

class ViewBuilder(DefaultSettingsView):
    def __init__(self,guild_id: int) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        
        super().__init__()
        
        self.back.label = button_name.back.get(locale)
        
        DDB = DropDownBuilder(guild_id)
        
        self.add_item(DDB)
    
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = reactions.AutoReactions(interaction.guild)
        
        await interaction.message.edit(embed=view.embed,view=view)