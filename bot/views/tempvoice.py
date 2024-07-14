from __future__ import annotations
from discord import Interaction
import nextcord

from bot.databases import GuildDateBases, localdb
from bot.languages import i18n

from typing import List, TYPE_CHECKING

from bot.misc.tempvoice import VoiceStatus
from bot.misc.utils import AsyncSterilization

from bot.resources.ether import Emoji


async def get_voice(self, interaction: nextcord.Interaction) -> None:
    channels_tracks_db = await localdb.get_table('channels_track_data')
    channels_data = await localdb.get_table('channels_data')
    channels_track_data = await channels_tracks_db.get(interaction.guild.id, [])

    for cid in channels_track_data:
        voice_data = await channels_data.get(cid)
        owner_id = voice_data['owner_id']
        status = voice_data['status']
        if interaction.id == owner_id and status == VoiceStatus.opened:
            return interaction.guild.get_channel(cid)
    return None


class OwnerSettingsDropDown(nextcord.ui.UserSelect):
    def __init__(self, locale: str) -> None:
        super().__init__(placeholder='Выберете участника которому хотите передать канал.')

    def get_view(self):
        view = nextcord.ui.View(timeout=300)
        view.add_item(self)
        return view

    async def callback(self, interaction: nextcord.Interaction) -> None:
        return await super().callback(interaction)


@AsyncSterilization
class TempVoiceView(nextcord.ui.View):
    embed: nextcord.Embed

    async def __init__(self) -> None:
        super().__init__(timeout=None)

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        voice = await get_voice(interaction)
        if voice is None:
            await interaction.response.send_message("I didn't find the private room you opened.")
            return False
        return True

    @nextcord.ui.button(emoji='👑')
    async def change_owner(self, button: nextcord.Button, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        locale = await gdb.get('language')
        view = OwnerSettingsDropDown(locale).get_view()
        await interaction.response.send_message(view=view, ephemeral=True)
