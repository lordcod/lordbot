import nextcord

from  ... import permisson_command
from ... import DefaultSettingsView

from bot.misc import utils
from bot.misc.ratelimit import BucketType
from bot.resources.ether import Emoji
from bot.databases.db import GuildDateBases, CommandDB
from bot.languages import help as help_info
from bot.languages.settings import (
    button as button_name
)

from typing import List, Optional

cd_types = {
    0:'Delay for a specific user',
    1:'Server latency(global)'
}



class CoolModal(nextcord.ui.Modal):
    def __init__(
        self,
        type,
        command_name
    ) -> None:
        self.type = type
        self.command_name = command_name
        
        super().__init__("Cooldown")
        
        self.rate = nextcord.ui.TextInput(
            label="Rate",
            min_length=1,
            max_length=4
        )
        self.per = nextcord.ui.TextInput(
            label="Per",
            placeholder="1h10m",
            min_length=1,
            max_length=10
        )
        
        self.add_item(self.rate)
        self.add_item(self.per)
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        srate = self.rate.value
        per = utils.calculate_time(self.per.value)
        rate = srate.isdigit() and int(srate)
        
        if not (per and rate):
            await interaction.response.send_message("Error #1", ephemeral=True)
            return
        
        
        cdb = CommandDB(interaction.guild.id)
        command_data = cdb.get(self.command_name, {})
        if "distribution" not in command_data:
            command_data["distribution"] = {}
        
        command_data["distribution"]["cooldown"] = {
            "type": self.type,
            "rate":rate,
            "per":per
        }
        
        cdb.update(self.command_name, command_data)
        
        
        view = CooldownsView(
            interaction.guild,
            self.command_name
        )
        
        await interaction.message.edit(embed=view.embed, view=view)


class DropDown(nextcord.ui.StringSelect):
    current_disabled = False
    
    def __init__(
        self, 
        guild_id: int,
        command_name: str
    ) -> None:
        self.command_name = command_name
        
        options = [
            nextcord.SelectOption(
                label="Member", 
                value=BucketType.member
            ),
            nextcord.SelectOption(
                label="Server", 
                value=BucketType.server
            )
        ]
        
        super().__init__(
            options=options
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        typ = int(self.values[0])
        
        modal = CoolModal(typ, self.command_name)
        
        await interaction.response.send_modal(modal)


class CooldownsView(DefaultSettingsView):
    embed: nextcord.Embed = None
    
    def __init__(self, guild: nextcord.Guild, command_name: str) -> None:
        self.command_name = command_name
        
        gdb = GuildDateBases(guild.id)
        colour = gdb.get('color')
        
        cdb = CommandDB(guild.id)
        command_data = cdb.get(command_name, {})
        distribution = command_data.get("distribution", {})
        cooldate = distribution.get("cooldown", None)
        
        if isinstance(cooldate, dict):
            description = (
                "The current delay for the command\n"
                f"Type: {cd_types.get(cooldate.get('type'))}\n"
                f"{cooldate.get('rate')} → {cooldate.get('per')}\n"
            )
        else:
            description = "The delay is not set"
        
        self.embed = nextcord.Embed(
            title=f"Command: {command_name}",
            description=description,
            color=colour
        )  
        
        super().__init__()
        
        cdd = DropDown(
            guild.id,
            command_name
        )
        self.add_item(cdd)
    
    
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = permisson_command.precise.CommandData(
            interaction.guild,
            self.command_name
        )
        
        await interaction.message.edit(embed=view.embed, view=view)
