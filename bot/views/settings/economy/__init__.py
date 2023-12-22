import nextcord

from .emoji import EmojiView
from .bonuses import Bonus
from ...settings import DefaultSettingsView

from bot.resources.ether import Emoji
from bot.databases.db import GuildDateBases
from bot.views import views

class DropDown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(
                label='Изменить сумму бонусов',emoji=Emoji.bagmoney, value='bonus'
            ),
            nextcord.SelectOption(
                label='Change the emoji',emoji=Emoji.emoji, value='emoji'
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
            'bonus':Bonus,
            'emoji': EmojiView
        }
        view = lists[value](interaction.guild)
        await interaction.message.edit(embed=view.embed,view=view)

class Economy(DefaultSettingsView):
    embed = nextcord.Embed(
        title='Система экономики',
        description=(
            "Экономическая система позволит вашему серверу подняться на совершенно другой уровень.\n"
            "Игры, уровни, рекламные акции, конкурсы и многое другое.\n"
            "Все это есть в нашей экономической системе.\n"
        )
    )
    
    def __init__(self,guild: nextcord.Guild) -> None:
        self.gdb = GuildDateBases(guild.id)
        self.es: dict = self.gdb.get('economic_settings',{})
        operate: bool = self.es.get('operate',False)
        colour: int = self.gdb.get('color',1974050)
        
        self.embed.color = colour
        
        super().__init__()
        
        self.economy_dd = DropDown()
        
        self.add_item(self.economy_dd)
        
        if operate:
            self.economy_switcher.label = "Disable"
            self.economy_switcher.style = nextcord.ButtonStyle.red
            self.economy_switcher_value = False
        else:
            self.economy_switcher.label = "Enable"
            self.economy_switcher.style = nextcord.ButtonStyle.green
            self.economy_switcher_value = True
            
            self.economy_dd.disabled = True
    
    @nextcord.ui.button(label='Назад',style=nextcord.ButtonStyle.red,row=1)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = views.SettingsView(interaction.user)
        
        await interaction.message.edit(embed=view.embed,view=view)
    
    @nextcord.ui.button(label='Switch',style=nextcord.ButtonStyle.green,row=1)
    async def economy_switcher(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.es['operate'] = self.economy_switcher_value
        self.gdb.set('economic_settings',self.es)
        
        view = self.__class__(interaction.guild)
        
        await interaction.message.edit(embed=view.embed, view=view)
    


