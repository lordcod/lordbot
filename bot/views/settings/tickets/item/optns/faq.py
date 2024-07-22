from __future__ import annotations
import contextlib
from typing import Optional

import nextcord


from bot.databases.handlers.guildHD import GuildDateBases
from bot.databases.varstructs import FaqPayload, TicketsPayload
from bot.misc.utils import AsyncSterilization
from bot.resources.info import DEFAULT_TICKET_FAQ_TYPE
from .standart import ViewOptionItem


@AsyncSterilization
class TicketFAQModal(nextcord.ui.Modal):
    async def __init__(self, guild: nextcord.Guild, message_id: int, selected_faq_item: Optional[int] = None):
        self.message_id = message_id
        self.selected_faq_item = selected_faq_item

        gdb = GuildDateBases(guild.id)
        tickets_data: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets_data[message_id]
        faq = ticket_data.get('faq', {})
        faq_items = faq.get('items', [])

        self.faq_item = faq_item = None
        if selected_faq_item is not None:
            with contextlib.suppress(IndexError):
                self.faq_item = faq_item = faq_items[selected_faq_item]

        def get_data(name):
            if faq_item is not None:
                return faq_item.get(name)

        if faq_item is None:
            super().__init__('Ticket FAQ Item')
        else:
            super().__init__(f'Ticket FAQ Item #{selected_faq_item+1}')

        self.label = nextcord.ui.TextInput(
            label='Label',
            max_length=128,
            placeholder=get_data('label')
        )
        if get_data('label'):
            self.label.required = False
        self.add_item(self.label)

        self.emoji = nextcord.ui.TextInput(
            label='Emoji',
            required=False,
            max_length=128,
            placeholder=get_data('emoji')
        )
        self.add_item(self.emoji)

        self.description = nextcord.ui.TextInput(
            label='Description',
            style=nextcord.TextInputStyle.paragraph,
            required=False,
            max_length=1024,
            placeholder=get_data('description')
        )
        self.add_item(self.description)

        self.response = nextcord.ui.TextInput(
            label='Answer',
            style=nextcord.TextInputStyle.paragraph,
            placeholder=get_data('response')
        )
        if get_data('response'):
            self.response.required = False
        self.add_item(self.response)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[self.message_id]
        faq = ticket_data.get('faq', {})
        faq_items = faq.get('items', [])

        if self.faq_item:
            faq_item_payload = self.faq_item.copy()
        else:
            faq_item_payload = {}

        data = dict(
            label=self.label.value,
            emoji=self.emoji.value,
            description=self.description.value,
            response=self.response.value
        )
        for key, value in data.items():
            if value:
                faq_item_payload[key] = value

        if self.selected_faq_item is None:
            faq_items.append(faq_item_payload)
        else:
            try:
                faq_items[self.selected_faq_item] = faq_item_payload
            except IndexError:
                self.selected_faq_item = len(faq_items)
                faq_items.append(faq_item_payload)

        faq['items'] = faq_items
        ticket_data['faq'] = faq
        await gdb.set_on_json('tickets', self.message_id, ticket_data)

        await self.view.edit_panel(interaction)

        view = await TicketFAQView(interaction.guild, self.message_id, self.selected_faq_item)
        embed = await view.get_embed(interaction.guild)
        await interaction.response.edit_message(embed=embed, view=view)


@AsyncSterilization
class TicketFAQTypeDropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild_id: int, faq: FaqPayload) -> None:
        faq_type = faq.get('type', DEFAULT_TICKET_FAQ_TYPE)
        faq_items = faq.get('items')

        options = [
            nextcord.SelectOption(
                label='Dropdown',
                description='Create a ticket through the last item in the drop-down menu with FAQ.',
                value=1,
                default=faq_type == 1
            ),
            nextcord.SelectOption(
                label='Button',
                description='You will have 2 FAQ buttons and create ticket.',
                value=2,
                default=faq_type == 2
            ),
        ]
        super().__init__(options=options, disabled=not faq_items)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = int(self.values[0])

        gdb = GuildDateBases(interaction.guild_id)
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[self.view.message_id]
        faq = ticket_data.get('faq', {})
        faq['type'] = value
        ticket_data['faq'] = faq
        await gdb.set_on_json('tickets', self.view.message_id, ticket_data)

        await self.view.edit_panel(interaction)

        view = await TicketFAQView(interaction.guild, self.view.message_id, self.view.selected_faq_item)
        embed = await view.get_embed(interaction.guild)
        await interaction.response.edit_message(embed=embed, view=view)


