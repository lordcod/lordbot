from typing import Optional
import nextcord
from bot.databases.db import GuildDateBases
from ..settings import DefaultSettingsView
from bot.views import views
from bot.resources.info import DEFAULT_PREFIX
from bot.misc.utils import get_prefix


class Modal(nextcord.ui.Modal):
    type = 'modal'
    
    def __init__(self,guild_id) -> None:
        prefix = get_prefix(guild_id,markdown=True)
        
        super().__init__(title='Префикс')
        
        self.prefix = nextcord.ui.TextInput(
            label='Префикс:',
            placeholder=prefix,
            max_length=7
        )
        self.add_item(self.prefix)
    
    async def callback(self, interaction: nextcord.Interaction):
        prefix = self.prefix.value
        gdb = GuildDateBases(interaction.guild_id)
        gdb.set('prefix',prefix)
        
        await interaction.response.send_message(f'New prefix - `{prefix}`',ephemeral=True)

class PrefixView(DefaultSettingsView):
    embed = nextcord.Embed(
        title='Префикс',
        description='Установка префикса, на который бот будет реагировать при вызове команды.'
    )
    
    def __init__(self,guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        colour = gdb.get('color',1974050)
        prefix = get_prefix(guild.id,markdown=False)
        
        self.embed.color = colour
        self.embed._fields = [{'name':f'Текущий префикс: `{prefix}`','value':''}]
        
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
        gdb = GuildDateBases(interaction.guild_id)
        prefix = DEFAULT_PREFIX
        
        gdb.set('prefix',prefix)
        await interaction.response.send_message(f'Reset Prefix\nDefault prefix - `{prefix}`',ephemeral=True)