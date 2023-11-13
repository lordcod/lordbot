import nextcord
from bot.databases.db import GuildDateBases

class DropDown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(
                label='Создать новый'
            )
        ]

        super().__init__(
            placeholder="Настройки экономики:",
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        pass

class AutoTranslate(nextcord.ui.View):
    type = 'view'
    content = {}
    
    def __init__(self,guild_id) -> None:
        self.gdb = GuildDateBases(guild_id)
        self.es = self.gdb.get('economic_settings',{})
        
        super().__init__()
        
        self.auto = DropDown()
        
        self.add_item(self.auto)
