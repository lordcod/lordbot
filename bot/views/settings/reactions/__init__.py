import nextcord
from bot.databases.db import GuildDateBases
from bot.resources.ether import Channel_Type
from .addres import ViewBuilder
from .datas import ReactData
from bot.views import views
from ...settings import DefaultSettingsView


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
                emoji=Channel_Type[chnl.type.value],
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
        gdb = GuildDateBases(interaction.guild_id)
        colour = gdb.get('color',1974050)
        
        value = self.values[0]
        value = int(value)
        
        channel = await interaction.guild.fetch_channel(value)
        channel_data = self.reactions.get(value,[])
        
        embed = nextcord.Embed(
            title="Авто-сообщения",
            description=(
                f"Канал: {channel.mention}\n"
                f"Эмодзи: {', '.join([emo for emo in channel_data])}"
            ),
            color=colour
        )
        
        await interaction.message.edit(embed=embed,view=ReactData(channel,channel_data))

class AutoReactions(DefaultSettingsView):
    embed = nextcord.Embed(
        title='Автоматические реакции',
        description='Управление автоматическим добавлением реакций в каналах'
    )
    
    def __init__(self,guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        colour = gdb.get('color',1974050)
        self.embed.color = colour
        
        super().__init__()
        
        self.auto = DropDown(guild)
        
        if not self.auto.is_option:
            self.add_item(self.auto)
    
    
    @nextcord.ui.button(label='Назад',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = views.SettingsView(interaction.user)
        
        await interaction.message.edit(embed=view.embed,view=view)
    
    @nextcord.ui.button(label='Добавить',style=nextcord.ButtonStyle.green)
    async def addtion(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.edit(embed=None,view=ViewBuilder())
