import logging
import nextcord
from nextcord.ext import commands

from bot.databases import GuildDateBases, EconomyMemberDB
from bot.misc.lordbot import LordBot

_log = logging.getLogger(__name__)


class GuildsEvent(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_guild_available(self, guild: nextcord.Guild):
        _log.trace('Guild available %s (%d), Member count: %d', guild.name, guild.id, guild.member_count)
        await GuildDateBases(guild.id).register()
        async for member in guild.fetch_members(limit=None):
            await EconomyMemberDB(guild.id, member.id).get_data()

    @commands.Cog.listener()
    async def on_guild_join(self, guild: nextcord.Guild):
        self.bot.lord_handler_timer.close_as_key(f'guild-deleted:{guild.id}')
        await GuildDateBases(guild.id).register()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: nextcord.Guild):
        gdb = GuildDateBases(guild.id)
        delay = 60 * 60 * 24 * 3
        self.bot.lord_handler_timer.create_timer_handler(
            delay, gdb.delete(), f'guild-deleted:{guild.id}')


def setup(bot):
    bot.add_cog(GuildsEvent(bot))
