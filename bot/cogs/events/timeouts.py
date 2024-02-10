import nextcord
from nextcord.ext import commands
import time
import asyncio
from typing import Optional


class members_event_timeouts(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_guild_audit_log_entry_create(self,
                                              entry: nextcord.AuditLogEntry):
        if entry.action != nextcord.AuditLogAction.member_update:
            return

        if (entry.before.communication_disabled_until is None and
                entry.after.communication_disabled_until is not None):
            self.bot.dispatch("timeout", entry.target, entry.user)

            timing = entry.target.communication_disabled_until.timestamp()
            temp = timing-time.time()

            th = self.bot.loop.call_later(
                temp, asyncio.create_task, self.process_untimeout(entry.target))

            self.bot.timeouts[entry.target.id] = (temp, timing, th)
        if (entry.before.communication_disabled_until is not None and
                entry.after.communication_disabled_until is None):
            self.bot.dispatch("untimeout", entry.target, entry.user)

            try:
                th = self.bot.timeouts[entry.target.id][2]
                th._args[0].close()
                th.cancel()
            except (KeyError, IndexError, AttributeError):
                pass
            self.bot.timeouts[entry.target.id] = None

    async def process_untimeout(self, member: nextcord.Member):
        self.bot.timeouts[member.id] = None
        setattr(member, '_timeout', None)
        self.bot.dispatch("untimeout", member, None)

    async def on_timeout(self,
                         member: nextcord.Member,
                         moderator: nextcord.Member):
        print(f"{moderator.display_name} выдал мут {member.display_name}")

    async def on_untimeout(self,
                           member: nextcord.Member,
                           moderator: Optional[nextcord.Member]):
        if moderator is None:
            print(f"У {member.display_name} закончился мут!")
            return
        print(f"{moderator.display_name} забрал мут у {member.display_name}")


def setup(bot):
    cog = members_event_timeouts(bot)

    bot.add_cog(cog)
