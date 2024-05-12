from datetime import timedelta
import nextcord
from nextcord.ext import commands
import time
import asyncio
from typing import Optional

from bot.misc.lordbot import LordBot


class MemberTimeoutEvent(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_guild_audit_log_entry_create(self,
                                              entry: nextcord.AuditLogEntry):
        if not (entry.action == nextcord.AuditLogAction.member_update
                and hasattr(entry.before, "communication_disabled_until")):
            return

        loctime = time.time()-self.bot.latency

        if (entry.before.communication_disabled_until is None and
                entry.after.communication_disabled_until is not None):

            timing = entry.target.communication_disabled_until.timestamp()
            temp = timing-loctime

            self.bot.dispatch(
                "timeout", entry.target, temp, entry.user, entry.reason)

            th = self.bot.loop.call_later(
                temp, asyncio.create_task, self.process_untimeout(entry.target))

            self.bot.timeouts[entry.target.id] = (
                temp, timing, th, loctime)
        if (entry.before.communication_disabled_until is not None and
                entry.after.communication_disabled_until is None):
            try:
                _data = self.bot.timeouts[entry.target.id]
                duration = loctime-_data[3]
                th = _data[2]
                th._args[0].close()
                th.cancel()
            except (KeyError, IndexError, AttributeError):
                duration = None
            self.bot.dispatch("untimeout", entry.target,
                              duration, entry.user, entry.reason)
            self.bot.timeouts.pop(entry.target.id, None)

    async def process_untimeout(self, member: nextcord.Member):
        loctime = time.time()
        try:
            _data = self.bot.timeouts[member.id]
            duration = loctime-_data[3]
        except (KeyError, IndexError, AttributeError):
            duration = None
        self.bot.timeouts.pop(member.id, None)
        setattr(member, '_timeout', None)
        self.bot.dispatch("untimeout", member, duration, None, None)


def setup(bot):
    bot.add_cog(MemberTimeoutEvent(bot))
