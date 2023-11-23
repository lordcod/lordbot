import nextcord
from nextcord.ext import commands

from bot.databases.db import GuildDateBases
from bot.misc import utils
from bot.resources import errors
from bot import languages

import googletrans

translator = googletrans.Translator()


class thread_event(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
    
    
    @commands.Cog.listener()
    async def on_thread_create(thread:nextcord.Thread):
        guild_data = GuildDateBases(thread.guild.id)
        afm = guild_data.get('thread_messages')
        thread_data = afm.get(thread.parent_id,None)
        if not thread_data:
            return
        
        content = thread_data.get('content','')
        content = await utils.generate_message(content)
        await thread.send(**content)



def setup(bot: commands.Bot):
    event = thread_event(bot)
    
    bot.add_cog(event)