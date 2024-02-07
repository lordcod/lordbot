import nextcord

from bot.databases.db import GuildDateBases


class MaxVolumeModal(nextcord.ui.Modal):
    def __init__(self) -> None:
        super().__init__("Max volume")

        self.volume = nextcord.ui.TextInput(
            label="Max volume",
            placeholder="0 - 100"
        )

        self.add_item(self.content)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        music_settings = gdb.get('music_settings')

        volume = self.volume.value

        if not (volume.isdigit() and 100 >= volume >= 0):
            await interaction.response.send_message("Not valid!")

        music_settings['volume'] = int(volume)

        gdb.set('music_settings', music_settings)

        await interaction.response.send_message(f"New default volume - {volume}")
