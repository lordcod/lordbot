import nextcord

from ... import permisson_command
from bot.views.settings._view import DefaultSettingsView

from bot.misc import utils
from bot.misc.time_transformer import display_time
from bot.misc.ratelimit import BucketType, reset_cooldown
from bot.databases import GuildDateBases, CommandDB

cd_types = {
    0: 'Member',
    1: 'Server(global)'
}


class CoolModal(nextcord.ui.Modal):
    def __init__(
        self,
        cooltype: int,
        command_name: str,
        *,
        rate: int = None,
        per: float = None
    ) -> None:
        self.type = cooltype
        self.command_name = command_name

        super().__init__("Cooldown")

        self.rate = nextcord.ui.TextInput(
            label="Rate (Exemple: 2)",
            placeholder=rate,
            min_length=1,
            max_length=4,
        )
        self.per = nextcord.ui.TextInput(
            label="Per (Exemple: 1h10m)",
            placeholder=per,
            min_length=1,
            max_length=10
        )

        self.add_item(self.rate)
        self.add_item(self.per)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        srate = self.rate.value
        per = utils.calculate_time(self.per.value)
        rate = srate.isdigit() and int(srate)

        if not (per and rate):
            await interaction.response.send_message("Error #1", ephemeral=True)
            return

        cdb = CommandDB(interaction.guild.id)
        command_data = cdb.get(self.command_name, {})
        command_data.setdefault("distribution", {})

        command_data["distribution"]["cooldown"] = {
            "type": self.type,
            "rate": rate,
            "per": per
        }

        cdb.update(self.command_name, command_data)

        view = CooldownsView(
            interaction.guild,
            self.command_name
        )

        await interaction.message.edit(embed=view.embed, view=view)


class CooltypeDropDown(nextcord.ui.StringSelect):
    current_disabled = False

    def __init__(
        self,
        guild_id: int,
        command_name: str
    ) -> None:
        self.command_name = command_name

        options = [
            nextcord.SelectOption(
                label="Member",
                value=BucketType.MEMBER.value
            ),
            nextcord.SelectOption(
                label="Server",
                value=BucketType.SERVER.value
            )
        ]

        super().__init__(options=options)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        cooltype = int(self.values[0])

        modal = CoolModal(cooltype, self.command_name)

        await interaction.response.send_modal(modal)


class CooldownsView(DefaultSettingsView):
    embed: nextcord.Embed = None

    def __init__(self, guild: nextcord.Guild, command_name: str) -> None:
        self.command_name = command_name

        gdb = GuildDateBases(guild.id)
        lang = gdb.get('language')
        color = gdb.get('color')

        cdb = CommandDB(guild.id)
        command_data = cdb.get(command_name, {})
        distribution = command_data.get("distribution", {})
        self.cooldate = cooldate = distribution.get("cooldown", None)

        super().__init__()

        if isinstance(cooldate, dict):
            description = (
                "The current delay for the command\n"
                f"Type: **{cd_types.get(cooldate.get('type'))}**\n"
                f"Frequency of use: **{cooldate.get('rate')}** → **{display_time(cooldate.get('per', lang))}**\n"
            )
        else:
            self.remove_item(self.edit)
            self.remove_item(self.delete)
            description = "The delay is not set"

        self.embed = nextcord.Embed(
            title=f"Command: {command_name}",
            description=description,
            color=color
        )

        cdd = CooltypeDropDown(
            guild.id,
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

    @nextcord.ui.button(label='Edit', style=nextcord.ButtonStyle.blurple)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        cooltype = self.cooldate.get('type')

        modal = CoolModal(cooltype, self.command_name)

        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        cdb = CommandDB(interaction.guild.id)
        command_data = cdb.get(self.command_name, {})

        del command_data["distribution"]["cooldown"]

        cdb.update(self.command_name, command_data)

        reset_cooldown(interaction.guild_id, self.command_name)

        view = CooldownsView(
            interaction.guild,
            self.command_name
        )

        await interaction.message.edit(embed=view.embed, view=view)
