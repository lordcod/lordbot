from nextcord.ext import commands

from bot.misc.tickettools import ModuleTicket


class tests(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ticket(self, ctx: commands.Context):
        ticket = ModuleTicket(ctx.guild, ctx.channel.category)
        await ticket.create(ctx.author)


def setup(bot):
    bot.add_cog(tests(bot))
