import nextcord

from ..greeting import Greeting
from ...settings import DefaultSettingsView

from bot.misc import utils
from bot.resources.ether import Emoji
from bot.views import views
from bot.databases.db import GuildDateBases
from bot.languages.settings import button as button_name
from bot.languages.settings.greeting import role as role_lang

from typing import Optional, List

class DropDownBuilder(nextcord.ui.RoleSelect):
    def __init__(self, guild_id) -> None:
        super().__init__(
            placeholder=None,
            min_values=1,
            max_values=5
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        roles: List[nextcord.Role] = self.values
        
        view = ViewBuilder(interaction.guild, roles)
        
        await interaction.message.edit(embed=view.embed, view=view)

class ViewBuilder(DefaultSettingsView):
    embed: nextcord.Embed
    
    def __init__(self,guild: nextcord.Guild, roles: List[nextcord.Role] = []) -> None:
        self.gdb = GuildDateBases(guild.id)
        colour = self.gdb.get('color')
        locale = self.gdb.get('language')
        roles_ids = self.gdb.get('auto_roles')
        
        super().__init__()
        
        
        DDB = DropDownBuilder(guild.id)
        
        self.add_item(DDB)
        
        self.back.label = button_name.back.get(locale)
        self.install.label = role_lang.install.get(locale)
        
        if roles:
            self.install.disabled = False
            self.roles = roles
            
            self.remove_item(self.delete)
        elif roles_ids:
            self.delete.disabled = False
            
            self.remove_item(self.install)
        else:
            self.remove_item(self.install)
            self.remove_item(self.delete)
        
        
        self.embed = nextcord.Embed(
            title=role_lang.embed_title.get(locale),
            description=role_lang.embed_description.get(locale),
            color=colour
        )
        
        if roles_ids:
            roles = [guild.get_role(role_id) for role_id in roles_ids]
            utils.remove_none(roles)
            
            self.embed.add_field(
                name=role_lang.embed_field.get(locale),
                value=', '.join([role.mention for role in roles])
            )
    
    
    @nextcord.ui.button(label='Back',style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = Greeting(interaction.guild)
        
        await interaction.message.edit(embed=view.embed, view=view)
    
    @nextcord.ui.button(label='Install roles',style=nextcord.ButtonStyle.blurple,disabled=True)
    async def install(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = self.gdb 
        roles_ids = [role.id for role in self.roles]
        
        gdb.set('auto_roles',roles_ids)
        
        view = ViewBuilder(interaction.guild)
        
        await interaction.message.edit(embed=view.embed, view=view)
    
    @nextcord.ui.button(label='Delete roles',style=nextcord.ButtonStyle.red,disabled=True)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = self.gdb 
        roles_ids = []
        
        gdb.set('auto_roles',roles_ids)
        
        view = ViewBuilder(interaction.guild)
        
        await interaction.message.edit(embed=view.embed, view=view)