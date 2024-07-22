from typing import Dict, List
import nextcord

from bot.databases.handlers.guildHD import GuildDateBases
from bot.misc.utils import AsyncSterilization
from bot.views.settings.tickets.item.optns.faq import TicketFAQView
from bot.views.settings.tickets.item.optns.modals import TicketFormsView
from bot.views.settings.tickets.item.optns.moderation_roles import TicketModRolesView
from .optns.standart import OptionItem,  FunctionOptionItem, ViewOptionItem
from .optns.ticket_type import TicketTypeView

distribution: List[AsyncSterilization[OptionItem]] = [TicketTypeView, TicketFAQView, TicketFormsView, TicketModRolesView]
distribution_keys: Dict[str, AsyncSterilization[OptionItem]] = {item.cls.__name__.lower(): item for item in distribution}


@AsyncSterilization
class TicketsItemDropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild: nextcord.Guild, message_id: int):
        self.message_id = message_id

        gdb = GuildDateBases(guild.id)
        system_emoji = await gdb.get('system_emoji')

        self.items = {key: await item(guild, message_id) for key, item in distribution_keys.items()}
        super().__init__(options=[
            nextcord.SelectOption(
                label=item.label,
                value=key,
                description=item.description,
                emoji=item.get_emoji(system_emoji)
            )
            for key, item in self.items.items()
        ])

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        item = self.items[value]

        if isinstance(item, nextcord.ui.Modal):
            await interaction.response.send_modal(item)
        elif isinstance(item, ViewOptionItem):
            embed = await item.get_embed(interaction.guild)
            await interaction.response.edit_message(embed=embed, view=item)
        elif isinstance(item, FunctionOptionItem):
            await item.callback(interaction)
