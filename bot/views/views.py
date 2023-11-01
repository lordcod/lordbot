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

class DropDown_MusicSelect(nextcord.ui.StringSelect):
    def __init__(self,tracks: List[Track],callback):
        options = [
            nextcord.SelectOption(
                label=track.title, description=', '.join(track.artist_names),value=track.id
            )
            for track in tracks
        ]
        super().__init__(
            custom_id='dropdown_customid',
            placeholder="Выбери музыку:",
            min_values=1,
            max_values=1,
            options=options,
        )
        self.callback_to = callback
    
    async def callback(self, interaction: nextcord.Interaction):
        await self.callback_to(interaction,self.values[0])