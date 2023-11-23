import nextcord
from nextcord.ext import commands

from bot.databases.db import GuildDateBases
from bot.misc import utils
from bot.resources import errors
from bot import languages
from bot.resources.errors import CallbackCommandError



class command_event(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
    
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        CommandError = CallbackCommandError(ctx,error)
        await CommandError.process()




def setup(bot: commands.Bot):
    event = command_event(bot)
    
    bot.add_cog(event)