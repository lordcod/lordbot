import nextcord


from .dj_roles import DjRolesView
from .volume import VolumeView
from .max_size import MaxSizeView

from bot.views import settings_menu
from bot.resources.ether import Emoji
from bot.views.settings._view import DefaultSettingsView
from bot.databases import GuildDateBases
from bot.languages import i18n


distribution = {
    "dj_roles": DjRolesView,
    "max_size": MaxSizeView,
    "volume": VolumeView
}


class MusicDropDown(nextcord.ui.StringSelect):
    def __init__(self, guild_id) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')

        options = [
            nextcord.SelectOption(
                label=i18n.t(locale, 'settings.music.dj-roles.name'),
                value="dj_roles",
                description=i18n.t(
                    locale, 'settings.music.dj-roles.description'),
                emoji=Emoji.music
            ),
            nextcord.SelectOption(
                label=i18n.t(locale, 'settings.music.max-queue-size.name'),
                value="max_size",
                description=i18n.t(
                    locale, 'settings.music.max-queue-size.description'),
                emoji=Emoji.playlist
            ),
            nextcord.SelectOption(
                label=i18n.t(locale, 'settings.music.default-volume.name'),
                value="volume",
                description=i18n.t(
                    locale, 'settings.music.default-volume.description'),
                emoji=Emoji.volume_up
            ),
        ]
        super().__init__(options=options)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        view = distribution[self.values[0]](interaction.guild)
        await interaction.response.edit_message(view=view)


class MusicView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        music_settings = gdb.get('music_settings')
        locale = gdb.get('language')
        color = gdb.get('color')

        description = ''

        if max_size := music_settings.get("queue-max-size"):
            description += i18n.t(locale,
                                  'settings.music.max-queue-size.value',
                                  size=max_size)
        if volume := music_settings.get("volume"):
            description += i18n.t(locale,
                                  'settings.music.default-volume.value',
                                  volume=volume)
        if dj_role_ids := music_settings.get("dj-roles"):
            dj_roles = filter(
                lambda item: item is not None,
                map(guild.get_role, dj_role_ids)
            )
            description += i18n.t(locale,
                                  'settings.music.dj-roles.value',
                                  roles=', '.join([role.mention for role in dj_roles]))

        self.embed = nextcord.Embed(
            title=i18n.t(locale,
                         'settings.music.title'),
            description=description,
            color=color
        )

        super().__init__()

        self.add_item(MusicDropDown(guild.id))

        self.back.label = i18n.t(locale, 'settings.button.back')

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = settings_menu.SettingsView(interaction.user)

        await interaction.response.edit_message(embed=view.embed, view=view)
