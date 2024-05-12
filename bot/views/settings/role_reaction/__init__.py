from typing import Optional
import nextcord
from bot.databases import GuildDateBases
from bot.databases.varstructs import ReactionRolePayload
from . import item
from .selector import RoleReactionSelectorView
from bot.views import settings_menu
from .._view import DefaultSettingsView


class RoleReactionDropDown(nextcord.ui.StringSelect):
    def __init__(self, guild: nextcord.Guild, selected_message_id: Optional[int] = None) -> None:
        gdb = GuildDateBases(guild.id)
        role_reaction: ReactionRolePayload = gdb.get('role_reactions')
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

        view = RoleReactionView(interaction.user.guild, message_id)

        await interaction.response.edit_message(embed=view.embed, view=view)


class RoleReactionView(DefaultSettingsView):
    embed: nextcord.Embed = None

    def __init__(self, guild: nextcord.Guild, message_id: Optional[int] = None) -> None:
        self.message_id = message_id
        gdb = GuildDateBases(guild.id)
        color = gdb.get('color')

        self.embed = nextcord.Embed(
            title="Roles for reactions",
            color=color,
            description='This module will help you assign roles based on reactions'
        )

        super().__init__()

        self.add_item(RoleReactionDropDown(guild, message_id))

        if message_id:
            self.edit.disabled = False
            self.delete.disabled = False

    @nextcord.ui.button(label="Back", style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction
                   ):
        view = settings_menu.SettingsView(interaction.user)

        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label="Add", style=nextcord.ButtonStyle.success)
    async def add(self,
                  button: nextcord.ui.Button,
                  interaction: nextcord.Interaction
                  ):
        view = await RoleReactionSelectorView.create(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label="Edit", style=nextcord.ButtonStyle.blurple, disabled=True)
    async def edit(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction
                   ):
        gdb = GuildDateBases(interaction.guild_id)
        all_role_reaction = gdb.get('role_reactions')
        role_reaction = all_role_reaction[self.message_id]

        view = item.RoleReactionItemView(
            interaction.guild, self.message_id, role_reaction['channel_id'], role_reaction)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.red, disabled=True)
    async def delete(self,
                     button: nextcord.ui.Button,
                     interaction: nextcord.Interaction
                     ):
        gdb = GuildDateBases(interaction.guild.id)
        role_reaction: ReactionRolePayload = gdb.get(
            'role_reactions')
        role_reaction.pop(self.message_id, None)
        gdb.set('role_reactions', role_reaction)

        view = RoleReactionView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
