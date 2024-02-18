import nextcord


class DelopTicketView(nextcord.ui.View):
    def __init__(self,
                 ticket_module) -> None:
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
