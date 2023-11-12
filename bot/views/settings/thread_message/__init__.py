import nextcord
from bot.databases.db import GuildDateBases
from bot.resources.languages import channel_type
from .addptional import ViewBuilder
from .thread import ThreadData

class DropDown(nextcord.ui.Select):
    def __init__(self,guild):
        self.gdb = GuildDateBases(guild.id)
        self.forum_message = forum_message  = self.gdb.get('thread_messages',{})
        channels = [guild.get_channel(key)  for key in forum_message]
        
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
            options=options,
        )
        
        if len(self.options) <= 0:
            self.disabled = True
            self.add_option(label='Нет настроек в данном модуле!')
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        value = int(value)
        
        channel = await interaction.guild.fetch_channel(value)
        channel_data = self.forum_message.get(value,{})
        
        embed = nextcord.Embed(
            title="Авто-сообщения",
            description=f"Канал: {channel.mention}"
        )
        
        await interaction.response.send_message(embed=embed,view=ThreadData(channel,channel_data),ephemeral=True)

class AutoThreadMessage(nextcord.ui.View):
    type = 'view'
    content = {}
    
    def __init__(self,guild_id) -> None:
        super().__init__()
        
        self.auto = DropDown(guild_id)
        
        self.add_item(self.auto)
    
    @nextcord.ui.button(label='Добавить',style=nextcord.ButtonStyle.green)
    async def addtion(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(view=ViewBuilder(),ephemeral=True)