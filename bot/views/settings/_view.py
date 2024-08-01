import nextcord

from bot.databases.handlers.guildHD import GuildDateBases
from bot.languages import i18n


class DefaultSettingsView(nextcord.ui.View):
    async def interaction_check(
        self,
        interaction: nextcord.Interaction
    ) -> bool:
        if not interaction.user.guild_permissions.manage_guild:
            gdb = GuildDateBases(interaction.guild_id)
            locale = await gdb.get('language')
            await interaction.response.send_message(
                i18n.t(locale, 'settings.permission.denied'),
                ephemeral=True
            )
            return False
        return True