@AsyncSterilization
class TicketFAQItemsDropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild_id: int, faq: FaqPayload, selected_faq_item: Optional[int] = None) -> None:
        faq_items = faq.get('items', [])

        options = [
            nextcord.SelectOption(
                label=item['label'],
                value=i,
                description=item.get('description'),
                emoji=item.get('emoji'),
                default=selected_faq_item == i
            )
            for i, item in enumerate(faq_items)
        ]

        disabled = len(options) == 0
        if disabled:
            options.append(
                nextcord.SelectOption(label='SelectOption')
            )

        super().__init__(options=options, disabled=disabled)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = int(self.values[0])

        view = await TicketFAQView(interaction.guild, self.view.message_id, value)
        embed = await view.get_embed(interaction.guild)
        await interaction.response.edit_message(embed=embed, view=view)


@AsyncSterilization
class TicketFAQView(ViewOptionItem):
    label = 'Ticket FAQ'
    description = 'Set up the FAQ and its type.'

    async def __init__(self, guild: nextcord.Guild, message_id: int, selected_faq_item: Optional[int] = None):
        self.message_id = message_id
        self.selected_faq_item = selected_faq_item

        gdb = GuildDateBases(guild.id)
        tickets_data: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets_data[message_id]
        faq = ticket_data.get('faq', {})
        faq_items = faq.get('items')

        super().__init__()

        if faq_items is not None:
            if len(faq_items) >= 20:
                self.add.disabled = True
            self.clear.disabled = False
        if selected_faq_item is not None:
            self.edit.disabled = False
            self.remove.disabled = False

        ttdd = await TicketFAQTypeDropDown(guild.id, faq)
        self.add_item(ttdd)
        tidd = await TicketFAQItemsDropDown(guild.id, faq, selected_faq_item)
        self.add_item(tidd)

    @nextcord.ui.button(label='Add', style=nextcord.ButtonStyle.green)
    async def add(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = await TicketFAQModal(interaction.guild, self.message_id)
        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label='Edit', style=nextcord.ButtonStyle.blurple, disabled=True)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = await TicketFAQModal(interaction.guild, self.message_id, self.selected_faq_item)
        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label='Remove', style=nextcord.ButtonStyle.red, disabled=True)
    async def remove(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[self.message_id]
        faq = ticket_data.get('faq', {})
        faq_items = faq.get('items', [])

        with contextlib.suppress(IndexError):
            faq_items.pop(self.selected_faq_item)

        faq['items'] = faq_items
        ticket_data['faq'] = faq
        await gdb.set_on_json('tickets', self.message_id, ticket_data)

        await self.edit_panel(interaction)

        view = await TicketFAQView(interaction.guild, self.message_id)
        embed = await view.get_embed(interaction.guild)
        await interaction.response.edit_message(embed=embed, view=view)

    @nextcord.ui.button(label='Clear', style=nextcord.ButtonStyle.grey, disabled=True)
    async def clear(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[self.message_id]
        faq = ticket_data.get('faq', {})
        faq['items'] = []
        ticket_data['faq'] = faq
        await gdb.set_on_json('tickets', self.message_id, ticket_data)

        await self.edit_panel(interaction)

        view = await TicketFAQView(interaction.guild, self.message_id)
        embed = await view.get_embed(interaction.guild)
        await interaction.response.edit_message(embed=embed, view=view)
