from __future__ import annotations

from typing import TYPE_CHECKING
import nextcord

if TYPE_CHECKING:
    from bot.misc.tickettools import ModuleTicket


class CloseTicketView(nextcord.ui.View):
    def __init__(self,
                 ticket_module: ModuleTicket) -> None:
        self.ticket_module = ticket_module
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Close ticket", custom_id="ticket:close",
                        style=nextcord.ButtonStyle.red, emoji="🔒")
    async def close_ticket(self,
                           button: nextcord.ui.Button,
                           interaction: nextcord.Interaction):
        await interaction.response.defer()
        await self.ticket_module.close()
