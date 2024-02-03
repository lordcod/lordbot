import nextcord

from  ... import ideas
from ... import DefaultSettingsView

from bot.resources.ether import Emoji
from bot.databases.db import GuildDateBases
from bot.databases.varstructs import IdeasPayload
from bot.languages.settings import (
    button as button_name
)

from typing import List



class RolesDropDown(nextcord.ui.StringSelect):
    current_disabled = False
    
    def __init__(
        self, 
        guild: nextcord.Guild,
        app_role_ids: List[int]
    ) -> None:
        self.gdb = GuildDateBases(guild.id)
        self.idea_datas: IdeasPayload | None = self.gdb.get('ideas')
        mod_role_ids = self.idea_datas.get('moderation-role-ids')
        
        options = []
        
        for role in guild.roles:
            if (
                role.is_default() or
                role.is_premium_subscriber() or
                role.is_integration() or
                role.is_bot_managed()
            ):
                continue
            
            opt = nextcord.SelectOption(
                label=role.name,
                value=role.id,
                emoji=Emoji.frame_person,
                default=(role.id in mod_role_ids or role.id in app_role_ids)
            )
            
            options.append(opt)
        
        options = options[:25]
        
        if 0 >= len(options):
            options.append(
                nextcord.SelectOption(
                    label="-"
                )
            )
            self.current_disabled = True
        
        super().__init__(
            placeholder="Select the roles in which the command will work",
            min_values=1,
            max_values=len(options),
            options=options,
            disabled=self.current_disabled
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        view = ModerationRolesView(
            interaction.guild,
            list(map(int, self.values))
        )
        await interaction.message.edit(embed=view.embed, view=view)



class ModerationRolesView(DefaultSettingsView):
    embed: nextcord.Embed = None
    
    def __init__(self, guild: nextcord.Guild, role_ids: List[int] = None) -> None:
        self.gdb = GuildDateBases(guild.id)
        self.idea_datas: IdeasPayload | None = self.gdb.get('ideas')
        mod_role_ids = self.idea_datas.get('moderation-role-ids')
        color = self.gdb.get('color')
        
        super().__init__()
        
        if role_ids is not None:
            self.mod_roles = role_ids
            self.edit.disabled = False
        if mod_role_ids:
            self.delete.disabled = False
        
        
        cdd = RolesDropDown(guild, (role_ids or []))
        self.add_item(cdd)
    
    
    
    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = ideas.IdeasView(interaction.guild)
        
        await interaction.message.edit(embed=view.embed, view=view)
    
    
    @nextcord.ui.button(label='Edit', style=nextcord.ButtonStyle.blurple, disabled=True)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):  
        idea_datas = self.idea_datas
        idea_datas['moderation-role-ids'] = self.mod_roles
        
        self.gdb.set('ideas', idea_datas) 
        
        view = self.__class__(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)
    
    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, disabled=True)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):  
        idea_datas = self.idea_datas
        idea_datas['moderation-role-ids'] = []
        
        self.gdb.set('ideas', idea_datas) 
        
        view = self.__class__(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)