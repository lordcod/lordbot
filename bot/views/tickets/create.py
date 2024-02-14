import nextcord


class CreateTicketView(nextcord.ui.View):
    def __init__(self,
                 ticket_module) -> None:
        self.ticket_module = ticket_module
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Create ticket", custom_id="ticket:create",
                        style=nextcord.ButtonStyle.red, emoji="📕")
    async def create_ticket(self,
                            button: nextcord.ui.Button,
                            interaction: nextcord.Interaction):
        await interaction.response.defer()
        await self.ticket_module.create(interaction.user)
