import nextcord
from nextcord.interactions import Interaction
from nextcord.utils import MISSING
from bot.misc.utils import clord,alphabet
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

