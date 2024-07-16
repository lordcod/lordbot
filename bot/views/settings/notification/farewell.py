import nextcord

from bot.databases.handlers.guildHD import GuildDateBases
from bot.languages import i18n
from bot.misc.utils import AsyncSterilization
from bot.views.settings import notification
from bot.views.settings._view import DefaultSettingsView


@AsyncSterilization
class FarewellView(DefaultSettingsView):
    embed = None

    async def __init__(self, guild: nextcord.Guild):
        self.gdb = GuildDateBases(guild.id)
        locale = await self.gdb.get('language')

        super().__init__()

        self.back.label = i18n.t(locale, 'settings.button.back')

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = await notification.NotificationView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
