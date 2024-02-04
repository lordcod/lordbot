from nextcord.ext import commands

from bot.misc.logger import Logger
from bot.databases.db import RoleDateBases
from bot.views.ideas import (Confirm, IdeaBut)

import time
import asyncio


class ready_event(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.process_temp_roles()

        self.bot.add_view(Confirm())
        self.bot.add_view(IdeaBut())

        Logger.success(f"The bot is registered as {self.bot.user}")

    @commands.Cog.listener()
    async def on_disconnect(self):
        Logger.core("Bot is disconnect")

    async def process_temp_roles(self):
        rsdb = RoleDateBases()
        datas = rsdb.get_all()

        for dat in datas:
            guild_id = dat[0]
            member_id = dat[1]
            temp_datas = dat[2]

            guild = self.bot.get_guild(guild_id)
            if not guild:
                continue

            member = guild.get_member(member_id)
            if not member:
                continue

            mrsdb = RoleDateBases(guild_id, member_id)

            for tp_data in temp_datas:
                temp = tp_data.get("time", 0) - int(time.time())
                role_id = tp_data.get("role_id")
                role = guild.get_role(role_id)

                if not (temp and role):
                    continue

                self.bot.loop.call_later(
                    temp, asyncio.create_task, member.remove_roles(role))
                self.bot.loop.call_later(
                    temp, asyncio.create_task, mrsdb.aremove(tp_data))


def setup(bot: commands.Bot):
    event = ready_event(bot)

    bot.add_cog(event)
