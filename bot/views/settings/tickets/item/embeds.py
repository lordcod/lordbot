
from typing import Any, Literal, Optional, Tuple
import nextcord

from bot.databases.handlers.guildHD import GuildDateBases
from bot.databases.varstructs import TicketsPayload
from bot.resources.ether import Emoji
from bot.resources.info import DEFAULT_TICKET_FAQ_TYPE, DEFAULT_TICKET_TYPE


def get_emoji(value: Any) -> Literal[Emoji.online, Emoji.offline]:
    if value:
        return Emoji.online
    else:
        return Emoji.offline


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


async def get_embed(guild: nextcord.Guild, message_id: int) -> nextcord.Embed:
    gdb = GuildDateBases(guild.id)
    color = await gdb.get('color')
    tickets: TicketsPayload = await gdb.get('tickets')
    ticket_data = tickets[message_id]
    ticket_index = list(tickets.keys()).index(message_id)+1

    enabled = ticket_data.get('enabled')
    ticket_type = ticket_data.get('type', DEFAULT_TICKET_TYPE)
    channel_id = ticket_data.get('channel_id')
    message_id = ticket_data.get('message_id')
    global_tickets_limit = ticket_data.get('global_user_tickets_limit')
    tickets_limit = ticket_data.get('user_tickets_limit')
    categories = ticket_data.get('categories')
    category_type = ticket_data.get('category_type', 1)
    user_closed = ticket_data.get('user_closed', True)
    modals = ticket_data.get('modals')
    created_embed = ticket_data.get('creating_embed_inputs')
    faq = ticket_data.get('faq', {})
    faq_type = faq.get('type', DEFAULT_TICKET_FAQ_TYPE)
    faq_items = faq.get('items')

    channel = guild.get_channel(channel_id)
    message = channel.get_partial_message(message_id)

    ticket_type_message = 'Channels' if ticket_type == 1 else 'Threads'

    if faq and faq_items:
        faq_type_message = 'DropDown' if faq_type == 1 else 'Button'
        faq_message = (
            f'— FAQ type: {faq_type_message}\n'
            f'— Number of FAQ: {len(faq_items)}'
        )
    else:
        faq_message = f'— FAQ: {Emoji.offline}'

    if categories:
        cat_type_message = 'DropDown' if category_type == 1 else 'Button'
        cat_message = (
            f'— Category type: {cat_type_message}\n'
            f'— Number of categories: {len(categories)}'
        )
    else:
        cat_message = f'— Categories: {Emoji.offline}'

    if modals:
        modal_message = (
            f'— Number of modals: {len(modals)}\n'
            f'— Creating embed responses: {get_emoji(created_embed)}'
        )
    else:
        modal_message = f'— Modals: {Emoji.offline}'

    embed = nextcord.Embed(
        title=f'Ticket #{ticket_index}',
        color=color,
        description=(
            'The tickets module allows you to create and manage support requests, '
            'helping participants to easily open tickets, and administrators to effectively track and solve them.\n\n'
            f'Linked Channel: {channel.mention}\n'
            f'Linked Message: {message.jump_url}\n'
        )
    )
    embed.add_field(
        name='',
        value=join_args(
            ('— Enabled: ', get_emoji(enabled)),
            ('― Ticket type: ', ticket_type_message),
            ('― Global ticket limit: ', global_tickets_limit),
            ('— Category ticket limit: ', tickets_limit),
            ('— Closing by the user:', get_emoji(user_closed)),
            (faq_message, True),
            (cat_message, True),
            (modal_message, True),
        )
    )

    return embed
