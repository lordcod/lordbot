import nextcord

from ..settings import DefaultSettingsView

from bot.databases.db import GuildDateBases
from bot.views import views
from bot.languages.settings import (
    disabled_commands as disabled_commands_langs,
    button as button_name
)
from bot.languages import help
from bot.resources.ether import Emoji

from typing import List,Dict,Union



class DropDown(nextcord.ui.Select):
    is_option = False
    
    def __init__(self,guild_id):
        self.gdb = GuildDateBases(guild_id)
        locale = self.gdb.get('language')
        disabled_commands = self.gdb.get('disabled_commands')
        
        options = []
        for command in help.commands[0:25]:
            if not command.get('allowed_disabled'):
                continue
            
            selectOption = nextcord.SelectOption(
                label=command.get('name'),
                value=command.get('name')
            )
            
            
            selectOption.description=command.get('brief_descriptrion').get(locale)
            
            if command.get('name') in disabled_commands:
                emoji = nextcord.PartialEmoji.from_str(Emoji.disabled)
                selectOption.emoji = emoji
                selectOption.default = True
            else:
                emoji = nextcord.PartialEmoji.from_str(Emoji.enabled)
                selectOption.emoji = emoji
                selectOption.default = False
            
            options.append(selectOption)
    
    
        super().__init__(
            placeholder=disabled_commands_langs.placeholder.get(locale),
            min_values=0,
            max_values=len(options),
            options=options,
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        locale = self.gdb.get('language')
        
        disabled_commands = self.values
        self.gdb.set('disabled_commands',disabled_commands)
        
        string_DC = ',\n'.join(disabled_commands)
        embed = nextcord.Embed(
            title=disabled_commands_langs.embed_title.get(locale)
        )
        if string_DC:
            embed.description = (
                f'{disabled_commands_langs.embed_description_list.get(locale)}\n'
                f"{string_DC}"
            )
        else:
            embed.description = disabled_commands_langs.embed_description_no_disabled.get(locale)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        view = DisabledCommandsView(interaction.guild)
        
        await interaction.message.edit(embed=view.embed, view=view)


class DisabledCommandsView(DefaultSettingsView):
    embed: nextcord.Embed
    
    def __init__(self,guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        colour = gdb.get('color')
        locale = gdb.get('language')
        
        self.embed = nextcord.Embed(
            title=disabled_commands_langs.title.get(locale),
            description=disabled_commands_langs.description.get(locale),
            color = colour
        )
        
        super().__init__()
        
        self.add_item(DropDown(guild.id))
        
        self.back.label = button_name.back.get(locale)
    
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = views.SettingsView(interaction.user)
        
        await interaction.message.edit(embed=view.embed,view=view)

