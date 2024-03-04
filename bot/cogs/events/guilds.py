import timeit
import nextcord
from nextcord.ext import commands

from bot.databases import GuildDateBases
from bot.misc.lordbot import LordBot


class guilds_event(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_guild_join(self, guild: nextcord.Guild):
        if ((gthd := self.bot.guild_timer_handlers.get(guild.id))
                and gthd[1] > timeit.default_timer()):
            gthd[0].cancel()
        else:
            GuildDateBases(guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: nextcord.Guild):
        gdb = GuildDateBases(guild.id)
        delay = 60 * 60 * 24 * 3
        gth = self.bot.loop.call_later(delay, gdb.delete)
        self.bot.guild_timer_handlers[guild.id] = (
            gth, delay+timeit.default_timer())


def setup(bot):
    bot.add_cog(guilds_event(bot))
