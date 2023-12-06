import nextcord

from ...settings import DefaultSettingsView

from bot.resources.ether import Emoji
from bot.views import views
from bot.databases.db import GuildDateBases
from bot.languages.settings.greeting import (
    init_embed as init_embed_lang,
    init_dropdown as init_dropdown_lang
)
from bot.languages.settings import (
    button as button_name
)

moduls = None

def get_moduls():
    from .role import ViewBuilder as RoleView
    from .welcome import ViewBuilder as WelcomeView
    
    _moduls = {
        'roles': RoleView,
        'welcome': WelcomeView
    }
    
    return _moduls


class DropDown(nextcord.ui.Select):
    is_option = False
    
    def __init__(self,guild: nextcord.Guild):
        self.gdb = GuildDateBases(guild.id)
        locale = self.gdb.get('language')
        
        options = [
            nextcord.SelectOption(
                label=init_dropdown_lang.welcome_label.get(locale),
                emoji=Emoji.frame_person,
                value='welcome'
            ),
            nextcord.SelectOption(
                label=init_dropdown_lang.roles_label.get(locale),
                emoji=Emoji.auto_role,
                value='roles'
            )
        ]
    
        super().__init__(
            placeholder=init_dropdown_lang.placeholder.get(locale),
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        global moduls
        if not moduls:
            moduls = get_moduls()
        
        value = self.values[0]
        
        view = moduls[value](interaction.guild)
        
        await interaction.message.edit(embed=view.embed, view=view)

class Greeting(DefaultSettingsView):
    embed: nextcord.Embed
    
    def __init__(self,guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        colour = gdb.get('color')
        locale = gdb.get('language')
        
        self.embed = nextcord.Embed(
            title=init_embed_lang.title.get(locale),
            description=init_embed_lang.description.get(locale),
            color = colour
        )
        
        super().__init__()
        
        self.back.label = button_name.back.get(locale)
        
        auto = DropDown(guild)
        
        if not auto.is_option:
            self.add_item(auto)
    
    
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = views.SettingsView(interaction.user)
        
        await interaction.message.edit(embed=view.embed,view=view)
