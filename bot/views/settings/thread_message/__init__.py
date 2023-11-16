import nextcord
from bot.databases.db import GuildDateBases
from bot.resources.languages import channel_type
from .addptional import ViewBuilder
from bot.views import views
from .thread import ThreadData
from ...settings import DefaultSettingsView

class DropDown(nextcord.ui.Select):
    is_option = False
    
    def __init__(self,guild):
        self.gdb = GuildDateBases(guild.id)
        self.forum_message = forum_message  = self.gdb.get('thread_messages',{})
        channels = [guild.get_channel(key) for key in forum_message]
        
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
            placeholder="Настройки авто-сообщений в ветках, форумах:",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        value = int(value)
        channel = await interaction.guild.fetch_channel(value)
        channel_data = self.forum_message.get(value,{})
        colour = self.gdb.get('color',1974050)
        
        
        embed = nextcord.Embed(
            title="Авто-сообщения",
            description=f"Канал: {channel.mention}",
            color=colour
        )
        await interaction.message.edit(embed=embed,view=ThreadData(channel,channel_data))

class AutoThreadMessage(DefaultSettingsView):
    embed = nextcord.Embed(
        title='Автоматические сообщения в форумах/ветках',
        description='Добавляйте или изменяйте свои автоматические сообщения в форумах/ветках'
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