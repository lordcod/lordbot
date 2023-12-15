import nextcord

from  .. import permisson_command
from ...settings import DefaultSettingsView

from bot.misc import utils
from bot.resources.ether import Emoji
from bot.databases.db import GuildDateBases, CommandDB
from bot.languages.settings import (
    button as button_name
)

from bot.languages import help as help_info
import jmespath

def get_command(name: str) -> help_info.CommandOption: 
    expression = f"[?name == '{name}']|[0]"
    result = jmespath.search(expression,help_info.commands)
    return result

class DropDown(nextcord.ui.StringSelect):
    def __init__(self, guild_id) -> None:
        options = [
            nextcord.SelectOption(
                label='Channel', emoji=Emoji.channel_text, value='channel'
            ),
            nextcord.SelectOption(
                label='Role', emoji=Emoji.auto_role, value='role'
            ),
        ]
        
        
        super().__init__(options=options)
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        pass


class CommandData(DefaultSettingsView):
    embed: nextcord.Embed = None
    
    def __init__(self, guild:nextcord.Guild, command_name: str) -> None:
        self.command_name = command_name
        self.cdb = CommandDB(guild.id)
        self.gdb = GuildDateBases(guild.id)
        
        super().__init__()
        
        DDD = DropDown(guild.id)
        self.add_item(DDD)
        
        locale:str = self.gdb.get('language')
        
        self.command_data: dict = get_command(command_name)
        self.command_info: dict = self.cdb.get(command_name,{})
        
        self.operate = self.command_info.get("operate",1)
        if self.operate == 1:
            self.switcher.label = "Disable"
            self.switcher.style = nextcord.ButtonStyle.red
        else:
            self.switcher.label = "Enable"
            self.switcher.style = nextcord.ButtonStyle.green
        
        
        self.back.label = button_name.back.get(locale)
    
    
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = permisson_command.CommandsDataView(interaction.guild)
        
        await interaction.message.edit(embed=view.embed,view=view)
    
    @nextcord.ui.button(label='Switcher')
    async def switcher(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        command_info = self.command_info
        desperate = 0 if self.operate == 1 else 1
        
        command_info['operate'] = desperate
        
        self.cdb.update(self.command_name, command_info)
        
        
        view = self.__class__(interaction.guild, self.command_name)
        
        await interaction.message.edit(embed=view.embed, view=view)

