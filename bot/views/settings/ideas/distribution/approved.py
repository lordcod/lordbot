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

from typing import Optional


class DropDown(nextcord.ui.ChannelSelect):
    def __init__(
        self, 
        guild_id: int
    ) -> None:
        gdb = GuildDateBases(guild_id)
        self.idea_data = gdb.get('ideas')
        
        super().__init__(channel_types=[nextcord.ChannelType.text])
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel = self.values[0]
        
        view = ApprovedView(interaction.guild, channel)
        
        await interaction.message.edit(embed=view.embed, view=view)


class ApprovedView(DefaultSettingsView):
    embed: nextcord.Embed = None
    
    def __init__(self, guild: nextcord.Guild, channel: Optional[nextcord.TextChannel] = None) -> None:
        gdb = GuildDateBases(guild.id)
        colour = gdb.get('color')
        
        super().__init__()
        
        self.channel = channel
        self.embed = None
        
        
        cdd = DropDown(
            guild.id
        )
        self.add_item(cdd)
    
    
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = ideas.IdeasView(interaction.guild)
        
        await interaction.message.edit(embed=view.embed, view=view)
    
    
    @nextcord.ui.button(label='Edit', style=nextcord.ButtonStyle.blurple)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):    
        pass
    
    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass