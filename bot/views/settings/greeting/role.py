import nextcord

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
    def __init__(self,guild_id: int, installer = None) -> None:
        pass
    
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass
    
    @nextcord.ui.button(label='Install roles',style=nextcord.ButtonStyle.blurple,disabled=True)
    async def install(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass