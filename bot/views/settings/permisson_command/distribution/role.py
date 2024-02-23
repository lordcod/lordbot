import nextcord

from ... import permisson_command
from bot.views.settings._view import DefaultSettingsView

from bot.databases import GuildDateBases, CommandDB


class RolesDropDown(nextcord.ui.RoleSelect):
    def __init__(
        self,
        guild: nextcord.Guild,
        command_name: str
    ) -> None:
        self.command_name = command_name
        self.gdb = GuildDateBases(guild.id)

        super().__init__(
            min_values=1,
            max_values=15,
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        for role in self.values.roles:
            if role.is_integration() or role.is_bot_managed():
                await interaction.response.send_message(
                    content=f"The {role.mention} role cannot be assigned and is used for integration or by a bot.",
                    ephemeral=True
                )
                break
        else:
            await interaction.response.defer()
            cdb = CommandDB(interaction.guild_id)

            command_data = cdb.get(self.command_name, {})
            command_data.setdefault("distribution", {})

            command_data["distribution"]["role"] = {
                "permission": 1,
                "values": self.values.ids
            }

            cdb.update(self.command_name, command_data)

        view = RolesView(
            interaction.guild,
            self.command_name
        )

        await interaction.message.edit(embed=view.embed, view=view)


class RolesView(DefaultSettingsView):
    embed: nextcord.Embed = None

    def __init__(self, guild: nextcord.Guild, command_name: str) -> None:
        self.command_name = command_name

        gdb = GuildDateBases(guild.id)
        color = gdb.get('color')

        cdb = CommandDB(guild.id)
        command_data = cdb.get(self.command_name, {})
        command_data.setdefault("distribution", {})

        self.embed = nextcord.Embed(
            title="Allowed roles",
            description="The selected command will only work in the roles that you select",
            color=color
        )
        role_ids = command_data["distribution"].get(
            "role", {}).get("values")

        self.embed.add_field(
            name="Selected roles:",
            value=', '.join(filter(
                lambda item: item is not None,
                [guild.get_role(role_id) for role_id in role_ids]
            )))

        super().__init__()

        cdd = RolesDropDown(
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
