import nextcord

from .modal import ModalBuilder
from .. import thread_message
from .._view import DefaultSettingsView

from bot.databases.db import GuildDateBases
from bot.languages.settings import (
    thread as thread_langs,
    button as button_name
)


class DropDownBuilder(nextcord.ui.ChannelSelect):
    def __init__(self, guild_id) -> None:
        self.gdb = GuildDateBases(guild_id)
        locale = self.gdb.get('language')
        super().__init__(
            placeholder=thread_langs.addptional.placeholder.get(locale),
            channel_types=[nextcord.ChannelType.forum,
                           nextcord.ChannelType.text]
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel: nextcord.TextChannel = self.values[0]
        locale = self.gdb.get('language')
        forum_message = self.gdb.get('thread_messages')

        if channel.id in forum_message:
            await interaction.response.send_message(
                thread_langs.addptional.channel_error.get(locale))
            return

        view = ViewBuilder(channel.guild.id, channel.id)

        view.install.disabled = False

        await interaction.message.edit(view=view)


class ViewBuilder(DefaultSettingsView):
    def __init__(self, guild_id, installer=None) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        self.installer = installer

        super().__init__()

        self.back.label = button_name.back.get(locale)
        self.install.label = thread_langs.addptional.install_mes.get(locale)

        DDB = DropDownBuilder(guild_id)

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
