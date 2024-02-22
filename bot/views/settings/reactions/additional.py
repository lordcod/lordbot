import nextcord


from .modal import ModalBuilder
from .. import reactions
from .._view import DefaultSettingsView

from bot.databases.db import GuildDateBases
from bot.languages import i18n


class DropDownBuilder(nextcord.ui.ChannelSelect):
    def __init__(self, guild_id) -> None:
        self.gdb = GuildDateBases(guild_id)
        locale = self.gdb.get('language')

        super().__init__(
            placeholder=i18n.t(
                locale, 'settings.reactions.addres.placeholder'),
            channel_types=[nextcord.ChannelType.news,
                           nextcord.ChannelType.text]
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel: nextcord.TextChannel = self.values[0]
        reacts: dict = self.gdb.get('reactions')
        locale: str = self.gdb.get('language')

        if channel.id in reacts:
            await interaction.response.send_message(i18n.t(
                locale, 'settings.reactions.addres.channel-error'),
                ephemeral=True)
            return

        view = InstallEmojiView(channel.guild.id, channel.id)

        await interaction.message.edit(view=view)


class InstallEmojiView(DefaultSettingsView):
    def __init__(self, guild_id: int, channel_id: int = None) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')

        super().__init__()

        if channel_id is not None:
            self.channel_id = channel_id
            self.install.disabled = False

        self.back.label = i18n.t(locale, 'settings.button.back')
        self.install.label = i18n.t(
            locale, 'settings.reactions.addres.install-emoji')

        DDB = DropDownBuilder(guild_id)

        self.add_item(DDB)

    @nextcord.ui.button(label='Back',
                        style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = reactions.AutoReactions(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Install emoji',
                        style=nextcord.ButtonStyle.blurple,
                        disabled=True)
    async def install(self,
                      button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):
        modal = ModalBuilder(interaction.guild_id, self.channel_id)

        await interaction.response.send_modal(modal)
