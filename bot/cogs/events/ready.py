import nextcord
from nextcord.ext import commands
from bot.misc.logger import Logger

from time import sleep
from string import ascii_lowercase
from random import choice, randint

class ready_event(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        Logger.success(f"The bot is registered as {self.bot.user}")
    
    @commands.Cog.listener()
    async def on_disconnect(self):
        Logger.core("Bot is disconnect")
    
    


def setup(bot: commands.Bot):
    event = ready_event(bot)
    
    bot.add_cog(event)