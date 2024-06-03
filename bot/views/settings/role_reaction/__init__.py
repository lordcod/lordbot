from typing import Optional
import nextcord
from bot.databases import GuildDateBases
from bot.databases.varstructs import ReactionRolePayload
from bot.misc.utils import to_async
from . import item
from .selector import RoleReactionSelectorView
from bot.views import settings_menu
from .._view import DefaultSettingsView


@to_async
class RoleReactionDropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild: nextcord.Guild, selected_message_id: Optional[int] = None) -> None:
        gdb = GuildDateBases(guild.id)
        role_reaction: ReactionRolePayload = await gdb.get('role_reactions')
        options = []
        for message_id, payload in role_reaction.items():
            channel = guild.get_channel(payload['channel_id'])

            options.append(nextcord.SelectOption(
                label=channel.name,
                description=f'MSG ID: {message_id}',
                value=str(message_id),
                default=message_id == selected_message_id
            ))

        if 0 >= len(options):
            options.append(nextcord.SelectOption(label="SelectOption"))
            _disabled = True
        else:
            _disabled = False
        super().__init__(options=options, disabled=_disabled)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        message_id = int(self.values[0])

        view = await RoleReactionView(interaction.user.guild, message_id)

        await interaction.response.edit_message(embed=view.embed, view=view)


@to_async
class RoleReactionView(DefaultSettingsView):
    embed: nextcord.Embed

    async def __init__(self, guild: nextcord.Guild, message_id: Optional[int] = None) -> None:
        self.message_id = message_id
        gdb = GuildDateBases(guild.id)
        color = await gdb.get('color')

        self.embed = nextcord.Embed(
            title="Roles for reactions",
            color=color,
            description='This module will help you assign roles based on reactions'
        )

        super().__init__()

        self.add_item(await RoleReactionDropDown(guild, message_id))

        if message_id:
            self.edit.disabled = False
            self.delete.disabled = False

    @nextcord.ui.button(label="Back", style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction
                   ):
        view = await settings_menu.SettingsView(interaction.user)

        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label="Add", style=nextcord.ButtonStyle.success)
    async def add(self,
                  button: nextcord.ui.Button,
                  interaction: nextcord.Interaction
                  ):
        view = await RoleReactionSelectorView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label="Edit", style=nextcord.ButtonStyle.blurple, disabled=True)
    async def edit(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction
                   ):
        gdb = GuildDateBases(interaction.guild_id)
        all_role_reaction = await gdb.get('role_reactions')
        role_reaction = all_role_reaction[self.message_id]

        view = await item.RoleReactionItemView(
            interaction.guild, self.message_id, role_reaction['channel_id'], role_reaction)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.red, disabled=True)
    async def delete(self,
                     button: nextcord.ui.Button,
                     interaction: nextcord.Interaction
                     ):
        gdb = GuildDateBases(interaction.guild.id)
        role_reaction: ReactionRolePayload = await gdb.get(
            'role_reactions')
        role_reaction.pop(self.message_id, None)
        await gdb.set('role_reactions', role_reaction)

        view = await RoleReactionView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
