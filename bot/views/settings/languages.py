import nextcord
from bot import languages
from bot.views import views
from ..settings import DefaultSettingsView
from bot.databases.db import GuildDateBases
from nextcord.utils import find


class DropDown(nextcord.ui.Select):
    def __init__(self,guild_id):
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language','en')
        
        options = [
            nextcord.SelectOption(
                label=f"{data.get('english_name')} ({data.get('native_name')})", 
                value=data.get('locale'), 
                emoji=data.get('flag',None),
                default=True if locale == data.get('locale') else False
            )
            for data in languages.current[:24]
        ]

        super().__init__(
            placeholder="Выберите язык для сервера:",
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        gdb = GuildDateBases(interaction.guild_id)
        
        langData = find(lambda lan:lan.get('locale',None)==value,languages.current)
        
        gdb.set('language',langData.get('locale'))
        
        
        await interaction.response.send_message(f"Selected language: {langData.get('native_name')}",ephemeral=True)

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
        
        lang = DropDown(guild.id)
        
        self.add_item(lang)
    
    
    @nextcord.ui.button(label='Назад',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = views.SettingsView(interaction.user) 
        
        await interaction.message.edit(embed=view.embed,view=view)

