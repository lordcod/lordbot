import nextcord

from bot.languages import i18n
from bot.misc.utils import AsyncSterilization
from bot.views.information_dd import get_info_dd


from ... import ideas
from bot.views.settings._view import DefaultSettingsView

from bot.databases import GuildDateBases
from bot.databases.varstructs import IdeasPayload


@AsyncSterilization
class RolesDropDown(nextcord.ui.RoleSelect):
    async def __init__(
        self,
        guild: nextcord.Guild
    ) -> None:
        self.gdb = GuildDateBases(guild.id)
        locale = await self.gdb.get('language')

        super().__init__(
            placeholder=i18n.t(locale, 'settings.ideas.mod_role.dropdown'),
            min_values=1,
            max_values=15
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        locale = await self.gdb.get('language')

        for role in self.values.roles:
            if role.is_integration() or role.is_bot_managed():
                await interaction.response.send_message(
                    content=i18n.t(locale, 'settings.roles.error.integration', role=role.mention),
                    ephemeral=True
                )
                return
        else:
            await self.gdb.set_on_json('ideas', 'moderation_role_ids', self.values.ids)

            view = await ModerationRolesView(interaction.guild)
            await interaction.response.edit_message(embed=view.embed, view=view)


@AsyncSterilization
class ModerationRolesView(DefaultSettingsView):
    embed: nextcord.Embed = None

    async def __init__(self, guild: nextcord.Guild) -> None:
        self.gdb = GuildDateBases(guild.id)
        self.idea_data: IdeasPayload = await self.gdb.get('ideas')
        mod_role_ids = self.idea_data.get('moderation_role_ids')
        color = await self.gdb.get('color')
        locale = await self.gdb.get('language')

        self.embed = nextcord.Embed(
            title=i18n.t(locale, 'settings.ideas.init.title'),
            description=i18n.t(locale, 'settings.ideas.init.description'),
            color=color
        )
        self.embed.add_field(
            name='',
            value=i18n.t(locale, 'settings.ideas.mod_role.field')
        )

        super().__init__()

        if mod_role_ids:
            self.delete.disabled = False

            moderation_roles = filter(lambda item: item is not None,
                                      map(guild.get_role,
                                          mod_role_ids))
            if moderation_roles:
                self.add_item(get_info_dd(
                    placeholder=i18n.t(locale, 'settings.ideas.init.value.mod_roles',
                                       roles=', '.join([role.mention for role in moderation_roles]))
                ))
            else:
                self.add_item(get_info_dd(
                    placeholder=i18n.t(locale, 'settings.ideas.init.value.mod_roles',
                                       roles=i18n.t(locale, 'settings.ideas.init.unspecified'))
                ))
        else:
            self.add_item(get_info_dd(
                placeholder=i18n.t(locale, 'settings.ideas.init.value.mod_roles',
                                   roles=i18n.t(locale, 'settings.ideas.init.unspecified'))
            ))

        cdd = await RolesDropDown(guild)
        self.add_item(cdd)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = await ideas.IdeasView(interaction.guild)

        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, disabled=True)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.gdb.set_on_json('ideas', 'moderation_role_ids', [])

        view = await ModerationRolesView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
