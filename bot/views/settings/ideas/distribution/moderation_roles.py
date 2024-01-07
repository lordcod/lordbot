import nextcord

from  ... import ideas
from ... import DefaultSettingsView

from bot.misc import utils
from bot.misc.ratelimit import BucketType
from bot.resources.ether import Emoji
from bot.databases.db import GuildDateBases, CommandDB
from bot.languages.settings import (
    button as button_name
)



class DropDown(nextcord.ui.StringSelect):
    current_disabled = False
    
    def __init__(
        self, 
        guild_id: int,
        value = None
    ) -> None:
        self.value = value
        
        options = []
        
        super().__init__(
            options=options
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        
        view = ModerationRolesView(interaction.guild)
        
        await interaction.message.edit(embed=view.embed, view=view)


class ModerationRolesView(DefaultSettingsView):
    embed: nextcord.Embed = None
    
    def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        colour = gdb.get('color')
        
        super().__init__()
        
        
        self.embed = None
        
        
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