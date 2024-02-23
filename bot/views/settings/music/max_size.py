import nextcord
from bot.databases import GuildDateBases
from .. import music
from .._view import DefaultSettingsView


class MaxSizeModal(nextcord.ui.Modal):
    def __init__(self, value: int) -> None:
        super().__init__("Maximum queue size")
        self.size = nextcord.ui.TextInput(
            label="Max size:",
            placeholder=value,
            max_length=3
        )
        self.add_item(self.size)

    async def callback(self, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        music_settings = gdb.get('music_settings')
        max_size = self.size.value

        if not max_size.isdigit():
            return

        music_settings['queue-max-size'] = int(max_size)

        gdb.set('music_settings', music_settings)

        view = MaxSizeView(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)


class MaxSizeView(DefaultSettingsView):
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
        max_size = music_settings.get("queue-max-size", 150)

        modal = MaxSizeModal(max_size)
        await interaction.response.send_modal(modal)
