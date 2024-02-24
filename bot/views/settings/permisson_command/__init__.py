import nextcord

from .precise import CommandData
from bot.views.settings._view import DefaultSettingsView

from bot.databases import GuildDateBases
from bot.views import settings_menu
from bot.languages import help, i18n


class DropDown(nextcord.ui.Select):
    def __init__(self, guild_id, name):
        self.gdb = GuildDateBases(guild_id)
        locale = self.gdb.get('language')

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
        view = CommandData(interaction.guild, command)

        await interaction.message.edit(embed=view.embed, view=view)


class CommandsDataView(DefaultSettingsView):
    foundation: list = list(help.categories.keys())
    step: int
    maximum: int = len(foundation)-1

    embed: nextcord.Embed

    def __init__(self, guild: nextcord.Guild, step=0) -> None:
        self.step = step

        gdb = GuildDateBases(guild.id)
        color = gdb.get('color')
        locale = gdb.get('language')

        self.embed = nextcord.Embed(
            title="Command Permission",
            description="",
            color=color
        )

        super().__init__()

        self.add_item(DropDown(guild.id, self.foundation[step]))

        self.back.label = i18n.t(locale, 'settings.button.back')

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = settings_menu.SettingsView(interaction.user)

        await interaction.message.edit(embed=view.embed, view=view)

    async def visual_handler(self, interaction: nextcord.Interaction):
        view = self.__class__(interaction.guild, self.step)
        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Previous', style=nextcord.ButtonStyle.grey)
    async def previous(self,
                       button: nextcord.ui.Button,
                       interaction: nextcord.Interaction):
        if 0 > (self.step - 1):
            return

        self.step -= 1

        await self.visual_handler(interaction)

    @nextcord.ui.button(label='Next', style=nextcord.ButtonStyle.grey)
    async def next(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        if (self.step + 1) > self.maximum:
            return

        self.step += 1

        await self.visual_handler(interaction)
