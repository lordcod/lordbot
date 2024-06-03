import nextcord

from bot.misc.utils import to_async

from .precise import CommandData
from bot.views.settings._view import DefaultSettingsView

from bot.databases import GuildDateBases
from bot.views import settings_menu
from bot.languages import help, i18n


@to_async
class PermDropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild_id, name):
        self.gdb = GuildDateBases(guild_id)
        locale = await self.gdb.get('language')

        commands = help.categories.get(name)
        options = []

        for command in commands:
            selectOption = nextcord.SelectOption(
                label=command.get('name'),
                value=command.get('name'),
                description=command.get('brief_descriptrion').get(locale),
                emoji=help.categories_emoji.get(name),
            )
            options.append(selectOption)

        super().__init__(
            placeholder="Choose command:",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        command = self.values[0]
        view = await CommandData(interaction.guild, command)
        await interaction.response.edit_message(embed=view.embed, view=view)


@to_async
class CommandsDataView(DefaultSettingsView):
    foundation: list = list(help.categories)
    step: int
    embed: nextcord.Embed

    async def __init__(self, guild: nextcord.Guild, step: int = 0) -> None:
        self.step = step

        gdb = GuildDateBases(guild.id)
        color = await gdb.get('color')
        locale = await gdb.get('language')

        self.embed = nextcord.Embed(
            title="Command Permission",
            description="",
            color=color
        )

        super().__init__()

        if self.step + 1 >= len(self.foundation):
            self.next.disabled = True
        if 0 > self.step - 1:
            self.previous.disabled = True

        dd = PermDropDown(guild.id, self.foundation[step])
        self.add_item(dd)
        self.back.label = i18n.t(locale, 'settings.button.back')

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = await settings_menu.SettingsView(interaction.user)

        await interaction.response.edit_message(embed=view.embed, view=view)

    async def visual_handler(self, interaction: nextcord.Interaction):
        view = await CommandData(interaction.guild, self.step)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Previous', style=nextcord.ButtonStyle.grey)
    async def previous(self,
                       button: nextcord.ui.Button,
                       interaction: nextcord.Interaction):
        self.step -= 1
        await self.visual_handler(interaction)

    @nextcord.ui.button(label='Next', style=nextcord.ButtonStyle.grey)
    async def next(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        self.step += 1
        await self.visual_handler(interaction)
