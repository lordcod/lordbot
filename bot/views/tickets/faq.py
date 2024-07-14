import nextcord
from bot.databases import GuildDateBases
from bot.databases.varstructs import TicketsButtonsPayload, TicketsItemPayload, TicketsPayload, FaqItemPayload
from bot.misc import utils
from bot.misc.utils import AsyncSterilization, generate_message, lord_format
from typing import List, Optional
from bot.resources.ether import Emoji
from bot.misc import tickettools
import datetime


def get_payload(member: nextcord.Member) -> dict:
    data = {
        'today_dt': datetime.datetime.today().isoformat()
    }
    data.update(utils.MemberPayload(member)._to_dict())
    data.update(utils.GuildPayload(member.guild)._to_dict())
    return data


@AsyncSterilization
class FAQDropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild_id: Optional[int] = None,
                       faq_items: List[FaqItemPayload] = [],
                       buttons: Optional[TicketsButtonsPayload] = None):
        if guild_id is None:
            super().__init__(custom_id='tickets:faq')
            return
        faq_placeholder = buttons.get('faq_placeholder')
        options = [
            nextcord.SelectOption(
                label=item['label'],
                value=i,
                description=item.get('description'),
                emoji=item.get('emoji'),
            )
            for i, item in enumerate(faq_items)
        ]
        super().__init__(
            custom_id='tickets:faq:dropdown:only',
            placeholder=faq_placeholder,
            options=options
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        tickets: TicketsPayload = await gdb.get('tickets', {})
        items = tickets.get(interaction.message.id).get('faq').get('items')
        response = items[int(self.values[0])]
        data = await generate_message(lord_format(response['response'], get_payload(interaction.user)))
        await interaction.response.send_message(**data, ephemeral=True)


@AsyncSterilization
class FAQTempDropDown(FAQDropDown.cls):
    async def __init__(self, guild_id: Optional[int] = None, faq_items: List[FaqItemPayload] = [], buttons: Optional[TicketsButtonsPayload] = None):
        await super().__init__(guild_id, faq_items, buttons=buttons)
        if guild_id is None:
            return
        self.faq_items = faq_items

    async def callback(self, interaction: nextcord.Interaction) -> None:
        response = self.faq_items[int(self.values[0])]
        data = await generate_message(lord_format(response['response'], get_payload(interaction.user)))
        await interaction.response.send_message(**data, ephemeral=True)


@AsyncSterilization
class FAQButtonOpen(nextcord.ui.Button):
    async def __init__(self, guild_id: Optional[int] = None, buttons: Optional[TicketsButtonsPayload] = None) -> None:
        if guild_id is None:
            super().__init__(custom_id='tickets:faq:view:faq')
            return
        faq_button = buttons.get('faq_button_open')
        super().__init__(
            style=faq_button.get('style'),
            label=faq_button.get('label'),
            custom_id='tickets:faq:view:faq',
            emoji=faq_button.get('emoji')
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        tickets: TicketsPayload = await gdb.get('tickets', {})
        items = tickets.get(interaction.message.id).get('faq').get('items')
        buttons = tickets.get(interaction.message.id)['buttons']

        view = nextcord.ui.View(timeout=300)
        view.add_item(await FAQTempDropDown(interaction.guild_id, items, buttons))
        await interaction.response.send_message(view=view, ephemeral=True)


@AsyncSterilization
class FAQCreateDropDown(FAQDropDown.cls):
    async def __init__(self, guild_id: Optional[int] = None, faq_items: List[FaqItemPayload] = [], buttons: Optional[TicketsButtonsPayload] = None):
        await super().__init__(guild_id, faq_items)
        self.custom_id = 'tickets:faq:dropdown:create'
        if guild_id is None:
            return
        faq_option = buttons.get('faq_option')
        self.append_option(nextcord.SelectOption(
            label=faq_option['label'],
            value='create_ticket',
            description=faq_option.get('description'),
            emoji=faq_option.get('emoji')
        ))

    async def callback(self, interaction: nextcord.Interaction) -> None:
        if self.values[0] != 'create_ticket':
            await super().callback(interaction)
            return
        await tickettools.ModuleTicket(interaction.user, interaction.message.id).create_after_faq(interaction)


@AsyncSterilization
class FAQButtonCreate(nextcord.ui.Button):
    async def __init__(self, guild_id: Optional[int] = None, buttons: Optional[TicketsButtonsPayload] = None) -> None:
        if guild_id is None:
            super().__init__(custom_id='tickets:faq:view:create')
            return
        faq_option = buttons.get('faq_button_create')
        super().__init__(
            style=faq_option.get('style'),
            label=faq_option.get('label'),
            custom_id='tickets:faq:view:create',
            emoji=faq_option.get('emoji')
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await tickettools.ModuleTicket(interaction.user, interaction.message.id).create_after_faq(interaction)


@AsyncSterilization
class FAQView(nextcord.ui.View):
    async def __init__(self, guild_id: Optional[int] = None, ticket_data: TicketsItemPayload = None):
        super().__init__(timeout=None)
        if guild_id is None:
            self.add_item(await FAQCreateDropDown())
            self.add_item(await FAQButtonOpen())
            self.add_item(await FAQButtonCreate())
            return

        buttons = ticket_data.get('buttons')
        faq = ticket_data.get('faq', {})
        faq_type = faq.get('type')
        faq_items = faq.get('items')

        if faq and faq_type and faq_items:
            if faq_type == 1:
                self.add_item(await FAQCreateDropDown(guild_id, faq_items, buttons))
                return
            else:
                self.add_item(await FAQButtonOpen(guild_id, buttons))
        self.add_item(await FAQButtonCreate(guild_id, buttons))

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        gdb = GuildDateBases(interaction.guild_id)
        tickets: TicketsPayload = await gdb.get('tickets', {})
        ticket_data = tickets.get(interaction.message.id)
        enabled = ticket_data.get('enabled', True)
        if not enabled:
            await interaction.response.send_message('Tickets are disabled by the server administrators!', ephemeral=True)
            return False
        return True
