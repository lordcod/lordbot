import nextcord

from ..greeting import Greeting
from ...settings import DefaultSettingsView

from bot.resources.ether import Emoji
from bot.views import views
from bot.databases.db import GuildDateBases
from bot.languages.settings import (
    button as button_name
)



class DropDownBuilder(nextcord.ui.ChannelSelect):
    def __init__(self,guild_id) -> None:
        pass
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        pass

class ViewBuilder(DefaultSettingsView):
    embed: nextcord.Embed
    
    def __init__(self,guild: int, installer = None) -> None:
        super().__init__()
        
        
    
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = Greeting(interaction.guild)
        
        await interaction.message.edit(embed=view.embed, view=view)
    
    @nextcord.ui.button(label='Install message',style=nextcord.ButtonStyle.blurple,disabled=True)
    async def install(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass