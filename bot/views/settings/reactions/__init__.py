import nextcord
from bot.databases.db import GuildDateBases
from bot.resources.languages import channel_type
from .addres import ViewBuilder
from .datas import ReactData
from bot.views import views


class DropDown(nextcord.ui.Select):
    is_option = False
    
    def __init__(self,guild):
        self.gdb = GuildDateBases(guild.id)
        self.reactions = self.gdb.get('reactions',{})
        channels = [guild.get_channel(key)  for key in self.reactions]
        
        if len(channels) <= 0:
            self.is_option = True
            return
        options = [
            nextcord.SelectOption(
                label=chnl.name,
                emoji=channel_type[chnl.type.value],
                value=chnl.id
            )
            for chnl in channels
        ]
    
        super().__init__(
            placeholder="Настройки авто-реакций:",
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        value = int(value)
        
        channel = await interaction.guild.fetch_channel(value)
        channel_data = self.reactions.get(value,[])
        
        embed = nextcord.Embed(
            title="Авто-сообщения",
            description=(
                f"Канал: {channel.mention}\n"
                f"Эмодзи: {', '.join([emo for emo in channel_data])}"
            )
        )
        
        await interaction.message.edit(embed=embed,view=ReactData(channel,channel_data))

class AutoReactions(nextcord.ui.View):
    type = 'view'
    content = {}
    
    def __init__(self,guild) -> None:
        super().__init__()
        
        self.auto = DropDown(guild)
        
        if not self.auto.is_option:
            self.add_item(self.auto)
    
    
    @nextcord.ui.button(label='Назад',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.edit(embed=None,view=views.SettingsView())
    
    @nextcord.ui.button(label='Добавить',style=nextcord.ButtonStyle.green)
    async def addtion(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.edit(embed=None,view=ViewBuilder())
