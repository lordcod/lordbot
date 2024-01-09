import nextcord

from ...settings import DefaultSettingsView

from bot.databases.varstructs import IdeasPayload
from bot.databases.db import GuildDateBases
from bot.views import views
from bot.views.ideas import IdeaBut
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
        ideas: IdeasPayload|None = gdb.get('ideas')
        
        enabled = ideas.get('enabled')
        
        self.embed = nextcord.Embed(
            title="Идеи",
            description="",
            color=colour
        )
        
        super().__init__()
        
        
        
        if channel_suggest := guild.get_channel(ideas.get("channel-suggest-id")):
            self.embed.description += f"Channel suggest: {channel_suggest.mention}\n"
        
        if channel_offers := guild.get_channel(ideas.get("channel-offers-id")):
            self.embed.description += f"Channel offers: {channel_offers.mention}\n"
        
        if channel_approved := guild.get_channel(ideas.get("channel-approved-id")):
            self.embed.description += f"Channel approved: {channel_approved.mention}\n"
        
        if moderation_role_ids := ideas.get("moderation-role-ids"):
            moderation_roles = filter(
                lambda item: item is not None,
                [guild.get_role(role_id) for role_id in moderation_role_ids]
            )
            if moderation_roles: self.embed.description += f"Moderation roles: {', '.join([role.mention for role in moderation_roles])}"
        
        
        if enabled:
            self.remove_item(self.enabled)
        else:
            self.remove_item(self.disabled)
        
        
        
        self.add_item(DropDown(guild.id))
        
        self.back.label = button_name.back.get(locale)
    
    
    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = views.SettingsView(interaction.user)
        
        await interaction.message.edit(embed=view.embed,view=view)
    
    @nextcord.ui.button(label='Enabled', style=nextcord.ButtonStyle.blurple)
    async def enabled(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        colour = gdb.get('color')
        ideas: IdeasPayload = gdb.get('ideas')
        
        channel_suggest_id = ideas.get("channel-suggest-id")
        channel_offers_id = ideas.get("channel-offers-id")
        
        channel_suggest = interaction.guild.get_channel(channel_suggest_id)
        channel_offers = interaction.guild.get_channel(channel_offers_id)
        
        if not (channel_suggest and channel_offers):
            await interaction.response.send_message(
                content=(
                    'You haven\'t set up everything to include ideas\n'
                    'Requirement value: **suggest** and **offers** channel'
                )
            )
            return
        
        embed = nextcord.Embed(
            title="Идеи",
            description=(
                "У тебя есть хорошая идея?\n"
                "И ты уверен что она всем понравится!\n"
                "Прежде чем ты ее напишешь, убедитесь, что таких идей еще не было!"
            ),
            colour=colour
        )
        view = IdeaBut(interaction.guild_id)
        
        message_suggest = await channel_suggest.send(embed=embed, view=view)
        
        ideas['message-suggest-id'] = message_suggest.id
        ideas['enabled'] = True
        
        gdb.set('ideas', ideas)
        
        view = self.__class__(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)
    
    @nextcord.ui.button(label='Disabled', style=nextcord.ButtonStyle.red)
    async def disabled(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        ideas: IdeasPayload = gdb.get('ideas')
        
        channel_suggest_id = ideas.get("channel-suggest-id")
        message_suggest_id = ideas.get("message-suggest-id")
        
        if channel_suggest_id and message_suggest_id:
            try:
                channel_suggest = interaction.guild.get_channel(channel_suggest_id)
                message_suggest = channel_suggest.get_partial_message(message_suggest_id)
                await message_suggest.delete()
            except:
                pass
        
        ideas['enabled'] = False
        
        gdb.set('ideas', ideas)
        
        view = self.__class__(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)
