from typing import Optional
import nextcord
from bot.databases.db import GuildDateBases
from  .. import reactions
from ...settings import DefaultSettingsView

class ModalsBuilder(nextcord.ui.Modal):
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
        
        if channel_id in reacts:
            await interaction.response.send_message("На этот канал уже установлено авто-сообщения")
            return
        
        reacts[channel_id] = []
        reacts[channel_id].append(content)
        
        gdb.set('reactions',reacts)
        
        view = reactions.AutoReactions(interaction.guild)
        await interaction.message.edit(embed=view.embed,view=view)

class DropDownBuilder(nextcord.ui.ChannelSelect):
    def __init__(self) -> None:
        super().__init__(
            placeholder='Выберете канал для авто-реакций'
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
        view = reactions.AutoReactions(interaction.guild)
        
        await interaction.message.edit(embed=view.embed,view=view)