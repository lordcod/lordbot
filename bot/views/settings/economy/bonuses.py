import nextcord
from bot.databases.db import GuildDateBases
from .. import economy
from ...settings import DefaultSettingsView


class Modal(nextcord.ui.Modal):
    def __init__(self, value: str, previous: str) -> None:
        super().__init__("Rewards", timeout=300)
        self.value = value
        self.bonus = nextcord.ui.TextInput(
            label=value.capitalize(),
            placeholder=previous,
            max_length=6
        )
        self.add_item(self.bonus)

    async def callback(self, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        economy_settings = gdb.get('economic_settings')
        bonus = self.bonus.value

        if not bonus.isdigit():
            return

        economy_settings[self.value] = int(bonus)

        gdb.set('economic_settings', economy_settings)

        view = Bonus(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)


class DropDown(nextcord.ui.Select):
    def __init__(self, guild_id):
        self.gdb = GuildDateBases(guild_id)
        self.economy_settings = self.gdb.get('economic_settings', {})
        options = [
            nextcord.SelectOption(
                label='Daily',
                value='daily',
            ),
            nextcord.SelectOption(
                label='Weekly',
                value='weekly'
            ),
            nextcord.SelectOption(
                label='Monthly',
                value='monthly'
            )
        ]

        super().__init__(
            placeholder="Setting up bonus amounts",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        previous = self.economy_settings.get(value)
        await interaction.response.send_modal(Modal(value, previous))


class Bonus(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        economy_settings = gdb.get('economic_settings')

        color = gdb.get('color', 1974050)
        self.embed = nextcord.Embed(
            title='Bonuses',
            color=color
        )
        self.embed.add_field(
            name="Daily",
            value=economy_settings.get('daily', 0)
        )
        self.embed.add_field(
            name="Weekly",
            value=economy_settings.get('weekly', 0)
        )
        self.embed.add_field(
            name="Monthly",
            value=economy_settings.get('monthly', 0)
        )

        super().__init__()

        self.bonus = DropDown(guild.id)

        self.add_item(self.bonus)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red, row=1)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = economy.Economy(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)
