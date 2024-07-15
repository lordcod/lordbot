import logging
from typing import Dict
from nextcord.ext import commands
import orjson

from bot.databases.handlers.guildHD import GuildDateBases
from bot.databases.varstructs import GiveawayData
from bot.languages.help import get_command
from bot.databases import RoleDateBases, BanDateBases, localdb
from bot.misc import tickettools
from bot.misc.giveaway import Giveaway
from bot.misc.lordbot import LordBot
from bot.misc.utils import AsyncSterilization
from bot.resources import info
from bot.views.giveaway import GiveawayView
from bot.views.ideas import ConfirmView, IdeaView, ReactionConfirmView

import time
import asyncio

from bot.views.tempvoice import TempVoiceView
from bot.views.tickets.closes import CloseTicketView
from bot.views.tickets.delop import ControllerTicketView
from bot.views.tickets.faq import FAQView
_log = logging.getLogger(__name__)


class ReadyEvent(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        bot.set_event(self.on_shard_disconnect)
        bot.set_event(self.on_disconnect)
        super().__init__()

    async def process_tickets(self):
        with open('tickets_data.json', 'rb') as file:
            tickets_data = orjson.loads(file.read())

        for guild_id, ticket_payload in tickets_data.items():
            guild_id = int(guild_id)
            guild = self.bot.get_guild(guild_id)

            if guild is None:
                continue

            _log.trace('Set config %s (%d) for tickets', guild.name, guild_id)

            gdb = GuildDateBases(guild_id)
            tickets = await gdb.get('tickets')

            if ticket_payload.pop('total', True) == False:
                locale = ticket_payload.pop('locale', 'ru')
                ticket_payload.update(info.DEFAULT_TICKET_PAYLOAD_RU.copy(
                ) if locale == 'ru' else info.DEFAULT_TICKET_PAYLOAD.copy())

            ticket_id = None
            for message_id, ticket in tickets.items():
                if ticket['channel_id'] == ticket_payload['channel_id']:
                    ticket_id = message_id
                    break

            if ticket_id:
                ticket_payload.update({
                    'message_id': ticket_id,
                    'category_id': ticket.get('category_id')
                })
                await gdb.set_on_json('tickets', ticket_id, ticket_payload)
                await tickettools.ModuleTicket.update_ticket_panel(guild, ticket_id)
            else:
                channel = guild.get_channel(ticket_payload['channel_id'])
                await tickettools.ModuleTicket.create_ticket_panel(channel, ticket_payload)

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            await asyncio.wait_for(self.bot.__with_ready__, timeout=30)
        except asyncio.TimeoutError:
            return

        await asyncio.gather(
            self.find_not_data_commands(),
            self.process_tickets(),
            self.process_temp_roles(),
            self.process_temp_bans(),
            self.process_giveaways(),
            self.process_guild_delete_tasks()
        )

        views = [ControllerTicketView, CloseTicketView, FAQView, ConfirmView,
                 ReactionConfirmView, IdeaView, GiveawayView, TempVoiceView]
        _log.trace('Views set: %s', views)
        for view in views:
            if isinstance(view, AsyncSterilization):
                rs = await view()
            else:
                rs = view()
            self.bot.add_view(rs)

        await GuildDateBases(1179069504186232852).set('tempvoice', {
            'enabled': True,
            'category_id': 1179069504651796561,
            'channel_id': 1179069504651796563,
            'channel_name': '{voice.count}-{member.username}',
            'channel_limit': 4
        })

        _log.info(f"The bot is registered as {self.bot.user}")

    async def on_disconnect(self):
        await self.bot._LordBot__session.close()
        await localdb._update_db(__name__)
        await localdb.cache.close()
        self.bot.engine.get_connection().close()
        _log.critical("Bot is disconnect")

    async def on_shard_disconnect(self, shard_id: int):
        _log.critical("Bot is disconnect (ShardId:%d)", shard_id)

    async def find_not_data_commands(self):
        cmd_wnf = []
        for cmd in self.bot.commands:
            cmd_data = get_command(cmd.qualified_name)
            if cmd_data is None:
                cmd_wnf.append(cmd.qualified_name)

        if cmd_wnf:
            _log.info(
                f"Was not found command information: {', '.join(cmd_wnf)}")

    async def process_temp_bans(self):
        bsdb = BanDateBases()
        datas = await bsdb.get_all()

        for (guild_id, member_id, ban_time) in datas:
            mbrsd = BanDateBases(guild_id, member_id)
            self.bot.lord_handler_timer.create(
                ban_time-time.time(), mbrsd.remove_ban(self.bot._connection), f"ban:{guild_id}:{member_id}")

    async def process_temp_roles(self):
        rsdb = RoleDateBases()
        datas = await rsdb.get_all()

        for (guild_id, member_id, role_id, role_time) in datas:
            if not (
                (guild := self.bot.get_guild(guild_id))
                and (member := guild.get_member(member_id))
                and (role := guild.get_role(role_id))
            ):
                continue

            mrsdb = RoleDateBases(guild_id, member_id)

            self.bot.lord_handler_timer.create(
                role_time-time.time(), mrsdb.remove_role(member, role), f"role:{guild_id}:{member_id}:{role_id}")

    async def process_giveaways(self):
        for guild in self.bot.guilds:
            gdb = GuildDateBases(guild.id)
            giveaways: Dict[int, GiveawayData] = await gdb.get('giveaways', {})
            for id, data in giveaways.items():
                if data['completed']:
                    continue
                gw = Giveaway(guild, id)
                gw.giveaway_data = data
                self.bot.lord_handler_timer.create(
                    gw.giveaway_data.get('date_end')-time.time(),
                    gw.complete(),
                    f'giveaway:{id}'
                )

    async def process_guild_delete_tasks(self):
        ...


def setup(bot):
    bot.add_cog(ReadyEvent(bot))
