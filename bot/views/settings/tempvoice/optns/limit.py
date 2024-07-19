import nextcord

from bot.databases.handlers.guildHD import GuildDateBases
from bot.misc.utils import AsyncSterilization
from .standart import OptionItem


@AsyncSterilization
class LimitModal(nextcord.ui.Modal, OptionItem):
    label = 'Channel limit'
    description = 'Change the default channel limit'
    emoji = 'limit'

    async def __init__(self, guild: nextcord.Guild):
        gdb = GuildDateBases(guild.id)
        data = await gdb.get('tempvoice')
        limit = data.get('limit', 4)

        super().__init__('TempVoice')

        self.limit = nextcord.ui.TextInput(
            label='Voice Limit',
            placeholder=limit
        )
        self.add_item(self.limit)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        limit = self.limit.value
        await gdb.set_on_json('tempvoice', 'channel_limit', limit)

        await self.update(interaction)
