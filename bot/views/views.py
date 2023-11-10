import nextcord
from nextcord.interactions import Interaction
from nextcord.utils import MISSING
from bot.misc.utils import clord
from bot.views import menus
from bot.databases.db import GuildDateBases
from bot.misc.yandex_api import Track
from typing import Any, Coroutine, List, Optional

class CustomList(menus.Main):
    dem = nextcord.Embed(title='Описание',description='Нашего персонала')
    
    async def callback(self,button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gem = self.dem
        gem._fields = [self.value[self.index]]
        await interaction.message.edit(embed=gem,view=self)


class Settings(nextcord.ui.Modal):
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
    
    
    async def callback(self, interaction: Interaction) -> Coroutine[Any, Any, None]:
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
        
        print(economy_settings)
        gdb.set('economic_settings',economy_settings)
        print(gdb.get('economic_settings',{}))