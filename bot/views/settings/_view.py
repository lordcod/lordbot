from typing import Dict
import nextcord

from bot.databases.handlers.guildHD import GuildDateBases
from bot.languages import i18n
from bot.misc.utils import AsyncSterilization


def has_permissions(**kwargs):
    def wrapped(cls: AsyncSterilization['DefaultSettingsView'] | type['DefaultSettingsView']):
        if isinstance(cls, AsyncSterilization):
            cls.cls.permission = kwargs
        else:
            cls.permission = kwargs
        return cls
    return wrapped


@has_permissions(manage_guild=True)
class DefaultSettingsView(nextcord.ui.View):
    permission: Dict[str, bool]

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
