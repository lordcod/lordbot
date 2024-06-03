import nextcord

from ... import ideas
from bot.views.settings._view import DefaultSettingsView
from bot.databases import GuildDateBases
from bot.databases.varstructs import IdeasPayload
from bot.misc.utils import TimeCalculator, to_async


@to_async
class CooldownModal(nextcord.ui.Modal):
    async def __init__(self, guild_id: int):
        self.gdb = GuildDateBases(guild_id)

        super().__init__("Cooldown")

        self.coldtime = nextcord.ui.TextInput(
            "Enter the time to delay between ideas",
            max_length=100
        )
        self.add_item(self.coldtime)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        try:
            cooltime = TimeCalculator[False].convert(self.coldtime.value)
        except ValueError:
            await interaction.response.send_message("It is necessary to write the time in the `1d2h10m` format")
            return
        await self.gdb.set_on_json('ideas', 'cooldown', cooltime)

        view = await CooldownView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)


@to_async
class CooldownView(DefaultSettingsView):
    embed: nextcord.Embed = None

    async def __init__(self, guild: nextcord.Guild) -> None:
        self.gdb = GuildDateBases(guild.id)
        self.idea_datas: IdeasPayload = await self.gdb.get('ideas')

        super().__init__()

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = await ideas.IdeasView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Edit', style=nextcord.ButtonStyle.blurple)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = await CooldownModal(interaction.guild_id)
        await interaction.response.send_modal(modal)
