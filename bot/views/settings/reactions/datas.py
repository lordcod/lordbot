from bot.databases.db import GuildDateBases
import nextcord
from bot.misc import utils
from bot.misc.utils import is_emoji
from  .. import reactions
from ...settings import DefaultSettingsView
from .modalBuilder import ModalsBuilder
from bot.languages.settings import (
    reactions as reaction_langs,
    button as button_name
)

class ReactData(DefaultSettingsView):
    def __init__(self,channel,channel_data) -> None:
        self.gdb = GuildDateBases(channel.guild.id)
        locale = self.gdb.get('language')
        self.forum_message  = self.gdb.get('reactions',{})
        
        self.channel_data = channel_data
        self.channel = channel
        super().__init__()
        
        self.back.label = button_name.back.get(locale)
        self.edit_reactions.label = reaction_langs.datas.editreact.get(locale)
        self.delete_reactions.label = reaction_langs.datas.delreact.get(locale)
    
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = reactions.AutoReactions(interaction.guild)
        
        await interaction.message.edit(embed=view.embed,view=view)
    
    @nextcord.ui.button(label='Edit reaction',style=nextcord.ButtonStyle.primary)
    async def edit_reactions(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = ModalsBuilder(interaction.guild_id,self.channel.id)
        
        await interaction.response.send_modal(modal)
    
    @nextcord.ui.button(label='Delete reaction',style=nextcord.ButtonStyle.red)
    async def delete_reactions(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        channel_id = self.channel.id
        del self.forum_message[channel_id]
        
        self.gdb.set('reactions',self.forum_message)
        
        view = reactions.AutoReactions(interaction.guild)
        await interaction.message.edit(embed=view.embed,view=view)
