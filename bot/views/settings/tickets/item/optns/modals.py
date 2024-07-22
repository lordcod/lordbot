from __future__ import annotations
import contextlib
from typing import Any, List, Literal, Optional, Tuple

import nextcord


from bot.databases.handlers.guildHD import GuildDateBases
from bot.databases.varstructs import ModalItemPayload, TicketsPayload
from bot.misc.utils import AsyncSterilization
from bot.resources.ether import Emoji
from .standart import ViewOptionItem


def get_emoji(value: Any) -> Literal[Emoji.online, Emoji.offline]:
    if value:
        return Emoji.online
    else:
        return Emoji.offline


def get_style(value: Literal[1, 2]) -> str:
    if value == 1:
        return 'Short'
    else:
        return 'Long'


def join_args(*args: Tuple[str, Optional[Any]]) -> str:
    res = []
    for que, value in args:
        if value is True:
            res.append(que)
            continue
        if not value:
            continue
        res.append(f'{que}{value}')
    return '\n'.join(res)


@AsyncSterilization
class TicketFormsModal(nextcord.ui.Modal):
    async def __init__(self, guild: nextcord.Guild, message_id: int, selected_item: Optional[int] = None):
        self.message_id = message_id
        self.selected_item = selected_item

        gdb = GuildDateBases(guild.id)
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[self.message_id]
        modals = ticket_data.get('modals')
        item = None

        if selected_item is not None:
            item = modals[selected_item]
            super().__init__(f"Ticket Froms #{selected_item+1}")
        else:
            super().__init__("Ticket Froms")

        def get_data(name):
            if selected_item is not None:
                return item.get(name)

        self.label = nextcord.ui.TextInput(
            label='Label',
            max_length=128,
            placeholder=get_data('label')
        )
        if get_data('label'):
            self.label.required = False
        self.add_item(self.label)

        self.placeholder = nextcord.ui.TextInput(
            label='Placeholder',
            max_length=128,
            required=False,
            placeholder=get_data('placeholder')
        )
        self.add_item(self.placeholder)

        self.default_value = nextcord.ui.TextInput(
            label='Default value',
            max_length=128,
            required=False,
            placeholder=get_data('default_value')
        )
        self.add_item(self.default_value)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[self.message_id]
        modals = ticket_data.get('modals', [])

        if self.selected_item is not None:
            item = modals[self.selected_item]
        else:
            item = {}

        data = dict(
            label=self.label.value,
            placeholder=self.placeholder.value,
            default_value=self.default_value.value
        )
        for key, value in data.items():
            if key != 'label' and value.lower().strip() in ('none', '-'):
                item.pop(key, None)
                continue
            if value:
                item[key] = value

        if self.selected_item is not None:
            try:
                modals[self.selected_item] = item
            except IndexError:
                self.selected_item = len(modals)
                modals.append(item)
        else:
            self.selected_item = len(modals)
            modals.append(item)

        await gdb.set_on_json('tickets', self.message_id, ticket_data)

        view = await TicketFormsView(interaction.guild, self.message_id, self.selected_item)
        embed = await view.get_embed(interaction.guild)
        await interaction.response.edit_message(embed=embed, view=view)


@AsyncSterilization
class TicketFormsDropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild_id: int, modals: Optional[List[ModalItemPayload]] = None, selected_item: Optional[int] = None) -> None:
        if modals is None:
            modals = []

        options = [
            nextcord.SelectOption(
                label=item['label'],
                value=i,
                description=item.get('placeholder'),
                emoji=get_emoji(item.get('required', True)),
                default=selected_item == i
            )
            for i, item in enumerate(modals)
        ]

        disabled = len(options) == 0
        if disabled:
            options.append(
                nextcord.SelectOption(label='SelectOption')
            )

        super().__init__(placeholder="Select the form to edit or delete.", options=options, disabled=disabled)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = int(self.values[0])

        view = await TicketFormsView(interaction.guild, self.view.message_id, value)
        embed = await view.get_embed(interaction.guild)
        await interaction.response.edit_message(embed=embed, view=view)


@AsyncSterilization
class TicketFormsRequiredDropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild_id: int, modal: Optional[ModalItemPayload], selected_item: Optional[int] = None) -> None:
        self.selected_item = selected_item

        if selected_item is None:
            options = [nextcord.SelectOption(label='SelectOption')]
            super().__init__(placeholder="Specify whether the data is required for the form.",
                             options=options, disabled=True)
            return

        required = modal.get('required', True)

        options = [
            nextcord.SelectOption(
                label='Required',
                value=1,
                description='The user will need to enter the data in the field.',
                emoji=Emoji.online,
                default=required
            ),
            nextcord.SelectOption(
                label='Optional',
                value=0,
                description='The user can optionally enter data in the field.',
                emoji=Emoji.offline,
                default=not required
            ),
        ]

        super().__init__(placeholder="Specify whether the data is required for the form.", options=options)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = bool(int(self.values[0]))

        gdb = GuildDateBases(interaction.guild_id)
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[self.view.message_id]

        modals = ticket_data['modals']
        modal = modals[self.selected_item]
        modal['required'] = value

        await gdb.set_on_json('tickets', self.view.message_id, ticket_data)

        view = await TicketFormsView(interaction.guild, self.view.message_id, self.selected_item)
        embed = await view.get_embed(interaction.guild)
        await interaction.response.edit_message(embed=embed, view=view)


