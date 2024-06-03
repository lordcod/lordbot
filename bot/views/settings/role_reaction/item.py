
import asyncio
from typing import Optional
import nextcord
from bot.databases import GuildDateBases
from bot.databases.varstructs import ReactionRoleItemPayload
from bot.misc.utils import to_async
from .._view import DefaultSettingsView
from .. import role_reaction
from ..set_reaction import fetch_reaction


class RoleReactionRegisterItemDropDown(nextcord.ui.StringSelect):
    def __init__(self, guild: nextcord.Guild, message_id: int, channel_id: int, role_reaction: ReactionRoleItemPayload, selected_role: Optional[nextcord.Role] = None) -> None:
        self.message_id = message_id
        self.channel_id = channel_id
        self.role_reaction = role_reaction

        options = [
            nextcord.SelectOption(
                label=f"@{role.name}",
                value=role_id,
                emoji=emoji,
                default=selected_role == role
            )
            for emoji, role_id in role_reaction['reactions'].items()
            if (role := guild.get_role(role_id))
        ]

        if 0 >= len(options):
            options.append(nextcord.SelectOption(label="SelectOption"))
            _disabled = True
        else:
            _disabled = False

        super().__init__(options=options, disabled=_disabled)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        role_id = int(self.values[0])
        role = interaction.guild.get_role(role_id)

        view = RoleReactionItemView(
            interaction.guild, self.message_id, self.channel_id, self.role_reaction, role)
        await interaction.message.edit(embed=view.embed, view=view)


class RoleReactionItemDropDown(nextcord.ui.RoleSelect):
    def __init__(self, guild: nextcord.Guild, message_id: int, channel_id: int, role_reaction: ReactionRoleItemPayload) -> None:
        self.message_id = message_id
        self.channel_id = channel_id
        self.role_reaction = role_reaction
        super().__init__()

    async def callback(self, interaction: nextcord.Interaction) -> None:
        role: nextcord.Role = self.values[0]

        if role.is_default():
            await interaction.response.send_message(
                content=f"The {role.mention} role is the default role for all users and can't be selected.",
                ephemeral=True
            )
            return
        elif role.is_premium_subscriber():
            await interaction.response.send_message(
                content=f"The {role.mention} role is a role that is used by subscribers of your server.",
                ephemeral=True
            )
            return
        elif role.is_integration() or role.is_bot_managed():
            await interaction.response.send_message(
                content=f"The {role.mention} role cannot be assigned and is used for integration or by a bot.",
                ephemeral=True
            )
            return
        elif not role.is_assignable():
            await interaction.response.send_message(
                content=f"The bot will not be able to assign the role {role.mention}, as that role is lower than the bot's. To resolve this issue, please move the role {interaction.guild.self_role.mention} to a higher position than {role.mention}.",
                ephemeral=True
            )
            return

        view = await RoleReactionItemView(
            interaction.guild, self.message_id, self.channel_id, self.role_reaction, role)
        await interaction.response.edit_message(embed=view.embed, view=view)


@to_async
class RoleReactionItemView(DefaultSettingsView):
    embed: nextcord.Embed = None

    async def __init__(self, guild: nextcord.Guild, message_id: int, channel_id: int, role_reaction: ReactionRoleItemPayload, selected_role: Optional[nextcord.Role] = None):
        gdb = GuildDateBases(guild.id)
        color = gdb.get('color')

        self.selected_role = selected_role
        self.role_reaction = role_reaction
        self.message_id = message_id
        self.channel_id = channel_id

        super().__init__()

        self.embed = nextcord.Embed(
            title="Roles for reactions",
            color=color,
            description='This module will help you assign roles based on reactions'
        )
        if role_reaction['reactions']:
            self.embed.add_field(
                name='Reactions',
                value='\n'.join([
                    f"・{emoji} - <@&{role_id}>"
                    for emoji, role_id in role_reaction['reactions'].items()
                ])
            )
            self.create.disabled = False
        if selected_role:
            self.update.disabled = False
            self.delete.disabled = False

        self.add_item(RoleReactionRegisterItemDropDown(
            guild, message_id, channel_id, role_reaction, selected_role))
        self.add_item(RoleReactionItemDropDown(
            guild, message_id, channel_id, role_reaction))

    @nextcord.ui.button(label="Back", style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction
                   ):
        view = await role_reaction.RoleReactionView(interaction.guild)

        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label="Create", style=nextcord.ButtonStyle.blurple, disabled=True)
    async def create(self,
                     button: nextcord.ui.Button,
                     interaction: nextcord.Interaction
                     ):
        channel = interaction.guild.get_channel(self.channel_id)
        message = channel.get_partial_message(self.message_id)

        for react in self.role_reaction['reactions']:
            asyncio.create_task(message.add_reaction(react))

        gdb = GuildDateBases(interaction.guild.id)
        await gdb.set_on_json('role_reactions', self.message_id, self.role_reaction)

        await self.back.callback(interaction)

    @nextcord.ui.button(label="Set reaction", style=nextcord.ButtonStyle.success, disabled=True)
    async def update(self,
                     button: nextcord.ui.Button,
                     interaction: nextcord.Interaction
                     ):
        message = await interaction.response.send_message(f"Send a reaction for role {self.selected_role.mention} by message", view=view, ephemeral=True)

        value = await fetch_reaction(interaction, message)

        for _emoji, _role_id in list(self.role_reaction['reactions'].items()):
            if _role_id == self.selected_role.id:
                self.role_reaction['reactions'].pop(_emoji)
        self.role_reaction['reactions'][value] = self.selected_role.id

        view = await RoleReactionItemView(
            interaction.guild, self.message_id, self.channel_id, self.role_reaction, self.selected_role)
        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label="Delete reaction", style=nextcord.ButtonStyle.red, disabled=True)
    async def delete(self,
                     button: nextcord.ui.Button,
                     interaction: nextcord.Interaction
                     ):
        for _emoji, _role_id in list(self.role_reaction['reactions'].items()):
            if _role_id == self.selected_role.id:
                self.role_reaction['reactions'].pop(_emoji)

        view = RoleReactionItemView(
            interaction.guild, self.message_id, self.channel_id, self.role_reaction)
        await interaction.response.edit_message(embed=view.embed, view=view)
