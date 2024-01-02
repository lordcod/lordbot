import nextcord

from ...settings import DefaultSettingsView

from bot.databases.varstructs import IdeasPayload
from bot.databases.db import GuildDateBases
from bot.views import views
from bot.languages.settings import (
    disabled_commands as disabled_commands_langs,
    button as button_name
)
from bot.resources.ether import Emoji


class DropDown(nextcord.ui.Select):
    def __init__(self, guild_id, name):
        self.gdb = GuildDateBases(guild_id)
        locale = self.gdb.get('language')
        
        options = [
            nextcord.SelectOption(
                label='Suggest',
            ),
            nextcord.SelectOption(
                label='Offers',
            ),
            nextcord.SelectOption(
                label='Approved',
            ),
            nextcord.SelectOption(
                label='Moderation roles',
            ),
        ]
        
        
        super().__init__(
            placeholder=disabled_commands_langs.placeholder.get(locale),
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        catalog = self.values[0]
        print(catalog)
        # await interaction.message.edit(embed=view.embed, view=view)


class IdeasView(DefaultSettingsView):
    embed: nextcord.Embed
    
    def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        colour: int = gdb.get('color')
        locale: str = gdb.get('language')
        ideas: IdeasPayload = gdb.get('ideas')
        
        self.embed = nextcord.Embed(
            title=disabled_commands_langs.title.get(locale),
            color=colour
        )
        
        if ideas:
            channel_suggest_id = ideas.get("channel-suggest-id")
            channel_offers_id = ideas.get("channel-offers-id")
            channel_approved_id = ideas.get("channel-approved-id")
            moderation_role_ids = ideas.get("moderation-role-ids")
            
            channel_suggest = guild.get_channel(channel_suggest_id)
            channel_offers = guild.get_channel(channel_offers_id)
            channel_approved = guild.get_channel(channel_approved_id)
            moderation_roles = filter(
                lambda item: item is not None,
                [guild.get_role(role_id) for role_id in moderation_role_ids]
            )
            
            
            self.embed.description = (
                f"Channel suggest: {channel_suggest.mention}\n"
                f"Channel offers: {channel_offers.mention}\n"
                f"Channel approved: {channel_approved.mention}\n"
                f"Moderation roles: {', '.join([role.mention for role in moderation_roles])}"
            )
        else:
            self.embed.description = "The module is not configured"
        
        super().__init__()
        
        self.back.label = button_name.back.get(locale)
    
    
    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = views.SettingsView(interaction.user)
        
        await interaction.message.edit(embed=view.embed,view=view)
    
    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.back.callback(interaction)