@AsyncSterilization
class TicketFormsStyleDropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild_id: int, modal: Optional[ModalItemPayload], selected_item: Optional[int] = None) -> None:
        self.selected_item = selected_item

        if selected_item is None:
            options = [nextcord.SelectOption(label='SelectOption')]
            super().__init__(placeholder="Specify the short or paragraph form style",
                             options=options, disabled=True)
            return

        style = modal.get('style', 1)

        options = [
            nextcord.SelectOption(
                label='Short',
                value=1,
                description='Indicates the short style of the form.',
                emoji=Emoji.online,
                default=style == 1
            ),
            nextcord.SelectOption(
                label='Paragraph',
                value=2,
                description='Displays the paragraph style of the form.',
                emoji=Emoji.offline,
                default=style == 2
            ),
        ]

        super().__init__(placeholder="Specify the short or paragraph form style", options=options)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = int(self.values[0])

        gdb = GuildDateBases(interaction.guild_id)
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[self.view.message_id]

        modals = ticket_data['modals']
        modal = modals[self.selected_item]
        modal['style'] = value

        await gdb.set_on_json('tickets', self.view.message_id, ticket_data)

        view = await TicketFormsView(interaction.guild, self.view.message_id, self.selected_item)
        embed = await view.get_embed(interaction.guild)
        await interaction.response.edit_message(embed=embed, view=view)


@AsyncSterilization
class TicketFormsView(ViewOptionItem):
    label = 'Ticket Forms'
    description = 'Set up the forms and its type.'

    async def __init__(self, guild: nextcord.Guild, message_id: int, selected_item: Optional[int] = None):
        self.message_id = message_id
        self.selected_item = selected_item

        gdb = GuildDateBases(guild.id)
        color = await gdb.get('color')
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[self.message_id]
        ticket_index = list(tickets.keys()).index(message_id)+1
        created_embed = ticket_data.get('creating_embed_inputs')
        modals = ticket_data.get('modals')
        item = None

        self.embed = nextcord.Embed(
            title=f'Ticket #{ticket_index}',
            color=color,
            description=(
                'The tickets module allows you to create and manage support requests, '
                'helping participants to easily open tickets, and administrators to effectively track and solve them.'
            )
        )

        if selected_item is not None:
            item = modals[selected_item]
            self.embed.add_field(
                name='',
                value=join_args(
                    ("— Creating embed inputs: ", get_emoji(ticket_data.get('creating_embed_inputs', True))),
                    ("— Label: ", item.get('label')),
                    ("— Placeholder: ", item.get('placeholder')),
                    ("— Default value: ", item.get('default_value')),
                    ("— Style: ", get_style(item.get('style', 1))),
                    ("— Required: ", get_emoji(item.get('required', True)))
                )
            )

        super().__init__()

        if modals is not None:
            if len(modals) >= 5:
                self.add.disabled = True
            self.clear.disabled = False
        if selected_item is not None:
            self.edit.disabled = False
            self.remove.disabled = False
        if created_embed:
            self.switch_creating_embed_inputs.label = 'Disable creating embed inputs'
            self.switch_creating_embed_inputs.style = nextcord.ButtonStyle.red
        else:
            self.switch_creating_embed_inputs.label = 'Enable creating embed inputs'
            self.switch_creating_embed_inputs.style = nextcord.ButtonStyle.green

        tfrdd = await TicketFormsRequiredDropDown(guild.id, item, selected_item)
        self.add_item(tfrdd)

        tfsdd = await TicketFormsStyleDropDown(guild.id, item, selected_item)
        self.add_item(tfsdd)

        tfdd = await TicketFormsDropDown(guild.id, modals, selected_item)
        self.add_item(tfdd)

    @nextcord.ui.button(label='Add', style=nextcord.ButtonStyle.green, row=0)
    async def add(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = await TicketFormsModal(interaction.guild, self.message_id)
        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label='Edit', style=nextcord.ButtonStyle.blurple, disabled=True, row=0)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = await TicketFormsModal(interaction.guild, self.message_id, self.selected_item)
        await interaction.response.send_modal(modal)

    @nextcord.ui.button(label='Remove', style=nextcord.ButtonStyle.red, disabled=True, row=0)
    async def remove(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[self.message_id]
        with contextlib.suppress(IndexError):
            ticket_data['modals'].pop(self.selected_item)
        await gdb.set_on_json('tickets', self.message_id, ticket_data)

        view = await TicketFormsView(interaction.guild, self.message_id)
        embed = await view.get_embed(interaction.guild)
        await interaction.response.edit_message(embed=embed, view=view)

    @nextcord.ui.button(label='Enable creating embed inputs', style=nextcord.ButtonStyle.grey, row=1)
    async def switch_creating_embed_inputs(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[self.message_id]
        ticket_data['creating_embed_inputs'] = not ticket_data.get('creating_embed_inputs')
        await gdb.set_on_json('tickets', self.message_id, ticket_data)

        view = await TicketFormsView(interaction.guild, self.message_id, self.selected_item)
        embed = await view.get_embed(interaction.guild)
        await interaction.response.edit_message(embed=embed, view=view)

    @nextcord.ui.button(label='Clear', style=nextcord.ButtonStyle.grey, disabled=True, row=1)
    async def clear(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        tickets: TicketsPayload = await gdb.get('tickets')
        ticket_data = tickets[self.message_id]
        ticket_data['modals'] = []
        await gdb.set_on_json('tickets', self.message_id, ticket_data)

        view = await TicketFormsView(interaction.guild, self.message_id)
        embed = await view.get_embed(interaction.guild)
        await interaction.response.edit_message(embed=embed, view=view)
