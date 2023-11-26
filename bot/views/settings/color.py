import nextcord
from bot.databases.db import GuildDateBases
import re
from bot.views import views
from ..settings import DefaultSettingsView
from bot.resources.info import DEFAULT_COLOR
from bot.misc.utils import to_color,from_color
from bot.languages.settings import (
    color as color_langs,
    button as button_name
)


class Modal(nextcord.ui.Modal):
    def __init__(self, guild_id) -> None:
        self.gdb = GuildDateBases(guild_id)
        
        colour = self.gdb.get('color',1974050)
        color = to_color(colour)
        
        super().__init__("Rewards", timeout=300)
        
        self.color = nextcord.ui.TextInput(
            label='Color',
            placeholder=color
        )
        
        self.add_item(self.color)
    
    async def callback(self, interaction: nextcord.Interaction) :
        color = self.color.value
        match = re.search(r'#([0-9a-fA-F]{6})', color)
        if not match:
            await interaction.response.send_message('Hex is not valid',ephemeral=True)
            return
        
        colour = from_color(color)
        self.gdb.set('color',colour)
        
        view = ColorView(interaction.guild)
        
        await interaction.message.edit(embed=view.embed,view=view)

class ColorView(DefaultSettingsView):
    embed: nextcord.Embed
    
    def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        locale = gdb.get('language')
        colour = gdb.get('color')
        color = to_color(colour)
        
        self.embed = nextcord.Embed(
            title=color_langs.title.get(locale),
            description=color_langs.description.get(locale),
            color = colour
        )
        self.embed._fields = [{'name':f'{color_langs.current.get(locale)}: `{color}`','value':''}]
        
        super().__init__()
        
        self.back.label = button_name.back.get(locale)
        self.edit.label = button_name.edit.get(locale)
        self.reset.label = button_name.reset.get(locale)
    
    
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = views.SettingsView(interaction.user)
        
        await interaction.message.edit(embed=view.embed,view=view)
    
    
    @nextcord.ui.button(label='Edit',style=nextcord.ButtonStyle.blurple)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = Modal(interaction.guild_id)
        
        await interaction.response.send_modal(modal)
    
    
    @nextcord.ui.button(label='Reset',style=nextcord.ButtonStyle.success)
    async def reset(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb =GuildDateBases(interaction.guild_id)
        colour = DEFAULT_COLOR
        gdb.set('color',colour)
        
        view = ColorView(interaction.guild)
        
        await interaction.message.edit(embed=view.embed,view=view)