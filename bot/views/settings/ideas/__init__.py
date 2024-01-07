import nextcord

from ...settings import DefaultSettingsView

from bot.databases.varstructs import ParticleIdeasPayload
from bot.databases.db import GuildDateBases
from bot.views import views
from bot.languages.settings import (
    disabled_commands as disabled_commands_langs,
    button as button_name
)
from bot.resources.ether import Emoji



class DropDown(nextcord.ui.Select):
    def __init__(self, guild_id):
        self.gdb = GuildDateBases(guild_id)
        locale = self.gdb.get('language')
        
        options = [
            nextcord.SelectOption(
                label='Suggest',
                value='suggest'
            ),
            nextcord.SelectOption(
                label='Offers',
                value='offers'
            ),
            nextcord.SelectOption(
                label='Approved',
                value='approved'
            ),
            nextcord.SelectOption(
                label='Moderation roles',
                value='moderation-roles'
            ),
        ]
        
        
        super().__init__(
            min_values=1,
            max_values=1,
            options=options,
        )
    
    async def callback(self, interaction: nextcord.Interaction) -> None:
        catalog = self.values[0]
        
        await interaction.response.send_message(catalog, ephemeral=True)


class IdeasView(DefaultSettingsView):
    embed: nextcord.Embed
    
    def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        colour: int = gdb.get('color')
        locale: str = gdb.get('language')
        ideas: ParticleIdeasPayload = gdb.get('ideas')
        
        self.embed = nextcord.Embed(
            title=disabled_commands_langs.title.get(locale),
            description="",
            color=colour
        )
        
        if ideas:
            if channel_suggest_id := ideas.get("channel-suggest-id"):
                channel_suggest = guild.get_channel(channel_suggest_id)
                self.embed.description += f"Channel suggest: {channel_suggest.mention}\n"
            
            if channel_offers_id := ideas.get("channel-offers-id"):
                channel_offers = guild.get_channel(channel_offers_id)
                self.embed.description += f"Channel offers: {channel_offers.mention}\n"
            
            if channel_approved_id := ideas.get("channel-approved-id"):
                channel_approved = guild.get_channel(channel_approved_id)
                self.embed.description += f"Channel approved: {channel_approved.mention}\n"
            
            if moderation_role_ids := ideas.get("moderation-role-ids"):
                moderation_roles = filter(
                    lambda item: item is not None,
                    [guild.get_role(role_id) for role_id in moderation_role_ids]
                )
                self.embed.description += f"Moderation roles: {', '.join([role.mention for role in moderation_roles])}"
            
        else:
            self.embed.description = "The module is not configured"
        
        super().__init__()
        
        self.add_item(DropDown(guild.id))
        
        self.back.label = button_name.back.get(locale)
    
    
    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = views.SettingsView(interaction.user)
        
        await interaction.message.edit(embed=view.embed,view=view)
    
    @nextcord.ui.button(label='Enabled', style=nextcord.ButtonStyle.blurple)
    async def switcher(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        ideas: ParticleIdeasPayload = gdb.get('ideas')
        
        channel_suggest_id = ideas.get("channel-suggest-id")
        channel_offers_id = ideas.get("channel-offers-id")
        
        if not (channel_suggest_id and channel_offers_id):
            await interaction.response.send_message('You haven\'t set up everything to include ideas')
            return
    
    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.back.callback(interaction)
