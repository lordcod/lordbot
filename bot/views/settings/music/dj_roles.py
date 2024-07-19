import nextcord
from bot.databases import GuildDateBases
from bot.languages import i18n
from bot.misc.utils import AsyncSterilization

from .. import music
from .._view import DefaultSettingsView


class RolesDropDown(nextcord.ui.RoleSelect):
    def __init__(
        self,
        guild: nextcord.Guild
    ) -> None:
        self.gdb = GuildDateBases(guild.id)
        super().__init__(
            min_values=1,
            max_values=25
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        for role in self.values.roles:
            if role.is_integration() or role.is_bot_managed():
                locale = self.gdb.get('language')
                await interaction.response.send_message(
                    content=i18n.t(locale,
                                   'settings.music.dj-roles.failed',
                                   role=role.mention),
                    ephemeral=True
                )
                break
        else:
            await self.gdb.set_on_json('music_settings', 'dj-roles', self.values.ids)
            view = await DjRolesView(interaction.guild)
            await interaction.response.edit_message(embed=view.embed, view=view)


@AsyncSterilization
class DjRolesView(DefaultSettingsView):
    embed: nextcord.Embed

    async def __init__(
        self,
        guild: nextcord.Guild
    ) -> None:
        self.embed = music.MusicView(guild).embed
        self.gdb = GuildDateBases(guild.id)
        music_settings = await self.gdb.get("music_settings")
        locale = await self.gdb.get('language')
        color = await self.gdb.get('color')

        self.embed = nextcord.Embed(
            title=i18n.t(locale,
                         'settings.music.title'),
            description="The music module allows you to set the maximum queue length, control the volume, assign DJ roles and create playlists.",
            color=color
        )
        self.embed.add_field(
            name='',
            value='> Select the roles that will be able to add and change music'
        )

        super().__init__()

        rdp = RolesDropDown(guild)
        self.add_item(rdp)

        if music_settings.get('dj-roles') is None:
            rdp.disabled = True
            self.remove_item(self.disabled)
        else:
            self.remove_item(self.enabled)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = await music.MusicView(interaction.guild)

        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Enabled', style=nextcord.ButtonStyle.green)
    async def enabled(self,
                      button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):
        await self.gdb.set_on_json('music_settings', 'dj-roles', [])

        view = await DjRolesView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Disabled', style=nextcord.ButtonStyle.red)
    async def disabled(self,
                       button: nextcord.ui.Button,
                       interaction: nextcord.Interaction):
        await self.gdb.set_on_json('music_settings', 'dj-roles', None)

        view = await DjRolesView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
