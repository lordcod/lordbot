import nextcord
from nextcord.ext import commands

from bot.misc.ratelimit import Cooldown
from bot.misc.logger import Logger
from bot.resources import errors
from bot.databases.db import GuildDateBases, CommandDB
from bot.resources.errors import CallbackCommandError, MissingRole, MissingChannel, CommandOnCooldown


class interactions_event(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
        
        bot.event(self.on_interaction)
    
    async def on_interaction(self, interaction: nextcord.Interaction):
        print(interaction.permissions.administrator)



def setup(bot: commands.Bot):
    event = interactions_event(bot)
    
    bot.add_cog(event)