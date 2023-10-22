from nextcord.ext import commands

class dops(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sync(ctx:commands.Context):
        await bot.register_application_commands(modal,guild_id=ctx.guild.id)
        await ctx.send("Successful add")

    @commands.command()
    async def unsync(ctx:commands.Context):
        try:
            await bot.delete_application_commands(modal,guild_id=ctx.guild.id)
            await ctx.send("Successful remove")
        except:
            await ctx.send("# <:warning:1155034269027139636>404 Not Found")



def setup(bot):
    bot.add_cog(dops(bot))