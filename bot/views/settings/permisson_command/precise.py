import nextcord

from .. import permisson_command
from .distribution.channel import ChannelsView
from .distribution.role import RolesView
from .distribution.cooldown import CooldownsView
from bot.views.settings._view import DefaultSettingsView

from bot.resources.ether import Emoji
from bot.databases import GuildDateBases, CommandDB
from bot.languages import help as help_info, i18n
from bot.languages.help import get_command


class DropDown(nextcord.ui.StringSelect):
    def __init__(self, guild_id, command_name) -> None:
        self.command_name = command_name

        options = [
            nextcord.SelectOption(
                label='Channel', emoji=Emoji.channel_text, value='channel'
            ),
            nextcord.SelectOption(
                label='Role', emoji=Emoji.auto_role, value='role'
            ),
            nextcord.SelectOption(
                label='Cooldown', emoji=Emoji.cooldown, value='cooldown'
            ),
        ]

        super().__init__(options=options)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]

        objections = {
            'channel': ChannelsView,
            'role': RolesView,
            'cooldown': CooldownsView
        }
        classification = objections.get(value)
        view = classification(
            interaction.guild,
            self.command_name
        )

        await interaction.response.edit_message(embed=view.embed, view=view)


class CommandData(DefaultSettingsView):
    embed: nextcord.Embed = None

    def __init__(self, guild: nextcord.Guild, command_name: str) -> None:
        self.command_name = command_name

        self.gdb = GuildDateBases(guild.id)
        color: int = self.gdb.get('color')
        locale: str = self.gdb.get('language')

        self.cdb = CommandDB(guild.id)
        self.command_data: dict = get_command(command_name)
        self.command_info: dict = self.cdb.get(command_name, {})

        self.operate = self.command_info.get("operate", 1)

        cat_emoji = help_info.categories_emoji[self.command_data.get(
            'category')]
        self.embed = nextcord.Embed(
            title=(
                f"{cat_emoji}"
                f"{self.command_data.get('name')}"
            ),
            description=self.command_data.get(
                'brief_descriptrion').get(locale),
            color=color
        )

        super().__init__()

        DDD = DropDown(guild.id, command_name)
        self.add_item(DDD)

        if self.command_data.get("allowed_disabled") is False:
            self.switcher.label = "Forbidden"
            self.switcher.style = nextcord.ButtonStyle.grey
            self.switcher.disabled = True
            DDD.disabled = True
        elif self.operate == 1:
            self.switcher.label = "Disable"
            self.switcher.style = nextcord.ButtonStyle.red
        elif self.operate == 0:
            self.switcher.label = "Enable"
            self.switcher.style = nextcord.ButtonStyle.green

        self.back.label = i18n.t(locale, 'settings.button.back')

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        cat_name = self.command_data.get('category')
        index = list(help_info.categories).index(cat_name)

        view = permisson_command.CommandsDataView(interaction.guild, index)

        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Switcher')
    async def switcher(self,
                       button: nextcord.ui.Button,
                       interaction: nextcord.Interaction):
        command_info = self.command_info
        desperate = 0 if self.operate == 1 else 1

        command_info['operate'] = desperate

        self.cdb.update(self.command_name, command_info)

        view = self.__class__(interaction.guild, self.command_name)

        await interaction.response.edit_message(embed=view.embed, view=view)
