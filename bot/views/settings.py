from typing import Optional
import nextcord

from bot.misc.utils import clord
from bot.databases.db import GuildDateBases
from bot.resources.languages import Languages_self as AllLangs

class Prefix(nextcord.ui.Modal):
    types = 'modal'
    
    def __init__(self) -> None:
        super().__init__(title='Префикс')
        
        self.prefix = nextcord.ui.TextInput(
            label='Префикс:',
            placeholder='l.',
            max_length=3
        )
        self.add_item(self.prefix)
    
    async def callback(self, interaction: nextcord.Interaction):
        prefix = self.prefix.value
        await interaction.response.send_message(f'New prefix - `{prefix}`',ephemeral=True)

class Economy(nextcord.ui.Modal):
    types = 'modal'
    
    def __init__(self) -> None:
        super().__init__("Rewards", timeout=300)
        
        self.daily = nextcord.ui.TextInput(
            label='Daily',
            placeholder='Enter the value for the daily reward',
            required=False,
            max_length=5
        )
        self.weekly = nextcord.ui.TextInput(
            label='Daily',
            placeholder='Enter the value for the weekly reward',
            required=False,
            max_length=5
        )
        self.monthly = nextcord.ui.TextInput(
            label='Daily',
            placeholder='Enter the value for the monthly reward',
            required=False,
            max_length=5
        )
        
        self.add_item(self.daily)
        self.add_item(self.weekly)
        self.add_item(self.monthly)
    
    async def callback(self, interaction: nextcord.Interaction) :
        daily = clord(self.daily.value,int)
        weekly = clord(self.weekly.value,int)
        monthly = clord(self.monthly.value,int)
        
        gdb = GuildDateBases(interaction.guild_id)
        economy_settings = gdb.get('economic_settings',{})
        
        if daily:
            economy_settings['daily'] = daily
        if weekly:
            economy_settings['weekly'] = weekly
        if monthly:
            economy_settings['monthly'] = monthly
        
        gdb.set('economic_settings',economy_settings)

class Color(nextcord.ui.Modal):
    types = 'modal'
    
    def __init__(self) -> None:
        super().__init__("Rewards", timeout=300)
        
        self.color = nextcord.ui.TextInput(
            label='Color',
            placeholder='#2596be'
        )
        
        self.add_item(self.color)
    
    async def callback(self, interaction: nextcord.Interaction) :
        color = self.color.value
        
        await interaction.response.send_message(color,ephemeral=True)



class _languages(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(
                label=data.get('native_name'), value=data.get('discord_language'), emoji=data.get('flag',None)
            )
            for data in AllLangs[:24]
        ]

        super().__init__(
            placeholder="Выберите язык для сервера:",
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        await interaction.response.send_message(f'Selected language: {value}',ephemeral=True)

class Languages(nextcord.ui.View):
    types = 'view'
    def __init__(self,) -> None:
        super().__init__()
        
        self._lang = _languages()
        
        self.add_item(self._lang)
