import nextcord

from bot.views.settings._view import DefaultSettingsView

from bot.views import settings_menu
from bot.databases.db import GuildDateBases
from bot.languages.settings import button as button_name


class MusicView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        locale = gdb.get('language')
        color = gdb.get('color')

        self.embed = nextcord.Embed(
            title='Music',
            description='Voice desc',
            color=color
        )

        super().__init__()

        self.back.label = button_name.back.get(locale)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = settings_menu.SettingsView(interaction.user)

        await interaction.message.edit(embed=view.embed, view=view)
