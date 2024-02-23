import nextcord


from .modal import ModalBuilder
from .. import thread_message
from .._view import DefaultSettingsView

from bot.misc import utils
from bot.languages import i18n
from bot.databases import GuildDateBases


class ThreadData(DefaultSettingsView):
    def __init__(self, channel: nextcord.abc.GuildChannel, channel_data) -> None:
        self.channel_data = channel_data
        self.channel = channel

        self.gdb = GuildDateBases(channel.guild.id)
        self.forum_message = self.gdb.get('thread_messages')
        locale = self.gdb.get('language')

        super().__init__()

        self.back.label = i18n.t(
            locale, 'settings.button.back')
        self.message.label = i18n.t(
            locale, 'settings.thread.thread.button.view')
        self.edit_message.label = i18n.t(
            locale, 'settings.thread.thread.button.edit')
        self.delete_message.label = i18n.t(
            locale, 'settings.thread.thread.button.delete')

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = thread_message.AutoThreadMessage(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Message', style=nextcord.ButtonStyle.success)
    async def message(self,
                      button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):
        channel_content = self.channel_data

        gdb = GuildDateBases(interaction.guild_id)
        locale = gdb.get('language')

        if not channel_content:
            await interaction.response.send_message(i18n.t(
                locale, 'settings.thread.thread.mes-not-found'))

        content = await utils.generate_message(channel_content)
        await interaction.response.send_message(**content, ephemeral=True)

    @nextcord.ui.button(label='Edit message',
                        style=nextcord.ButtonStyle.primary)
    async def edit_message(self,
                           button: nextcord.ui.Button,
                           interaction: nextcord.Interaction):
        modal = ModalBuilder(interaction.guild_id, self.channel.id)

        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label='Delete message', style=nextcord.ButtonStyle.red)
    async def delete_message(self,
                             button: nextcord.ui.Button,
                             interaction: nextcord.Interaction):
        channel_id = self.channel.id
        del self.forum_message[channel_id]

        self.gdb.set('thread_messages', self.forum_message)

        view = thread_message.AutoThreadMessage(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)
