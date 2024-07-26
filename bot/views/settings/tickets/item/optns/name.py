import nextcord

from bot.databases.handlers.guildHD import GuildDateBases
from bot.databases.varstructs import TicketsPayload
from bot.misc.utils import AsyncSterilization
from .standart import OptionItem


@AsyncSterilization
class TicketNameModal(nextcord.ui.Modal, OptionItem):
    label = 'Ticket name'
    description = 'Change the default ticket name when opening'

    async def __init__(self, guild: nextcord.Guild, message_id: int):
        self.message_id = message_id

        gdb = GuildDateBases(guild.id)
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[message_id]
        name = ticket_data.get('names').get('open')

        super().__init__('Tickets Name')

        self.name = nextcord.ui.TextInput(
            label='Name',
            placeholder=name,
            max_length=128
        )
        self.add_item(self.name)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[self.message_id]

        name = self.name.value
        ticket_data['names']['open'] = name

        await gdb.set_on_json('tickets', self.message_id, ticket_data)

        await self.update(interaction)
