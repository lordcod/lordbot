import nextcord

from ...settings import DefaultSettingsView

from bot.resources.ether import Emoji
from bot.views import views
from bot.databases.db import GuildDateBases
from bot.languages.settings import (
    button as button_name
)


class DropDown(nextcord.ui.Select):
    is_option = False
    
    def __init__(self,guild: nextcord.Guild):
        self.gdb = GuildDateBases(guild.id)
        locale = self.gdb.get('language')
        
        options = [
            nextcord.SelectOption(
                label='Welcoming new members',
                emoji=Emoji.frame_person,
                value='welcoming'
            ),
            nextcord.SelectOption(
                label='Automatic roles',
                emoji=Emoji.auto_role,
                value='roles'
            )
        ]
    
        super().__init__(
            placeholder='Define the greeting setting:',
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        await interaction.response.send_message('The menu is being developed!', ephemeral=True)

class Greeting(DefaultSettingsView):
    embed: nextcord.Embed
    
    def __init__(self,guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        colour = gdb.get('color')
        locale = gdb.get('language')
        
        self.embed = nextcord.Embed(
            title='The Participant Welcome module',
            description='A module that is equipped with an automatic greeting and roles',
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
