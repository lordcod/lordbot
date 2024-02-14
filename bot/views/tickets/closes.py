import nextcord


class CloseTicketView(nextcord.ui.View):
    def __init__(self,
                 ticket_module) -> None:
        self.ticket_module = ticket_module
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Close ticket", custom_id="ticket:close",
                        style=nextcord.ButtonStyle.red, emoji="🔒")
    async def close_ticket(self,
                           button: nextcord.ui.Button,
                           interaction: nextcord.Interaction):
        await interaction.response.defer()
        await self.ticket_module.close()
