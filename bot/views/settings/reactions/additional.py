import nextcord

from .modal import ModalBuilder
from .. import reactions
from ...settings import DefaultSettingsView

from bot.databases.db import GuildDateBases
from bot.languages.settings import (
    reactions as reaction_langs,
    button as button_name
)


class DropDownBuilder(nextcord.ui.ChannelSelect):
    def __init__(self, guild_id) -> None:
        self.gdb = GuildDateBases(guild_id)
        locale = self.gdb.get('language')

        super().__init__(
            placeholder=reaction_langs.addres.ph.get(locale),
            channel_types=[nextcord.ChannelType.news,
                           nextcord.ChannelType.text]
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel: nextcord.TextChannel = self.values[0]
        reacts: dict = self.gdb.get('reactions')
        locale: str = self.gdb.get('language')

        if channel.id in reacts:
            await interaction.response.send_message(reaction_langs.addres.channel_error.get(locale), ephemeral=True)
            return

        view = ViewBuilder(channel.guild.id, channel.id)

        view.install.disabled = False

        await interaction.message.edit(view=view)


class ViewBuilder(DefaultSettingsView):
    def __init__(self, guild_id: int, installer=None) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')

        self.installer = installer

        super().__init__()

        self.back.label = button_name.back.get(locale)
        self.install.label = reaction_langs.addres.install_emoji.get(locale)

        DDB = DropDownBuilder(guild_id)

        self.add_item(DDB)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = reactions.AutoReactions(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Install emoji', style=nextcord.ButtonStyle.blurple, disabled=True)
    async def install(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = ModalBuilder(interaction.guild_id, self.installer)

        await interaction.response.send_modal(modal)
