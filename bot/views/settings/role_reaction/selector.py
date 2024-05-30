from typing import List, Optional
import nextcord
from bot.databases import GuildDateBases
from bot.databases.varstructs import ReactionRolePayload
from bot.misc import utils
from . import item
from .. import role_reaction
from .._view import DefaultSettingsView


@utils.to_async
class RoleReactionSelectorChannelDropDown(nextcord.ui.ChannelSelect):
    async def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        super().__init__(channel_types=[
            nextcord.ChannelType.text,
            nextcord.ChannelType.voice,
            nextcord.ChannelType.news,
            nextcord.ChannelType.stage_voice,
            nextcord.ChannelType.guild_directory
        ])

    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel = self.values[0]

        view = await RoleReactionSelectorView(interaction.user.guild, channel)

        await interaction.response.edit_message(embed=view.embed, view=view)


@utils.to_async
class RoleReactionSelectorMessageDropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild: nextcord.Guild, channel: Optional[nextcord.TextChannel] = None, selected_message_id: Optional[int] = None) -> None:
        self.channel = channel
        if channel:
            messages = await channel.history(limit=15).flatten()
        if not (channel and messages):
            super().__init__(options=[nextcord.SelectOption(
                label="SelectOption")], disabled=True)
            return

        options = [
            nextcord.SelectOption(
                label=f'ID: {mes.id}({mes.author.name})',
                value=mes.id,
                description=self.get_content(mes),
                default=mes.id == selected_message_id
            )
            for mes in messages
        ]

        if 0 >= len(options):
            options.append(nextcord.SelectOption(label="SelectOption"))
            _disabled = True
        else:
            _disabled = False
        super().__init__(options=options, disabled=_disabled)

    @staticmethod
    def get_content(mes: nextcord.Message) -> Optional[str]:
        if mes.content:
            return utils.cut_back(mes.content, 100)
        if mes.embeds:
            return utils.cut_back(f"[EMBEDS] {title if (title := mes.embeds[0].title) else ''}", 100)
        if mes.attachments:
            return '[ATTACHMENTS]'
        return None

    async def callback(self, interaction: nextcord.Interaction) -> None:
        message_id = int(self.values[0])

        view = await RoleReactionSelectorView(
            interaction.user.guild, self.channel, message_id)

        await interaction.response.edit_message(embed=view.embed, view=view)


@utils.to_async
class RoleReactionSelectorView(DefaultSettingsView):
    embed: nextcord.Embed = None

    async def __init__(self, guild: nextcord.Guild, channel: Optional[nextcord.TextChannel] = None, message_id: Optional[int] = None) -> None:
        gdb = GuildDateBases(guild.id)
        color = await gdb.get('color')

        self.channel = channel
        self.message_id = message_id

        self.embed = nextcord.Embed(
            title="Roles for reactions",
            color=color,
            description='This module will help you assign roles based on reactions'
        )

        super().__init__()

        self.add_item(await RoleReactionSelectorChannelDropDown(guild))
        self.add_item(
            await RoleReactionSelectorMessageDropDown(guild, channel, message_id))
        if message_id:
            self.next.disabled = False

    @nextcord.ui.button(label="Back", style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction
                   ):
        view = await role_reaction.RoleReactionView(interaction.user)

        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label="Next", style=nextcord.ButtonStyle.blurple, disabled=True)
    async def next(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction
                   ):
        role_reaction = {
            'channel_id': self.channel.id,
            'reactions': {}
        }

        view = await item.RoleReactionItemView(
            interaction.user, self.message_id, self.channel.id, role_reaction)

        await interaction.response.edit_message(embed=view.embed, view=view)
