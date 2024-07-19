import nextcord

from bot.databases.handlers.guildHD import GuildDateBases
from bot.misc.utils import AsyncSterilization
from bot.views.settings.tempvoice.optns.standart import OptionItem


@AsyncSterilization
class NameModal(nextcord.ui.Modal, OptionItem):
    label = 'Channel name'
    description = 'Change the default channel name'
    emoji = 'name'

    async def __init__(self, guild: nextcord.Guild):
        gdb = GuildDateBases(guild.id)
        data = await gdb.get('tempvoice')
        name = data.get('name', '{voice.count.active}-{member.username}')

        super().__init__('TempVoice')

        self.name = nextcord.ui.TextInput(
            label='Voice Name',
            placeholder=name
        )
        self.add_item(self.name)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        name = self.name.value
        await gdb.set_on_json('tempvoice', 'channel_name', name)

        await self.update(interaction)
