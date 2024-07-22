from typing import List, Optional
import nextcord
from nextcord.utils import MISSING

from bot.databases.handlers.guildHD import GuildDateBases
from bot.databases.varstructs import TicketsPayload
from bot.misc.utils import AsyncSterilization

from .standart import ViewOptionItem


@AsyncSterilization
class TicketModRolesDropDown(nextcord.ui.RoleSelect):
    async def __init__(self, guild: nextcord.Guild) -> None:
        super().__init__(placeholder='Select moderator roles', max_values=25, row=0)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[self.view.message_id]
        ticket_data['moderation_roles'] = self.values.ids
        await gdb.set_on_json('tickets', self.view.message_id, ticket_data)

        view = await TicketModRolesView(interaction.guild, self.view.message_id)
        embed = await view.get_embed(interaction.guild)
        await interaction.response.edit_message(embed=embed, view=view)


@AsyncSterilization
class TicketModRolesView(ViewOptionItem):
    label = 'Ticket Moderation Roles'
    description = 'Assign moderators to automatically add to all applications.'

    async def __init__(self, guild: nextcord.Guild, message_id: int):
        self.message_id = message_id

        self.edit_row_back(1)

        super().__init__()

        tmrdd = await TicketModRolesDropDown(guild)
        self.add_item(tmrdd)

    @nextcord.ui.button(label='Clear', style=nextcord.ButtonStyle.red, disabled=True, row=1)
    async def clear(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[self.message_id]
        ticket_data['moderation_roles'] = []
        await gdb.set_on_json('tickets', self.message_id, ticket_data)

        view = await TicketModRolesView(interaction.guild, self.message_id)
        embed = await view.get_embed(interaction.guild)
        await interaction.response.edit_message(embed=embed, view=view)
