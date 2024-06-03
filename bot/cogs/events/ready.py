import logging
from nextcord.ext import commands

from bot.languages.help import get_command
from bot.databases import RoleDateBases, BanDateBases
from bot.misc.lordbot import LordBot
from bot.views.ideas import ConfirmView, IdeaView, ReactionConfirmView

import time
import asyncio
_log = logging.getLogger(__name__)


class ReadyEvent(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
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

        self.bot.add_view(await ConfirmView())
        self.bot.add_view(await ReactionConfirmView())
        self.bot.add_view(await IdeaView())

        _log.info(f"The bot is registered as {self.bot.user}")

    async def on_disconnect(self):
        await self.bot.session.close()
        await self.bot.engine.__connection.close()
        _log.critical("Bot is disconnect")

    async def process_temp_bans(self):
        bsdb = BanDateBases()
        datas = await bsdb.get_all()

        for (guild_id, member_id, ban_time) in datas:
            mbrsd = BanDateBases(guild_id, member_id)
            self.bot.lord_handler_timer.create_timer_handler(
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

            self.bot.lord_handler_timer.create_timer_handler(
                role_time-time.time(), mrsdb.remove_role(member, role), f"role:{guild_id}:{member_id}:{role_id}")


def setup(bot):
    bot.add_cog(ReadyEvent(bot))
