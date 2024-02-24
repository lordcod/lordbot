import nextcord

from bot.views.settings._view import DefaultSettingsView

from bot.views import settings_menu
from bot.databases import GuildDateBases
from bot.languages import i18n


class RolesDropDown(nextcord.ui.RoleSelect):
    def __init__(
        self,
        guild: nextcord.Guild
    ) -> None:
        self.gdb = GuildDateBases(guild.id)
        locale = self.gdb.get('language')

        super().__init__(
            placeholder=i18n.t(locale, 'settings.auto-role.placeholder'),
            min_values=1,
            max_values=15,
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        for role in self.values.roles:
            if role.is_default():
                await interaction.response.send_message(
                    content=f"The {role.mention} role is the default role for all users and can't be selected.",
                    ephemeral=True
                )
            elif role.is_premium_subscriber():
                await interaction.response.send_message(
                    content=f"The {role.mention} role is a role that is used by subscribers of your server.",
                    ephemeral=True
                )
            elif role.is_integration() or role.is_bot_managed():
                await interaction.response.send_message(
                    content=f"The {role.mention} role cannot be assigned and is used for integration or by a bot.",
                    ephemeral=True
                )
            elif role.position >= interaction.guild.me.top_role.position:
                await interaction.response.send_message(
                    content=f"The bot will not be able to assign the role {role.mention}, as that role is lower than the bot's. To resolve this issue, please move the role {interaction.guild.self_role.mention} to a higher position than {role.mention}.",
                    ephemeral=True
                )
            else:
                continue
            break
        else:
            await interaction.response.defer()
            self.gdb.set('auto_roles', self.values.ids)

        view = AutoRoleView(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)


class AutoRoleView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(self, guild: nextcord.Guild) -> None:
        self.gdb = GuildDateBases(guild.id)
        color = self.gdb.get('color')
        locale = self.gdb.get('language')
        roles_ids = self.gdb.get('auto_roles')

        super().__init__()

        DDB = RolesDropDown(guild)

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
        view = settings_menu.SettingsView(interaction.user)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Clear roles', style=nextcord.ButtonStyle.red)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.gdb.set('auto_roles', [])

        view = self.__class__(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)
