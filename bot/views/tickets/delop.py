from __future__ import annotations

from typing import TYPE_CHECKING
import nextcord

if TYPE_CHECKING:
    from bot.misc.tickettools import ModuleTicket


class DelopTicketView(nextcord.ui.View):
    def __init__(self,
                 ticket_module: ModuleTicket) -> None:
        self.ticket_module = ticket_module
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Delete ticket", custom_id="ticket:delete",
                        style=nextcord.ButtonStyle.red, emoji="⛔")
    async def delete_ticket(self,
                            button: nextcord.ui.Button,
                            interaction: nextcord.Interaction):
        await interaction.response.defer()
        await self.ticket_module.delete()

    @nextcord.ui.button(label="Reopen ticket", custom_id="ticket:reopen",
                        style=nextcord.ButtonStyle.blurple, emoji="🔓")
    async def reopen_ticket(self,
                            button: nextcord.ui.Button,
                            interaction: nextcord.Interaction):
        await interaction.response.defer()
        await self.ticket_module.reopen()
