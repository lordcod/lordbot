from typing import Optional
import nextcord
from bot.databases.db import GuildDateBases
from  .. import thread_message 
from ...settings import DefaultSettingsView

class ModalsBuilder(nextcord.ui.Modal):
    def __init__(self,channel_id) -> None:
        self.channel_id = channel_id
        super().__init__('Авто-сообщение')
        
        self.content = nextcord.ui.TextInput(
            label='Сообщение:',
            placeholder='Вы также можете пользоваться embed-builder'
        )
        
        self.add_item(self.content)
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        forum_message = gdb.get('thread_messages',{})
        content = self.content.value
        channel_id = self.channel_id
        
        if channel_id in forum_message:
            await interaction.response.send_message("На этот канал уже установлено авто-сообщения")
            return
        
        forum_message[channel_id] = {}
        forum_message[channel_id]['content'] = content
        
        gdb.set('thread_messages',forum_message)
        
        view = thread_message.AutoThreadMessage(interaction.guild)
        await interaction.message.edit(embed=view.embed,view=view)

class DropDownBuilder(nextcord.ui.ChannelSelect):
    def __init__(self) -> None:
        super().__init__(
            placeholder='Выберете канал для авто-сообщений', 
            channel_types=[nextcord.ChannelType.forum,nextcord.ChannelType.text,nextcord.ChannelType.news]
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel = self.values[0]
        await interaction.response.send_modal(ModalsBuilder(channel.id))

class ViewBuilder(DefaultSettingsView):
    def __init__(self) -> None:
        super().__init__()
        
        DDB = DropDownBuilder()
        
        self.add_item(DDB)
    
    
    @nextcord.ui.button(label='Назад',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = thread_message.AutoThreadMessage(interaction.guild)
        
        await interaction.message.edit(embed=view.embed,view=view)