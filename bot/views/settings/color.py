import nextcord
from bot.databases.db import GuildDateBases
import re
from bot.views import views
from ..settings import DefaultSettingsView


class Modal(nextcord.ui.Modal):
    def __init__(self, guild_id) -> None:
        self.gdb = GuildDateBases(guild_id)
        
        colour = self.gdb.get('color',1974050)
        colour = hex(colour).replace('0x', '#')
        
        super().__init__("Rewards", timeout=300)
        
        self.color = nextcord.ui.TextInput(
            label='Color',
            placeholder=colour
        )
        
        self.add_item(self.color)
    
    async def callback(self, interaction: nextcord.Interaction) :
        color = self.color.value
        match = re.search(r'#([0-9a-fA-F]{6})', color)
        if not match:
            await interaction.response.send_message('Hex is not valid',ephemeral=True)
            return
        
        colour = int(color[1:], 16)
        self.gdb.set('color',colour)
        
        embed = nextcord.Embed(title=f'A new system color is installed - {color}',color=colour)
        
        await interaction.response.send_message(embed=embed,ephemeral=True)

class ColorView(DefaultSettingsView):
    embed = None
    
    def __init__(self, guild_id) -> None:
        super().__init__()
        
    
    
    @nextcord.ui.button(label='Назад',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.edit(embed=None,view=views.SettingsView(interaction.user))
    