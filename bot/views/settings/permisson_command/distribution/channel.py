import nextcord

from ... import permisson_command
from bot.views.settings._view import DefaultSettingsView

from bot.databases import GuildDateBases, CommandDB


class ChannelsDropDown(nextcord.ui.ChannelSelect):
    def __init__(
        self,
        guild: nextcord.Guild,
        command_name: str
    ) -> None:
        self.command_name = command_name

        super().__init__(
            placeholder="Select the channels in which the command will work",
            min_values=1,
            max_values=15
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        cdb = CommandDB(interaction.guild_id)

        command_data = cdb.get(self.command_name, {})
        command_data.setdefault("distribution", {})

        command_data["distribution"]["channel"] = {
            "permission": 1,
            "values": self.values.ids
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
        command_data = cdb.get(self.command_name, {})
        command_data.setdefault("distribution", {})

        channel_ids = command_data["distribution"].get(
            "channel", {}).get("values")

        self.embed = nextcord.Embed(
            title="Allowed channels",
            description="The selected command will only work in the channels that you select",
            color=color
        )
        if channel_ids:
            self.embed.add_field(
                name="Selected channels:",
                value=', '.join(filter(
                    lambda item: item is not None,
                    [guild.get_channel(channel_id)
                     for channel_id in channel_ids]
                )))

        super().__init__()

        cdd = ChannelsDropDown(
            guild,
            command_name
        )
        self.add_item(cdd)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = permisson_command.precise.CommandData(
            interaction.guild,
            self.command_name
        )

        await interaction.message.edit(embed=view.embed, view=view)
