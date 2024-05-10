import nextcord
from nextcord.ext import commands

from bot.misc.lordbot import LordBot


class Confessions(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot

    @nextcord.slash_command()
    async def confessions(self, interaction: nextcord.Interaction):
        pass

    @confessions.subcommand(name='create')
    async def confessions_create(self, interaction: nextcord.Interaction):
        pass

    @confessions.subcommand(name='report')
    async def confessions_report(self, interaction: nextcord.Interaction):
        pass

    @confessions.subcommand(name='block')
    async def confessions_block(self, interaction: nextcord.Interaction):
        pass


def setup(bot):
    bot.add_cog(Confessions(bot))
