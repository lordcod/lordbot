import nextcord
from bot.databases import GuildDateBases
from bot.misc import utils
from .. import music
from .._view import DefaultSettingsView

from bot.languages import i18n


class VolumeModal(nextcord.ui.Modal):
    def __init__(self, guild_id: int, value: int) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')

        super().__init__(i18n.t(
            locale, 'settings.music.default-volume.description'))
        self.volume = nextcord.ui.TextInput(
            label=i18n.t(
                locale, 'settings.music.default-volume.name'),
            placeholder=value,
            max_length=3
        )
        self.add_item(self.volume)

    async def callback(self, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        music_settings = gdb.get('music_settings')
        volume = self.volume.value

        if not volume.isdigit():
            return

        music_settings['volume'] = utils.clamp(int(volume), 0, 100)

        gdb.set('music_settings', music_settings)

        view = VolumeView(interaction.guild)

        await interaction.response.edit_message(embed=view.embed, view=view)


class VolumeView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(self, guild: nextcord.Guild) -> None:
        self.embed = music.MusicView(guild).embed
        self.gdb = GuildDateBases(guild.id)
        locale = self.gdb.get('language')

        super().__init__()

        self.back.label = i18n.t(locale, 'settings.button.back')
        self.edit.label = i18n.t(locale, 'settings.button.edit')

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = music.MusicView(interaction.guild)

        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Edit', style=nextcord.ButtonStyle.blurple)
    async def edit(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        music_settings = self.gdb.get("music_settings")
        volume = music_settings.get("volume", 70)

        modal = VolumeModal(volume)
        await interaction.response.send_modal(modal)
