import nextcord

from ... import ideas
from ... import DefaultSettingsView

from bot.misc import utils
from bot.misc.ratelimit import BucketType
from bot.resources.ether import Emoji
from bot.databases.db import GuildDateBases, CommandDB
from bot.databases.varstructs import IdeasPayload
from bot.languages.settings import (
    button as button_name
)

from typing import Optional


class DropDown(nextcord.ui.ChannelSelect):
    def __init__(
        self,
        guild_id: int
    ) -> None:
        gdb = GuildDateBases(guild_id)
        self.idea_data = gdb.get('ideas')

        super().__init__(channel_types=[nextcord.ChannelType.text])

    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel = self.values[0]

        view = ApprovedView(interaction.guild, channel)

        await interaction.message.edit(embed=view.embed, view=view)


class ApprovedView(DefaultSettingsView):
    embed: nextcord.Embed = None

    def __init__(self, guild: nextcord.Guild, channel: Optional[nextcord.TextChannel] = None) -> None:
        self.gdb = GuildDateBases(guild.id)
        self.idea_datas: IdeasPayload | None = self.gdb.get('ideas')
        channel_approved_id = self.idea_datas.get('channel-approved-id')

        super().__init__()

        if channel is not None:
            self.channel = channel
            self.edit.disabled = False
        if channel_approved_id is not None:
            self.delete.disabled = False

        cdd = DropDown(guild.id)
        self.add_item(cdd)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = ideas.IdeasView(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Edit', style=nextcord.ButtonStyle.blurple, disabled=True)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        idea_datas = self.idea_datas
        idea_datas['channel-approved-id'] = self.channel.id

        self.gdb.set('ideas', idea_datas)

        view = self.__class__(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, disabled=True)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        idea_datas = self.idea_datas
        idea_datas.pop('channel-approved-id')

        self.gdb.set('ideas', idea_datas)

        view = self.__class__(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)
