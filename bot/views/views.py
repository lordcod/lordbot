import nextcord
from bot.views import menus
from bot.misc.yandex_api import Track
from typing import List

class CustomList(menus.Main):
    dem = nextcord.Embed(title='Описание',description='Нашего персонала')
    
    async def callback(self,button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gem = self.dem
        gem._fields = [self.value[self.index]]
        await interaction.message.edit(embed=gem,view=self)
