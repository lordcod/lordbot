import nextcord

from  ... import ideas
from ... import DefaultSettingsView

from bot.misc import utils
from bot.resources.ether import Emoji
from bot.databases.db import GuildDateBases
from bot.languages.settings import (
    button as button_name
)




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
            if (
                role.is_default() or
                role.is_premium_subscriber() or
                role.is_integration() or
                role.is_bot_managed()
            ):
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
        pass




class ModerationRolesView(DefaultSettingsView):
    embed: nextcord.Embed = None
    
    def __init__(self, guild: nextcord.Guild, role_ids: list[int] = None) -> None:
        gdb = GuildDateBases(guild.id)
        colour = gdb.get('color')
        
        super().__init__()
        
        
        self.embed = nextcord.Embed()
        
        
        cdd = DropDown(
            guild.id
        )
        self.add_item(cdd)
    
    
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = ideas.IdeasView(interaction.guild)
        
        await interaction.message.edit(embed=view.embed, view=view)
    
    
    @nextcord.ui.button(label='Edit',style=nextcord.ButtonStyle.blurple)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):    
        pass
    
    @nextcord.ui.button(label='Delete',style=nextcord.ButtonStyle.red)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass