import nextcord

from  ... import permisson_command
from ... import DefaultSettingsView

from bot.misc import utils
from bot.resources.ether import Emoji
from bot.databases.db import GuildDateBases, CommandDB
from bot.languages import help as help_info
from bot.languages.settings import (
    button as button_name
)

from typing import List

class DropDown(nextcord.ui.StringSelect):
    current_disabled = False
    
    def __init__(
        self, 
        guild: nextcord.Guild,
        command_name: str,
        roles: list[nextcord.Role]
    ) -> None:
        self.command_name = command_name
        options = []
        
        for role in guild.roles:
            interdict = [
                role.is_default(),
                role.is_premium_subscriber(),
                role.is_integration(),
                role.is_bot_managed()
            ]
            if True in interdict:
                continue
            
            opt = nextcord.SelectOption(
                label=role.name,
                value=role.id,
                emoji=Emoji.frame_person,
                default=role in roles
            )
            
            options.append(opt)
        
        options = options[:25]
        if 0 >= len(options):
            options.append(
                nextcord.SelectOption(
                    label="-"
                )
            )
            self.current_disabled = True
        
        super().__init__(
            placeholder="Select the roles in which the command will work",
            min_values=1,
            max_values=len(options),
            options=options,
            disabled=self.current_disabled
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        values = self.values
        role_ids = [int(val) for val in values]
        
        cdb = CommandDB(interaction.guild_id)
        
        command_data = cdb.get(self.command_name, {})
        if "distribution" not in command_data:
            command_data["distribution"] = {}
        
        command_data["distribution"]["role"] = {
            "permission":1,
            "values":role_ids
        }
        
        cdb.update(self.command_name, command_data)
        
        
        view = RolesView(
            interaction.guild,
            self.command_name
        )
        
        await interaction.message.edit(embed=view.embed, view=view)


class RolesView(DefaultSettingsView):
    embed: nextcord.Embed = None
    
    def __init__(self, guild: nextcord.Guild, command_name: str) -> None:
        self.command_name = command_name
        
        gdb = GuildDateBases(guild.id)
        colour = gdb.get('color')
        
        cdb = CommandDB(guild.id)
        command_data = cdb.get(command_name, {})
        distribution = command_data.get("distribution", {})
        role_perms = distribution.get("role", None)
        
        role_ids = []
        roles = []
        
        self.embed = nextcord.Embed(
            title="Allowed roles",
            description="The selected command will only work in the roles that you select",
            color=colour
        )
        
        if role_perms:
            role_ids = role_perms.get('values')
            roles = [guild.get_role(id) for id in role_ids]
        
        super().__init__()
        
        cdd = DropDown(
            guild,
            command_name,
            roles
        )
        self.add_item(cdd)
    
    
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = permisson_command.precise.CommandData(
            interaction.guild,
            self.command_name
        )
        
        await interaction.message.edit(embed=view.embed, view=view)
