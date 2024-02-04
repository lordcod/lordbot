import nextcord

from .emoji import EmojiView
from .bonuses import Bonus
from ...settings import DefaultSettingsView

from bot.resources.ether import Emoji
from bot.databases.db import GuildDateBases
from bot.views import settings_menu

class DropDown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(
                label='Change the amount of bonuses',emoji=Emoji.bagmoney, value='bonus'
            ),
            nextcord.SelectOption(
                label='Change the emoji',emoji=Emoji.emoji, value='emoji'
            )
        ]

        super().__init__(
            placeholder="Economy Settings:",
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
        title='The economic system',
        description=(
            "The economic system will allow your server to rise to a completely different level.\n"
            "Games, levels, promotions, contests and more.\n"
            "All this is in our economic system.\n"
        )
    )
    
    def __init__(self,guild: nextcord.Guild) -> None:
        self.gdb = GuildDateBases(guild.id)
        self.es: dict = self.gdb.get('economic_settings')
        operate: bool = self.es.get('operate')
        color: int = self.gdb.get('color')
        
        self.embed.color = color
        
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
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red,row=1)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = settings_menu.SettingsView(interaction.user)
        
        await interaction.message.edit(embed=view.embed,view=view)
    
    @nextcord.ui.button(label='Switch',style=nextcord.ButtonStyle.green,row=1)
    async def economy_switcher(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.es['operate'] = self.economy_switcher_value
        self.gdb.set('economic_settings',self.es)
        
        view = self.__class__(interaction.guild)
        
        await interaction.message.edit(embed=view.embed, view=view)
    


