import logging
from typing import Dict
from nextcord.ext import commands

from bot.databases.handlers.guildHD import GuildDateBases
from bot.databases.varstructs import GiveawayData
from bot.languages.help import get_command
from bot.databases import RoleDateBases, BanDateBases
from bot.misc.giveaway import Giveaway
from bot.misc.lordbot import LordBot
from bot.views.giveaway import GiveawayView
from bot.views.ideas import ConfirmView, IdeaView, ReactionConfirmView

import time
import asyncio
_log = logging.getLogger(__name__)


class ReadyEvent(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        bot.set_event(self.on_shard_disconnect)
        bot.set_event(self.on_disconnect)
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            await asyncio.wait_for(self.bot.__with_ready__, timeout=30)
        except asyncio.TimeoutError:
            return

        cmd_wnf = []
        for cmd in self.bot.commands:
            cmd_data = get_command(cmd.qualified_name)
            if cmd_data is None:
                cmd_wnf.append(cmd.qualified_name)

        if cmd_wnf:
            _log.info(f"Was not found command information: {', '.join(cmd_wnf)}")

        await self.process_temp_roles()
        await self.process_temp_bans()
        await self.process_giveaways()
        await self.process_guild_delete_tasks()

        self.bot.add_view(await ConfirmView())
        self.bot.add_view(await ReactionConfirmView())
        self.bot.add_view(await IdeaView())
        self.bot.add_view(GiveawayView())

        _log.info(f"The bot is registered as {self.bot.user}")

    async def on_disconnect(self):
        await self.bot.session.close()
        await self.bot.engine._DataBase__connection.close()
        _log.critical("Bot is disconnect")

    async def on_shard_disconnect(self, shard_id: int):
        await self.bot.session.close()
        await self.bot.engine._DataBase__connection.close()
        _log.critical("Bot is disconnect (ShardId:%d)", shard_id)

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
        deleted_tasks = await GuildDateBases.get_deleted()
        for id, delay in deleted_tasks:
            if self.bot.get_guild(id) or not delay:
                continue
            gdb = GuildDateBases(id)
            self.bot.lord_handler_timer.create(
                delay-time.time(), gdb.delete(), f'guild-deleted:{id}')


def setup(bot):
    bot.add_cog(ReadyEvent(bot))
