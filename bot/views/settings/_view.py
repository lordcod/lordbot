import nextcord


class DefaultSettingsView(nextcord.ui.View):
    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message('You don\'t have the authority to use the settings', ephemeral=True)
            return False
        return True
