import nextcord
from bot.databases import GuildDateBases
from bot.languages import i18n
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
            await interaction.response.defer()
            music_settings = self.gdb.get("music_settings")
            music_settings['dj-roles'] = self.values.ids
            self.gdb.set("music_settings", music_settings)

        view = DjRolesView(interaction.guild)

        await interaction.response.edit_message(embed=view.embed, view=view)


class DjRolesView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(
        self,
        guild: nextcord.Guild
    ) -> None:
        self.embed = music.MusicView(guild).embed
        self.gdb = GuildDateBases(guild.id)
        music_settings = self.gdb.get("music_settings")

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
        view = music.MusicView(interaction.guild)

        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Enabled', style=nextcord.ButtonStyle.green)
    async def enabled(self,
                      button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):

        music_settings = self.gdb.get("music_settings")
        music_settings['dj-roles'] = []
        self.gdb.set("music_settings", music_settings)

        view = self.__class__(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Disabled', style=nextcord.ButtonStyle.red)
    async def disabled(self,
                       button: nextcord.ui.Button,
                       interaction: nextcord.Interaction):

        music_settings = self.gdb.get("music_settings")
        music_settings['dj-roles'] = None
        self.gdb.set("music_settings", music_settings)

        view = self.__class__(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
