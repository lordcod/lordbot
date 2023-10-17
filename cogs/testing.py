from nextcord.ext import commands

class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def com(self, ctx, argument):
        await ctx.send(argument)       


def setup(bot):
    bot.add_cog(test(bot))