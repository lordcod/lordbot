import nextcord

from ._view import DefaultSettingsView

from bot.databases import GuildDateBases
from bot.views import settings_menu
from bot.resources.info import DEFAULT_PREFIX
from bot.languages import i18n


class Modal(nextcord.ui.Modal):
    def __init__(self, guild_id) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        prefix = gdb.get('prefix')

        super().__init__(title=i18n.t(locale, 'settings.prefix.title'))

        self.prefix = nextcord.ui.TextInput(
            label=f"{i18n.t(locale, 'settings.prefix.title')}:",
            placeholder=prefix,
            max_length=3
        )
        self.add_item(self.prefix)

    async def callback(self, interaction: nextcord.Interaction):
        prefix = self.prefix.value
        gdb = GuildDateBases(interaction.guild_id)
        gdb.set('prefix', prefix)

        view = PrefixView(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)


class PrefixView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        prefix = gdb.get('prefix')

        color = gdb.get('color')
        locale = gdb.get('language')

        self.embed = nextcord.Embed(
            title=i18n.t(locale, 'settings.prefix.title'),
            description=i18n.t(locale, 'settings.prefix.description'),
            color=color
        )
        self.embed._fields = [
            {
                'name': i18n.t(locale, 'settings.prefix.current', prefix=prefix),
                'value': ''
            }
        ]

        super().__init__()

        self.back.label = i18n.t(locale, 'settings.button.back')
        self.edit.label = i18n.t(locale, 'settings.button.edit')
        self.reset.label = i18n.t(locale, 'settings.button.reset')

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = settings_menu.SettingsView(interaction.user)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Edit', style=nextcord.ButtonStyle.blurple)
    async def edit(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        modal = Modal(interaction.guild_id)

        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label='Reset', style=nextcord.ButtonStyle.success)
    async def reset(self,
                    button: nextcord.ui.Button,
                    interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        gdb.set('prefix', DEFAULT_PREFIX)

        view = PrefixView(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)
