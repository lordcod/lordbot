import nextcord

from bot.views.settings._view import DefaultSettingsView

from bot.resources.ether import Emoji
from bot.views import settings_menu
from bot.databases import GuildDateBases
from bot.languages import i18n

from typing import List


class RolesDropDown(nextcord.ui.StringSelect):
    current_disabled = False

    def __init__(
        self,
        guild: nextcord.Guild,
        select_roles: List[int]
    ) -> None:
        self.gdb = GuildDateBases(guild.id)
        locale = self.gdb.get('language')
        auto_roles = self.gdb.get('auto_roles')

        options = []

        for role in guild.roles:
            if (
                role.is_default() or
                role.is_premium_subscriber() or
                role.is_integration() or
                role.is_bot_managed() or
                role.position > guild.me.top_role.position
            ):
                continue

            opt = nextcord.SelectOption(
                label=role.name,
                value=role.id,
                emoji=Emoji.frame_person,
                default=(
                    role.id in auto_roles or
                    (select_roles is not None and role.id in select_roles)
                )
            )

            options.append(opt)

        options = options[:25]

        if 0 >= len(options):
            options.append(nextcord.SelectOption(
                label="-"
            ))
            self.current_disabled = True

        super().__init__(
            placeholder=i18n.t(locale, 'settings.auto-role.placeholder'),
            min_values=1,
            max_values=len(options),
            options=options,
            disabled=self.current_disabled
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        view = AutoRoleView(
            interaction.guild,
            list(map(int, self.values))
        )
        await interaction.message.edit(embed=view.embed, view=view)


class AutoRoleView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(self, guild: nextcord.Guild, select_roles: List[int] = None) -> None:
        self.gdb = GuildDateBases(guild.id)
        color = self.gdb.get('color')
        locale = self.gdb.get('language')
        roles_ids = self.gdb.get('auto_roles')

        super().__init__()

        DDB = RolesDropDown(guild, select_roles)

        self.add_item(DDB)

        self.back.label = i18n.t(locale, 'settings.button.back')
        self.install.label = i18n.t(
            locale, 'settings.auto-role.button.install')
        self.delete.label = i18n.t(locale, 'settings.auto-role.button.delete')

        self.embed = nextcord.Embed(
            title=i18n.t(locale, 'settings.auto-role.embed.title'),
            description=i18n.t(locale, 'settings.auto-role.embed.description'),
            color=color
        )

        if select_roles is not None:
            self.install.disabled = False
            self.roles = select_roles

            self.remove_item(self.delete)
        if roles_ids:
            self.delete.disabled = False

            self.remove_item(self.install)

            roles = filter(lambda item: item is not None,
                           [guild.get_role(role_id) for role_id in roles_ids])

            self.embed.add_field(
                name=i18n.t(locale, 'settings.auto-role.embed.field'),
                value=', '.join([role.mention for role in roles])
            )
        if select_roles is None and not roles_ids:
            self.remove_item(self.install)
            self.remove_item(self.delete)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = settings_menu.SettingsView(interaction.user)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Install roles', style=nextcord.ButtonStyle.blurple, disabled=True)
    async def install(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = self.gdb

        gdb.set('auto_roles', self.roles)

        view = self.__class__(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Delete roles', style=nextcord.ButtonStyle.red, disabled=True)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = self.gdb
        roles_ids = []

        gdb.set('auto_roles', roles_ids)

        view = self.__class__(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)
