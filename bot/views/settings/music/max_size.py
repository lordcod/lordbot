import nextcord
from bot.databases import GuildDateBases
from bot.languages import i18n
from .. import music
from .._view import DefaultSettingsView


class MaxSizeModal(nextcord.ui.Modal):
    def __init__(self, guild_id, value: int) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        super().__init__(i18n.t(locale, 'settings.music.max-queue-size.description'))
        self.size = nextcord.ui.TextInput(
            label=i18n.t(locale, 'settings.music.max-queue-size.name'),
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

        await interaction.response.edit_message(embed=view.embed, view=view)


class MaxSizeView(DefaultSettingsView):
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
        max_size = music_settings.get("queue-max-size", 150)

        modal = MaxSizeModal(interaction.guild_id, max_size)
        await interaction.response.send_modal(modal)
