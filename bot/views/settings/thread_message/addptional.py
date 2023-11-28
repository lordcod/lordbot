from typing import Optional
import nextcord
from bot.databases.db import GuildDateBases
from  .. import thread_message 
from ...settings import DefaultSettingsView
from .modalsBuilder import ModalsBuilder
from bot.languages.settings import (
    thread as thread_langs,
    button as button_name
)

class DropDownBuilder(nextcord.ui.ChannelSelect):
    def __init__(self,guild_id) -> None:
        self.gdb = GuildDateBases(guild_id)
        locale = self.gdb.get('language')
        super().__init__(
            placeholder=thread_langs.addptional.mph.get(locale), 
            channel_types=[nextcord.ChannelType.forum,nextcord.ChannelType.text,nextcord.ChannelType.news]
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel = self.values[0]
        locale = self.gdb.get('language')
        forum_message = self.gdb.get('thread_messages',{})
        
        
        if channel.id in forum_message:
            await interaction.response.send_message(thread_langs.addptional.channel_error.get(locale))
            return
        
        modal = ModalsBuilder(interaction.guild_id,channel.id)
        
        await interaction.response.send_modal(modal)

class ViewBuilder(DefaultSettingsView):
    def __init__(self,guild_id) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        
        super().__init__()
        
        self.back.label = button_name.back.get(locale)
        
        DDB = DropDownBuilder(guild_id)
        
        self.add_item(DDB)
    
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = thread_message.AutoThreadMessage(interaction.guild)
        
        await interaction.message.edit(embed=view.embed,view=view)