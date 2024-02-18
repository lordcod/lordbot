import jmespath
import nextcord
from bot import languages
from bot.views import settings_menu
from ._view import DefaultSettingsView
from bot.databases.db import GuildDateBases
from nextcord.utils import find
from bot.languages.settings import (
    languages as languages_trans,
    button as button_name
)


class DropDown(nextcord.ui.Select):
    def __init__(self, guild_id):
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')

        options = [
            nextcord.SelectOption(
                label=(f"{data.get('english_name')} "
                       f"({data.get('native_name')})"),
                value=data.get('locale'),
                emoji=data.get('flag', None),
                default=locale == data.get('locale')
            )
            for data in languages.current[:25]
        ]

        super().__init__(
            placeholder=languages_trans.choose.get(locale),
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        gdb = GuildDateBases(interaction.guild_id)

        gdb.set('language', value)

        view = Languages(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)


class Languages(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        color = gdb.get('color')
        locale = gdb.get('language')

        self.embed = nextcord.Embed(
            title=languages_trans.title.get(locale),
            description=languages_trans.description.get(locale),
            color=color
        )

        super().__init__()

        self.back.label = button_name.back.get(locale)

        lang = DropDown(guild.id)

        self.add_item(lang)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = settings_menu.SettingsView(interaction.user)

        await interaction.message.edit(embed=view.embed, view=view)
