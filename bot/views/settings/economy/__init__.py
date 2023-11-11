import nextcord
from .bonuses import Bonus
from bot.resources.languages import Emoji
from bot.databases.db import GuildDateBases

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
    
    def __init__(self,guild_id) -> None:
        self.gdb = GuildDateBases(guild_id)
        self.es = self.gdb.get('economic_settings',{})
        operate = self.es.get('operate',False)
        
        super().__init__()
        
        self._lang = DropDown()
        
        self.add_item(self._lang)
        
        
        if operate:
            self.economy_Off.disabled = False
        else:
            self.economy_On.disabled = False
    
    @nextcord.ui.button(label='Включить',style=nextcord.ButtonStyle.green,disabled=True)
    async def economy_On(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        es = self.es
        es['operate'] = True
        self.gdb.set('economic_settings',es)
    
    @nextcord.ui.button(label='Выключить',style=nextcord.ButtonStyle.red,disabled=True)
    async def economy_Off(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        es = self.es
        es['operate'] = False
        self.gdb.set('economic_settings',es)
