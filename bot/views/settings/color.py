import nextcord
from bot.databases.db import GuildDateBases
import re
from bot.views import views
from ..settings import DefaultSettingsView
from bot.resources.info import DEFAULT_COLOR
from bot.misc.utils import to_color,from_color


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
        
        embed = nextcord.Embed(title=f'A new system color is installed - {color}',color=colour)
        
        await interaction.response.send_message(embed=embed,ephemeral=True)

class ColorView(DefaultSettingsView):
    embed = nextcord.Embed(
        title='Цвет системных сообщений',
        description=(
            'Когда вы используете команды, бот отображает вставки, которые по умолчанию имеют невидимый цвет.\n\n'
            'Вы можете установить свой цвет в соответствии с тематикой вашего сообщества.'
        )
    )
    
    def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        colour = gdb.get('color',1974050)
        color = to_color(colour)
        
        self.embed.color = colour
        self.embed._fields = [{'name':f'Текущий цвет: `{color}`','value':''}]
        
        super().__init__()
    
    
    
    @nextcord.ui.button(label='Назад',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = views.SettingsView(interaction.user)
        
        await interaction.message.edit(embed=view.embed,view=view)
    
    
    @nextcord.ui.button(label='Изменить',style=nextcord.ButtonStyle.blurple)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = Modal(interaction.guild_id)
        
        await interaction.response.send_modal(modal)
    
    
    @nextcord.ui.button(label='Сбросить',style=nextcord.ButtonStyle.success)
    async def reset(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb =GuildDateBases(interaction.guild_id)
        
        colour = DEFAULT_COLOR
        color = to_color(colour)
        
        gdb.set('color',colour)
        
        embed = nextcord.Embed(title=f'Reset color\nDefault system color - **{color}**',color=colour)
        
        await interaction.response.send_message(embed=embed,ephemeral=True)