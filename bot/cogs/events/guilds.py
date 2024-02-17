import time
import nextcord
from nextcord.ext import commands

from bot.databases.db import GuildDateBases


class guilds_event(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_guild_join(self, guild: nextcord.Guild):
        if ((gthd := self.bot.guild_timer_handlers.get(guild.id))
                and gthd[1] > time.time()):
            gthd[0].cancel()
        else:
            GuildDateBases(guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: nextcord.Guild):
        gdb = GuildDateBases(guild.id)
        delay = 60 * 60 * 24 * 3
        gth = self.bot.loop.call_later(delay, gdb.delete)
        self.bot.guild_timer_handlers[guild.id] = (gth, delay+time.time())


def setup(bot: commands.Bot):
    event = guilds_event(bot)

    bot.add_cog(event)
