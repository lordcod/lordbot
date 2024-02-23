import nextcord
from bot.databases import GuildDateBases
from bot.misc import utils
from .. import music
from .._view import DefaultSettingsView


class VolumeModal(nextcord.ui.Modal):
    def __init__(self, value: int) -> None:
        super().__init__("Default volume music")
        self.volume = nextcord.ui.TextInput(
            label="Volume:",
            placeholder=value,
            max_length=3
        )
        self.add_item(self.size)

    async def callback(self, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        music_settings = gdb.get('music_settings')
        volume = self.volume.value

        if not volume.isdigit():
            return

        music_settings['volume'] = utils.clamp(int(volume), 0, 100)

        gdb.set('music_settings', music_settings)

        view = VolumeView(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)


class VolumeView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(self, guild: nextcord.Guild) -> None:
        self.embed = music.MusicView(guild).embed
        self.gdb = GuildDateBases(guild.id)

        super().__init__()

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = music.MusicView(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Install', style=nextcord.ButtonStyle.blurple)
    async def install(self,
                      button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):
        music_settings = self.gdb.get("music_settings")
        volume = music_settings.get("volume", 70)

        modal = VolumeModal(volume)
        await interaction.response.send_modal(modal)
