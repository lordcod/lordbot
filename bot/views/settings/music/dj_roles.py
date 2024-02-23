from typing import List, Optional
import nextcord
from bot.databases import GuildDateBases
from bot.resources.ether import Emoji
from .. import music
from .._view import DefaultSettingsView


class RolesDropDown(nextcord.ui.StringSelect):
    current_disabled = False

    def __init__(
        self,
        guild: nextcord.Guild,
        select_roles: List[int]
    ) -> None:
        self.gdb = GuildDateBases(guild.id)
        dj_roles = self.gdb.get('music_settings').get('dj-roles', [])

        options = []

        for role in guild.roles:
            if (
                role.is_default() or
                role.is_premium_subscriber() or
                role.is_integration() or
                role.is_bot_managed()
            ):
                continue

            opt = nextcord.SelectOption(
                label=role.name,
                value=role.id,
                emoji=Emoji.frame_person,
                default=(
                    role.id in dj_roles or
                    role.id in select_roles
                )
            )

            options.append(opt)

        options = options[:25]

        if 0 >= len(options):
            options.append(
                nextcord.SelectOption(
                    label="-"
                )
            )
            self.current_disabled = True

        super().__init__(
            placeholder="Select roles that can interact with music.",
            min_values=1,
            max_values=len(options),
            options=options,
            disabled=self.current_disabled
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        view = DjRolesView(
            interaction.guild,
            list(map(int, self.values))
        )
        await interaction.message.edit(embed=view.embed, view=view)


class DjRolesView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(
        self,
        guild: nextcord.Guild,
        select_roles: Optional[List[int]] = None
    ) -> None:
        self.embed = music.MusicView(guild).embed
        self.select_roles = select_roles
        self.gdb = GuildDateBases(guild.id)
        music_settings = self.gdb.get("music_settings")

        super().__init__()
        rdp = RolesDropDown(guild,
                            select_roles if select_roles else [])

        if select_roles is not None:
            self.install.disabled = False

        if music_settings.get('dj-roles') is None:
            self.enabled.disabled = False
            self.remove_item(self.install)
        else:
            self.remove_item(self.enabled)

        self.add_item(rdp)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = music.MusicView(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Enabled', style=nextcord.ButtonStyle.green,
                        disabled=True)
    async def enabled(self,
                      button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):

        music_settings = self.gdb.get("music_settings")
        music_settings['dj-roles'] = []
        self.gdb.set("music_settings", music_settings)

        view = self.__class__(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Install', style=nextcord.ButtonStyle.blurple,
                        disabled=True)
    async def install(self,
                      button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):

        music_settings = self.gdb.get("music_settings")
        music_settings['dj-roles'] = self.select_roles
        self.gdb.set("music_settings", music_settings)

        view = self.__class__(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)
