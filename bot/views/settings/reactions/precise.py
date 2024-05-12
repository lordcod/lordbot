import nextcord

from bot.languages import i18n

from .modal import ModalBuilder
from .. import reactions
from .._view import DefaultSettingsView

from bot.databases import GuildDateBases


class ReactData(DefaultSettingsView):
    def __init__(self, channel, channel_data) -> None:
        self.gdb = GuildDateBases(channel.guild.id)
        locale = self.gdb.get('language')
        self.forum_message = self.gdb.get('reactions')

        self.channel_data = channel_data
        self.channel = channel
        super().__init__()

        self.back.label = i18n.t(
            locale, 'settings.button.back')
        self.edit_reactions.label = i18n.t(
            locale, 'settings.reactions.button.edit')
        self.delete_reactions.label = i18n.t(
            locale, 'settings.reactions.button.delete')

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = reactions.AutoReactions(interaction.guild)

        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Edit reaction',
                        style=nextcord.ButtonStyle.primary)
    async def edit_reactions(self,
                             button: nextcord.ui.Button,
                             interaction: nextcord.Interaction):
        modal = ModalBuilder(interaction.guild_id, self.channel.id)

        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label='Delete reaction',
                        style=nextcord.ButtonStyle.red)
    async def delete_reactions(self,
                               button: nextcord.ui.Button,
                               interaction: nextcord.Interaction):
        channel_id = self.channel.id
        del self.forum_message[channel_id]

        self.gdb.set('reactions', self.forum_message)

        view = reactions.AutoReactions(interaction.guild)

        await interaction.response.edit_message(embed=view.embed, view=view)
