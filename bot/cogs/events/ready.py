from nextcord.ext import commands

from bot.misc.logger import Logger
from bot.databases import RoleDateBases, BanDateBases
from bot.misc.lordbot import LordBot
from bot.views.ideas import (ConfirmView, IdeaView)

import timeit
import asyncio


class ready_event(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.process_temp_roles()
        await self.process_temp_bans()

        self.bot.add_view(ConfirmView())
        self.bot.add_view(IdeaView())

        Logger.success(f"The bot is registered as {self.bot.user}")

    @commands.Cog.listener()
    async def on_disconnect(self):
        Logger.core("Bot is disconnect")

    async def process_temp_bans(self):
        bsdb = BanDateBases()
        datas = bsdb.get_all()

        for dat in datas:
            guild_id = dat[0]
            member_id = dat[1]
            ban_time = dat[2]

            mbrsd = BanDateBases(guild_id, member_id)
            self.bot.loop.call_later(
                ban_time-timeit.default_timer(),
                asyncio.create_task,
                mbrsd.remove_ban(self.bot._connection)
            )

    async def process_temp_roles(self):
        rsdb = RoleDateBases()
        datas = rsdb.get_all()

        for dat in datas:
            guild_id = dat[0]
            member_id = dat[1]
            role_id = dat[2]
            role_time = dat[3]

            if not (
                (guild := self.bot.get_guild(guild_id)) and
                (member := guild.get_member(member_id)) and
                (role := guild.get_role(role_id))
            ):
                continue

            mrsdb = RoleDateBases(guild_id, member_id)

            rth = self.bot.loop.call_later(
                role_time-timeit.default_timer(),
                asyncio.create_task,
                mrsdb.remove_role(member, role)
            )

            self.bot.role_timer_handlers.add_th(
                guild.id, member.id, role.id, rth)


def setup(bot):
    bot.add_cog(ready_event(bot))
