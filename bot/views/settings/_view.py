import nextcord
from nextcord.ext import commands

from bot.databases.handlers.guildHD import GuildDateBases
from bot.languages import i18n
commands.has_permissions


class DefaultSettingsView(nextcord.ui.View):
    permission: dict = {'manage_guild': True}

    async def interaction_check(
        self,
        interaction: nextcord.Interaction
    ) -> bool:
        permissions = interaction.guild.me.guild_permissions
        missing = [perm for perm, value in self.permission.items() if getattr(permissions, perm) != value]

        if missing:
            await interaction.response.defer()
            return False

        if not interaction.user.guild_permissions.manage_guild:
            gdb = GuildDateBases(interaction.guild_id)
            locale = await gdb.get('language')
            await interaction.response.send_message(
                i18n.t(locale, 'settings.permission.denied'),
                ephemeral=True
            )
            return False
        return True
