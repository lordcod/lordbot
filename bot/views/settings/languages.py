import nextcord
from bot.resources.languages import Languages_self as AllLangs
from bot.views import views
from ..settings import DefaultSettingsView
from bot.databases.db import GuildDateBases


class DropDown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(
                label=data.get('native_name'), value=data.get('discord_language'), emoji=data.get('flag',None)
            )
            for data in AllLangs[:24]
        ]

        super().__init__(
            placeholder="Выберите язык для сервера:",
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        await interaction.response.send_message(f'Selected language: {value}',ephemeral=True)

class Languages(DefaultSettingsView):
    embed = nextcord.Embed(
        title='Язык',
        description='Эта настройка изменяет язык для работы с ботом. Выберите язык сервера.'
    )
    
    def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        colour = gdb.get('color',1974050)
        self.embed.color = colour
        
        super().__init__()
        
        lang = DropDown()
        
        self.add_item(lang)
    
    
    @nextcord.ui.button(label='Назад',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = views.SettingsView(interaction.user) 
        
        await interaction.message.edit(embed=view.embed,view=view)

