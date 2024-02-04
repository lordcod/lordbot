import nextcord

from ..settings import DefaultSettingsView

from bot.databases.db import GuildDateBases
from bot.views import settings_menu
from bot.resources.info import DEFAULT_PREFIX
from bot.misc.utils import get_prefix
from bot.languages.settings import (
    prefix as prefix_langs,
    button as button_name
)


class Modal(nextcord.ui.Modal):
    def __init__(self, guild_id) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        prefix = get_prefix(guild_id, markdown=True)

        super().__init__(title=prefix_langs.title.get(locale, 'en'))

        self.prefix = nextcord.ui.TextInput(
            label=f'{prefix_langs.title.get(locale)}:',
            placeholder=prefix,
            max_length=3
        )
        self.add_item(self.prefix)

    async def callback(self, interaction: nextcord.Interaction):
        prefix = self.prefix.value
        gdb = GuildDateBases(interaction.guild_id)
        locale = gdb.get('language')
        gdb.set('prefix', prefix)

        view = PrefixView(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)


class PrefixView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        prefix = get_prefix(guild.id, markdown=False)
        color = gdb.get('color')
        locale = gdb.get('language')

        self.embed = nextcord.Embed(
            title=prefix_langs.title.get(locale),
            description=prefix_langs.description.get(locale),
            color=color
        )
        self.embed._fields = [
            {
                'name': f"{prefix_langs.current.get(locale)}: `{prefix}`",
                'value': ''
            }
        ]

        super().__init__()

        self.back.label = button_name.back.get(locale)
        self.edit.label = button_name.edit.get(locale)
        self.reset.label = button_name.reset.get(locale)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = settings_menu.SettingsView(interaction.user)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Edit', style=nextcord.ButtonStyle.blurple)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = Modal(interaction.guild_id)

        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label='Reset', style=nextcord.ButtonStyle.success)
    async def reset(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        prefix = DEFAULT_PREFIX

        gdb.set('prefix', prefix)

        view = PrefixView(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)
