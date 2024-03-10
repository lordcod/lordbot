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
        self.bot.lord_handler_timer.close_as_key(f'guild-deleted:{guild.id}')
        GuildDateBases(guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: nextcord.Guild):
        gdb = GuildDateBases(guild.id)
        delay = 60 * 60 * 24 * 3
        self.bot.lord_handler_timer.create_timer_handler(
            delay, gdb.adelete(), f'guild-deleted:{guild.id}')


def setup(bot):
    bot.add_cog(guilds_event(bot))
