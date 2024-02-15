import nextcord

from .dj_roles import DjRolesView
from .volume import VolumeView
from .max_size import MaxSizeView

from bot.views import settings_menu
from bot.resources.ether import Emoji
from bot.views.settings._view import DefaultSettingsView
from bot.databases.db import GuildDateBases
from bot.languages.settings import button as button_name


distribution = {
    "dj_roles": DjRolesView,
    "max_size": MaxSizeView,
    "volume": VolumeView
}


class MusicDropDown(nextcord.ui.StringSelect):
    def __init__(self) -> None:
        options = [
            nextcord.SelectOption(
                label="Dj-roles",
                value="dj_roles",
                description="Roles that can control music.",
                emoji=Emoji.music
            ),
            nextcord.SelectOption(
                label="Max size",
                value="max_size",
                description="Maximum track queue length.",
                emoji=Emoji.playlist
            ),
            nextcord.SelectOption(
                label="Default volume",
                value="volume",
                description="The default music volume.",
                emoji=Emoji.volume_up
            ),
        ]
        super().__init__(options=options)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        view = distribution[self.values[0]](interaction.guild)
        await interaction.message.edit(view=view)


class MusicView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        music_settings = gdb.get('music_settings')
        locale = gdb.get('language')
        color = gdb.get('color')

        description = ''

        if max_size := music_settings.get("queue-max-size"):
            description += f"Maximum queue size: {max_size}\n"
        if volume := music_settings.get("volume"):
            description += f"Default volume music: {volume}\n"
        if dj_role_ids := music_settings.get("dj-roles"):
            dj_roles = filter(
                lambda item: item is not None,
                map(guild.get_role, dj_role_ids)
            )
            description += f"Dj-roles: {', '.join([role.mention for role in dj_roles])}"

        self.embed = nextcord.Embed(
            title='Music',
            description=description,
            color=color
        )

        super().__init__()

        self.add_item(MusicDropDown())

        self.back.label = button_name.back.get(locale)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = settings_menu.SettingsView(interaction.user)

        await interaction.message.edit(embed=view.embed, view=view)
