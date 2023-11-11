import nextcord
from bot.databases.db import GuildDateBases
from .addtional import ViewBuilder

class DropDown(nextcord.ui.Select):
    def __init__(self,guild_id):
        self.gdb = GuildDateBases(guild_id)
        self.forum_message = forum_message  = self.gdb.get('thread_messages',{})
        
        options = [
            nextcord.SelectOption(
                label=f'<#{key}>',
            )
            for key in forum_message
        ]
    
        super().__init__(
            placeholder="Настройки авто-сообщений в ветках, форумах:",
            min_values=1,
            max_values=1,
            options=options,
        )
        
        if len(self.options) <= 0:
            self.disabled = True
            self.add_option(label='Нет настроек в данном модуле!')
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.send_message('Ok')

class AutoThreadMessage(nextcord.ui.View):
    type = 'view'
    content = {}
    
    def __init__(self,guild_id) -> None:
        super().__init__()
        
        self.auto = DropDown(guild_id)
        
        self.add_item(self.auto)
        
    @nextcord.ui.button(label='Добавить')
    async def addtion(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(view=ViewBuilder(),ephemeral=True)