from bot.databases.db import GuildDateBases
import nextcord
from bot.misc import utils
from  .. import reactions


class EditModalsBuilder(nextcord.ui.Modal):
    def __init__(self,channel_id) -> None:
        self.channel_id = channel_id
        super().__init__('Авто-сообщение')
        
        self.emo = nextcord.ui.TextInput(
            label='Эмодзи:',
            placeholder='<[a]:name:id>'
        )
        
        self.add_item(self.emo)
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        reacts  = gdb.get('reactions',{})
        content = self.emo.value
        channel_id = self.channel_id
        
        reacts[channel_id] = []
        reacts[channel_id].append(content)
        
        gdb.set('reactions',reacts)
        
        view = reactions.AutoReactions(interaction.guild)
        await interaction.message.edit(**view.content,view=view)


class ReactData(nextcord.ui.View):
    def __init__(self,channel,channel_data) -> None:
        self.gdb = GuildDateBases(channel.guild.id)
        self.forum_message  = self.gdb.get('reactions',{})
        
        self.channel_data = channel_data
        self.channel = channel
        super().__init__()
    
    
    @nextcord.ui.button(label='Назад',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = reactions.AutoReactions(interaction.guild)
        await interaction.message.edit(**view.content,view=view)
    
    @nextcord.ui.button(label='Изменить реакции',style=nextcord.ButtonStyle.primary,row=2)
    async def edit_message(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(EditModalsBuilder(self.channel.id))
    
    @nextcord.ui.button(label='Удалить авто-реакции',style=nextcord.ButtonStyle.red,row=2)
    async def delete_message(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        channel_id = self.channel.id
        del self.forum_message[channel_id]
        
        self.gdb.set('reactions',self.forum_message)
        
        
        view = reactions.AutoReactions(interaction.guild)
        await interaction.message.edit(**view.content,view=view)
