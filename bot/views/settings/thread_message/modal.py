import nextcord

from bot.languages import i18n

from .. import thread_message

from bot.databases import GuildDateBases


class ModalBuilder(nextcord.ui.Modal):
    def __init__(self, guild_id, channel_id) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        self.channel_id = channel_id
        super().__init__(i18n.t(
            locale, 'settings.thread.modal.title'))

        self.content = nextcord.ui.TextInput(
            label=i18n.t(
                locale, 'settings.thread.modal.label'),
            placeholder=i18n.t(
                locale, 'settings.thread.modal.placeholder')
        )

        self.add_item(self.content)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        forum_message = gdb.get('thread_messages')

        content = self.content.value
        channel_id = self.channel_id

        forum_message[channel_id] = content

        gdb.set('thread_messages', forum_message)

        view = thread_message.AutoThreadMessage(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)
