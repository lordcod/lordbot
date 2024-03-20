
import nextcord
from nextcord.ext import commands

from bot.misc.lordbot import LordBot


class reminder(commands.Cog):
    def __init__(self, bot: LordBot):
        self.bot = bot


def setup(bot):
    bot.add_cog(help(bot))
