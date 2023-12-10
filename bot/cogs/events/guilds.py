import nextcord
from nextcord.ext import commands

from bot.misc import utils
from bot.misc.logger import Logger
from bot.databases.db import GuildDateBases

import asyncio


class guilds_event(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild: nextcord.Guild):
        gdb = GuildDateBases(guild.id)
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: nextcord.Guild):
        gdb = GuildDateBases(guild.id)
    
    def on_error(func):
        async def wrapped(self, member, gdb):
            try:
                result = await func(self, member, gdb)
                return result
            except Exception as err:
                Logger.error(err)
        return wrapped




def setup(bot: commands.Bot):
    event = guilds_event(bot)
    
    bot.add_cog(event)