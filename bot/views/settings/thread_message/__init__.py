import nextcord

from .additional import ViewBuilder
from .precise import ThreadData
from ...settings import DefaultSettingsView

from bot.views import views
from bot.databases.db import GuildDateBases
from bot.resources.ether import Channel_Type
from bot.languages.settings import (
    thread as thread_langs,
    button as button_name
)

class DropDown(nextcord.ui.Select):
    is_option = False
    
    def __init__(self,guild: nextcord.Guild):
        self.gdb = GuildDateBases(guild.id)
        locale = self.gdb.get('language')
        self.forum_message = self.gdb.get('thread_messages',{})
        channels = [guild.get_channel(key) for key in self.forum_message]
        
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
            placeholder=thread_langs.init.pc.get(locale),
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        value = int(value)
        channel = await interaction.guild.fetch_channel(value)
        channel_data = self.forum_message.get(value)
        locale = self.gdb.get('language')
        colour = self.gdb.get('color')
        
        
        embed = nextcord.Embed(
            title=thread_langs.init.brief_title.get(locale),
            description=f"{thread_langs.init.channel.get(locale)}: {channel.mention}",
            color=colour
        )
        await interaction.message.edit(embed=embed,view=ThreadData(channel,channel_data))

class AutoThreadMessage(DefaultSettingsView):
    embed: nextcord.Embed
    
    
    def __init__(self,guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        locale = gdb.get('language')
        colour = gdb.get('color')
        
        self.embed = nextcord.Embed(
            title=thread_langs.init.title.get(locale),
            description=thread_langs.init.description.get(locale),
            color = colour
        )
        
        super().__init__()
        
        self.back.label = button_name.back.get(locale)
        self.addtion.label = button_name.add.get(locale)
        
        self.auto = DropDown(guild)
        
        if not self.auto.is_option:
            self.add_item(self.auto)
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = views.SettingsView(interaction.user)
        
        await interaction.message.edit(embed=view.embed,view=view)
    
    @nextcord.ui.button(label='Add',style=nextcord.ButtonStyle.green)
    async def addtion(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = ViewBuilder(interaction.guild_id)
        
        await interaction.message.edit(embed=None,view=view)