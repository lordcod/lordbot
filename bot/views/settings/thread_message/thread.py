from bot.databases.db import GuildDateBases
import nextcord
from bot.misc import utils


class EditModalsBuilder(nextcord.ui.Modal):
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
        forum_message  = gdb.get('thread_messages',{})
        
        content = self.content.value
        channel_id = self.channel_id
        
        channel_data = forum_message.get(channel_id,{})
        channel_data['content'] = content
        
        gdb.set('thread_messages',forum_message)



class ThreadData(nextcord.ui.View):
    def __init__(self,channel,channel_data) -> None:
        self.gdb = GuildDateBases(channel.guild.id)
        self.forum_message  = self.gdb.get('thread_messages',{})
        
        self.channel_data = channel_data
        self.channel = channel
        super().__init__()
    
    @nextcord.ui.button(label='Посмотреть сообщение',style=nextcord.ButtonStyle.blurple)
    async def message(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        channel_data = self.channel_data
        
        if not channel_data:
            await interaction.response.send_message("Сообщения не найдено")
        
        content = channel_data.get('content','')
        content = await utils.generate_message(content)
        await interaction.response.send_message(**content,ephemeral=True)
    
    @nextcord.ui.button(label='Изменить сообщение',style=nextcord.ButtonStyle.primary)
    async def edit_message(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(EditModalsBuilder(self.channel.id))
    
    @nextcord.ui.button(label='Удалить сообщение',style=nextcord.ButtonStyle.red)
    async def delete_message(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        channel_id = self.channel.id
        del self.forum_message[channel_id]
        
        
        self.gdb.set('thread_messages',self.forum_message)
        
        await interaction.response.send_message("Сообщение успешно удалено!",ephemeral=True,delete_after=5)

