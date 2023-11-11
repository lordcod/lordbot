import nextcord
from bot.misc.utils import clord
from bot.databases.db import GuildDateBases


class Modal(nextcord.ui.Modal):
    type = 'modal'
    
    def __init__(self,name,value,default) -> None:
        super().__init__("Rewards", timeout=300)
        self.value = value
        self.bonus = nextcord.ui.TextInput(
            label=name,
            placeholder=default,
            max_length=6
        )
        self.add_item(self.bonus)
    
    async def callback(self, interaction: nextcord.Interaction) :
        gdb = GuildDateBases(interaction.guild_id)
        economy_settings = gdb.get('economic_settings',{})
        bonus = clord(self.bonus.value,int)
        
        if bonus:
            economy_settings[self.value] = bonus
        
        gdb.set('economic_settings',economy_settings)


class DropDown(nextcord.ui.Select):
    def __init__(self,guild_id):
        self.gdb = GuildDateBases(guild_id)
        self.economy_settings = self.gdb.get('economic_settings',{})
        options = [
            nextcord.SelectOption(
                label='Daily',
                description=self.economy_settings.get('daily',0),
                value='daily',
            ),
            nextcord.SelectOption(
                label='Weekly',
                description=self.economy_settings.get('weekly',0),
                value='weekly'
            ),
            nextcord.SelectOption(
                label='Monthly',
                description=self.economy_settings.get('monthly',0),
                value='monthly'
            )
        ]

        super().__init__(
            placeholder="Настройка бонусов:",
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        name = value.capitalize()
        default = self.economy_settings.get(value)
        await interaction.response.send_modal(Modal(name,value,default))


class Bonus(nextcord.ui.View):
    type = 'view'
    content = {}
    
    def __init__(self,guild_id) -> None:
        super().__init__()
        
        self.bonus = DropDown(guild_id)
        
        self.add_item(self.bonus)