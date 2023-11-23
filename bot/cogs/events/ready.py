import nextcord
from nextcord.ext import commands

from bot.databases.db import GuildDateBases
from bot.misc import utils
from bot.resources import errors
from bot import languages

import googletrans

translator = googletrans.Translator()


class ready_event(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"The bot is registered as {self.bot.user}")
    
    @commands.Cog.listener()
    async def on_disconnect(self):
        print("Bot is disconnect")
        
    


def setup(bot: commands.Bot):
    event = ready_event(bot)
    
    bot.add_cog(event)