import nextcord

from ... import permisson_command
from bot.views.settings._view import DefaultSettingsView

from bot.misc import utils
from bot.resources.ether import Emoji
from bot.databases.db import GuildDateBases, CommandDB
from bot.languages import help as help_info
from bot.languages.settings import (
    button as button_name
)

from typing import List


class DropDown(nextcord.ui.StringSelect):
    current_disabled = False

    def __init__(
        self,
        guild: nextcord.Guild,
        command_name: str,
        channels: list[nextcord.TextChannel]
    ) -> None:
        self.command_name = command_name
        options = []

        for tchnl in guild.text_channels[:25]:
            opt = nextcord.SelectOption(
                label=tchnl.name,
                value=tchnl.id,
                description=tchnl.topic,
                emoji=Emoji.channel_text,
            )
            if tchnl in channels:
                opt.default = True
            options.append(opt)

        if 0 >= len(options):
            options.append(
                nextcord.SelectOption(
                    label="To make it work"
                )
            )
            self.current_disabled = True
        super().__init__(
            placeholder="Select the channels in which the command will work",
            min_values=0,
            max_values=len(options),
            options=options,
            disabled=self.current_disabled
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        values = self.values
        channel_ids = [int(val) for val in values]

        cdb = CommandDB(interaction.guild_id)

        command_data = cdb.get(self.command_name, {})
        if "distribution" not in command_data:
            command_data["distribution"] = {}

        command_data["distribution"]["channel"] = {
            "permission": 1,
            "values": channel_ids
        }

        cdb.update(self.command_name, command_data)

        view = ChannelsView(
            interaction.guild,
            self.command_name
        )

        await interaction.message.edit(embed=view.embed, view=view)


class ChannelsView(DefaultSettingsView):
    embed: nextcord.Embed = None

    def __init__(self, guild: nextcord.Guild, command_name: str) -> None:
        self.command_name = command_name

        gdb = GuildDateBases(guild.id)
        color = gdb.get('color')

        cdb = CommandDB(guild.id)
        command_data = cdb.get(command_name, {})
        distribution = command_data.get("distribution", {})
        channel_perms = distribution.get("channel", None)

        channel_ids = []
        channels = []

        self.embed = nextcord.Embed(
            title="Allowed channels",
            description="The selected command will only work in the channels that you select",
            color=color
        )

        if channel_perms:
            channel_ids = channel_perms.get('values')
            channels = [guild.get_channel(id) for id in channel_ids]

        super().__init__()

        cdd = DropDown(
            guild,
            command_name,
            channels
        )
        self.add_item(cdd)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = permisson_command.precise.CommandData(
            interaction.guild,
            self.command_name
        )

        await interaction.message.edit(embed=view.embed, view=view)
