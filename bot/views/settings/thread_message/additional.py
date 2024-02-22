import nextcord

from bot.languages import i18n

from .modal import ModalBuilder
from .. import thread_message
from .._view import DefaultSettingsView

from bot.databases.db import GuildDateBases
from bot.languages.settings import (
    thread as thread_langs,
    button as button_name
)


class ChannelDropDown(nextcord.ui.ChannelSelect):
    def __init__(self, guild_id) -> None:
        self.gdb = GuildDateBases(guild_id)
        locale = self.gdb.get('language')
        super().__init__(
            placeholder=i18n.t(
                locale, 'settings.thread.addptional.placeholder'),
            channel_types=[nextcord.ChannelType.forum,
                           nextcord.ChannelType.text]
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel: nextcord.TextChannel = self.values[0]
        locale = self.gdb.get('language')
        forum_message = self.gdb.get('thread_messages')

        if channel.id in forum_message:
            await interaction.response.send_message(i18n.t(
                locale, 'settings.thread.addptional.channel-error'))
            return

        view = InstallThreadView(channel.guild.id, channel.id)

        view.install.disabled = False

        await interaction.message.edit(view=view)


class InstallThreadView(DefaultSettingsView):
    def __init__(self, guild_id, installer=None) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        self.installer = installer

        super().__init__()

        self.back.label = button_name.back.get(locale)
        self.install.label = i18n.t(
            locale, 'settings.thread.addptional.button.install-mes')

        DDB = ChannelDropDown(guild_id)

        self.add_item(DDB)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = thread_message.AutoThreadMessage(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Install message',
                        style=nextcord.ButtonStyle.blurple,
                        disabled=True)
    async def install(self,
                      button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):
        modal = ModalBuilder(interaction.guild_id, self.installer)

        await interaction.response.send_modal(modal)
