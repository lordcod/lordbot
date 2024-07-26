import nextcord

from bot.databases.handlers.guildHD import GuildDateBases
from bot.databases.varstructs import TicketsPayload
from bot.misc.utils import AsyncSterilization
from bot.resources.ether import Emoji
from .standart import FunctionOptionItem


@AsyncSterilization
class ClosedUserFunction(FunctionOptionItem):
    label: str
    description: str

    async def __init__(self, guild: nextcord.Guild, message_id: int):
        self.message_id = message_id

        gdb = GuildDateBases(guild.id)
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[message_id]
        self.closed_user = ticket_data.get('user_closed', True)

        if self.closed_user:
            self.label = 'Disable closing by user'
            self.description = 'Click to prohibit users from closing the ticket.'
            self.emoji = Emoji.offline
        else:
            self.label = 'Enable closing by user'
            self.description = 'Click to allow users to close the ticket.'
            self.emoji = Emoji.online

    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild.id)
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[self.message_id]
        ticket_data['user_closed'] = not self.closed_user
        await gdb.set_on_json('tickets', self.message_id, ticket_data)

        await self.update(interaction)
