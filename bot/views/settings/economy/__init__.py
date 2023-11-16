import nextcord
from .bonuses import Bonus
from bot.resources.languages import Emoji
from bot.databases.db import GuildDateBases
from bot.views import views
from ...settings import DefaultSettingsView

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
            'Bonus':Bonus
        }
        view = lists[value](interaction.guild)
        await interaction.message.edit(embed=view.embed,view=view)

class Economy(DefaultSettingsView):
    embed = nextcord.Embed(title='Система экономики')
    
    def __init__(self,guild: nextcord.Guild) -> None:
        self.gdb = GuildDateBases(guild.id)
        self.es = self.gdb.get('economic_settings',{})
        operate = self.es.get('operate',False)
        colour = self.gdb.get('color',1974050)
        
        self.embed.color = colour
        
        super().__init__()
        
        self.economy = DropDown()
        
        self.add_item(self.economy)
        
        
        if operate:
            self.remove_item(self.economy_On)
            self.economy_Off.disabled = False
        else:
            self.remove_item(self.economy_Off)
            self.economy_On.disabled = False
    
    @nextcord.ui.button(label='Назад',style=nextcord.ButtonStyle.red,row=1)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = views.SettingsView(interaction.user)
        
        await interaction.message.edit(embed=view.embed,view=view)
    
    @nextcord.ui.button(label='Включить',style=nextcord.ButtonStyle.green,row=1,disabled=True)
    async def economy_On(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        es = self.es
        es['operate'] = True
        self.gdb.set('economic_settings',es)
    
    @nextcord.ui.button(label='Выключить',style=nextcord.ButtonStyle.red,row=1,disabled=True)
    async def economy_Off(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        es = self.es
        es['operate'] = False
        self.gdb.set('economic_settings',es)


