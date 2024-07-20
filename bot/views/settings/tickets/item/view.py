import nextcord

from bot.databases.handlers.guildHD import GuildDateBases
from bot.databases.varstructs import TicketsPayload
from bot.misc.utils import AsyncSterilization
from bot.views.settings import tickets
from bot.views.settings._view import DefaultSettingsView


@AsyncSterilization
class TicketsItemView(DefaultSettingsView):
    embed = None

    async def __init__(self, guild: nextcord.Guild, message_id: int) -> None:
        gdb = GuildDateBases(guild.id)
        color = await gdb.get('color')
        tickets: TicketsPayload = await gdb.get('tickets', {})
        ticket_data = tickets[message_id]

        self.message_id = message_id
        self.ticket_data = ticket_data

        enabled = self.ticket_data.get('enabled')

        self.embed = nextcord.Embed(
            title='Tickets',
            color=color,
            description='The tickets module allows you to create and manage support requests, helping participants to easily open tickets, and administrators to effectively track and solve them.'
        )

        super().__init__()

        if enabled:
            self.switch.label = 'Disable'
            self.switch.style = nextcord.ButtonStyle.danger
        else:
            self.switch.label = 'Enable'
            self.switch.style = nextcord.ButtonStyle.success

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = await tickets.TicketsView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button()
    async def switch(self, button: nextcord.Button, interaction: nextcord.Interaction):
        self.ticket_data['enabled'] = not self.ticket_data.get('enabled')

        gdb = GuildDateBases(interaction.guild_id)
        await gdb.set_on_json('tickets', self.message_id, self.ticket_data)

        view = await TicketsItemView(interaction.guild, self.message_id)
        await interaction.response.edit_message(embed=view.embed, view=view)
