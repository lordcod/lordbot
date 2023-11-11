import nextcord
from .bonuses import Bonus
from bot.resources.languages import Emoji

class DropDown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(
                label='Bonus',emoji=Emoji.bagmoney
            )
        ]

        super().__init__(
            placeholder="Настройки экономики:",
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        lists = {
            'Bonus':Bonus(interaction.guild_id)
        }
        view = lists[value]
        if view.type == 'modal':
            await interaction.response.send_modal(view)
        if view.type == 'view':
            await interaction.response.send_message(**view.content,view=view,ephemeral=True)

class Economy(nextcord.ui.View):
    type = 'view'
    content = {
        'embed':nextcord.Embed(title='Система экономики')
    }
    
    def __init__(self,) -> None:
        super().__init__()
        
        self._lang = DropDown()
        
        self.add_item(self._lang)
