import nextcord

from .additional import ViewBuilder
from .precise import ReactData
from ...settings import DefaultSettingsView

from bot.misc import utils
from bot.views import views
from bot.databases.db import GuildDateBases
from bot.resources.ether import Channel_Type
from bot.languages.settings import (
    reactions as reaction_langs,
    button as button_name
)


class DropDown(nextcord.ui.Select):
    is_option = False
    
    def __init__(self,guild: nextcord.Guild):
        self.gdb = GuildDateBases(guild.id)
        locale = self.gdb.get('language')
        self.reactions = self.gdb.get('reactions',{})
        channels = [guild.get_channel(key)  for key in self.reactions]
        utils.remove_none(channels)
        
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
            placeholder=reaction_langs.init.ph.get(locale),
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        colour = gdb.get('color')
        locale = gdb.get('language')
        
        value = self.values[0]
        value = int(value)
        
        channel = await interaction.guild.fetch_channel(value)
        channel_data = self.reactions.get(value)
        
        embed = nextcord.Embed(
            title=reaction_langs.init.brief_title.get(locale),
            description=(
                f"{reaction_langs.init.channel.get(locale)}: {channel.mention}\n"
                f"{reaction_langs.init.emoji.get(locale)}: {', '.join([emo for emo in channel_data])}"
            ),
            color=colour
        )
        
        await interaction.message.edit(embed=embed,view=ReactData(channel,channel_data))

class AutoReactions(DefaultSettingsView):
    embed: nextcord.Embed
    
    def __init__(self,guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        colour = gdb.get('color')
        locale = gdb.get('language')
        
        self.embed = nextcord.Embed(
            title=reaction_langs.init.title.get(locale),
            description=reaction_langs.init.description.get(locale),
            color = colour
        )
        
        super().__init__()
        
        self.back.label = button_name.back.get(locale)
        self.addtion.label = button_name.add.get(locale)
        
        auto = DropDown(guild)
        
        if not auto.is_option:
            self.add_item(auto)
    
    
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = views.SettingsView(interaction.user)
        
        await interaction.message.edit(embed=view.embed,view=view)
    
    @nextcord.ui.button(label='Add',style=nextcord.ButtonStyle.green)
    async def addtion(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = ViewBuilder(interaction.guild_id)
        
        await interaction.message.edit(embed=None,view=view)
