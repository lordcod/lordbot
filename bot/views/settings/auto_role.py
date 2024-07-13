import nextcord

from bot.misc.utils import AsyncSterilization

from bot.views.settings._view import DefaultSettingsView

from bot.views import settings_menu
from bot.databases import GuildDateBases
from bot.languages import i18n


@AsyncSterilization
class RolesDropDown(nextcord.ui.RoleSelect):
    async def __init__(
        self,
        guild: nextcord.Guild
    ) -> None:
        self.gdb = GuildDateBases(guild.id)
        locale = await self.gdb.get('language')

        super().__init__(
            placeholder=i18n.t(locale, 'settings.auto-role.placeholder'),
            min_values=1,
            max_values=25,
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        locale = await self.gdb.get('language')

        for role in self.values.roles:
            if role.is_default():
                await interaction.response.send_message(
                    content=i18n.t(locale, 'settings.roles.error.default'),
                    ephemeral=True
                )
            elif role.is_premium_subscriber():
                await interaction.response.send_message(
                    content=i18n.t(locale, 'settings.roles.error.premium', role=role.mention),
                    ephemeral=True
                )
            elif role.is_integration() or role.is_bot_managed():
                await interaction.response.send_message(
                    content=i18n.t(locale, 'settings.roles.error.integration', role=role.mention),
                    ephemeral=True
                )
            elif not role.is_assignable():
                await interaction.response.send_message(
                    content=i18n.t(locale, 'settings.roles.error.assignable', role=role.mention, bot_role=interaction.guild.self_role.mention),
                    ephemeral=True
                )
            else:
                continue
            break
        else:
            await self.gdb.set('auto_roles', self.values.ids)

            view = await AutoRoleView(interaction.guild)
            await interaction.response.edit_message(embed=view.embed, view=view)


@AsyncSterilization
class AutoRoleView(DefaultSettingsView):
    embed: nextcord.Embed

    async def __init__(self, guild: nextcord.Guild) -> None:
        self.gdb = GuildDateBases(guild.id)
        color = await self.gdb.get('color')
        locale = await self.gdb.get('language')
        roles_ids = await self.gdb.get('auto_roles')

        super().__init__()

        DDB = await RolesDropDown(guild)
        self.add_item(DDB)

        self.back.label = i18n.t(locale, 'settings.button.back')
        self.delete.label = i18n.t(locale, 'settings.auto-role.button.delete')

        self.embed = nextcord.Embed(
            title=i18n.t(locale, 'settings.auto-role.embed.title'),
            description=i18n.t(locale, 'settings.auto-role.embed.description'),
            color=color
        )

        if roles_ids:
            roles = filter(lambda item: item is not None,
                           [guild.get_role(role_id) for role_id in roles_ids])

            self.embed.add_field(
                name=i18n.t(locale, 'settings.auto-role.embed.field'),
                value=', '.join([role.mention for role in roles])
            )
        else:
            self.delete.disabled = True

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = await settings_menu.SettingsView(interaction.user)

        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Clear roles', style=nextcord.ButtonStyle.red)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.gdb.set('auto_roles', [])

        view = await AutoRoleView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
