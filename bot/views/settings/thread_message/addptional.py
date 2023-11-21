from typing import Optional
import nextcord
from bot.databases.db import GuildDateBases
from  .. import thread_message 
from ...settings import DefaultSettingsView
from bot.languages.settings import (
    thread as thread_langs,
    button as button_name
)

class ModalsBuilder(nextcord.ui.Modal):
    def __init__(self,guild_id,channel_id) -> None:
        self.channel_id = channel_id
        
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        
        super().__init__(thread_langs.addptional.title.get(locale))
        
        self.content = nextcord.ui.TextInput(
            label=thread_langs.addptional.tilabel.get(locale),
            placeholder=thread_langs.addptional.tiph.get(locale)
        )
        self.add_item(self.content)
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        content = self.content.value
        channel_id = self.channel_id
        
        gdb = GuildDateBases(interaction.guild_id)
        locale = gdb.get('language')
        forum_message = gdb.get('thread_messages',{})
        
        if channel_id in forum_message:
            await interaction.response.send_message(thread_langs.addptional.cherr.get(locale))
            return
        
        forum_message[channel_id] = {}
        forum_message[channel_id]['content'] = content
        
        gdb.set('thread_messages',forum_message)
        
        view = thread_message.AutoThreadMessage(interaction.guild)
        await interaction.message.edit(embed=view.embed,view=view)

class DropDownBuilder(nextcord.ui.ChannelSelect):
    def __init__(self,guild_id) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        super().__init__(
            placeholder=thread_langs.addptional.mph.get(locale), 
            channel_types=[nextcord.ChannelType.forum,nextcord.ChannelType.text,nextcord.ChannelType.news]
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel = self.values[0]
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