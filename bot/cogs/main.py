from nextcord.ext import commands
import nextcord

class main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shutdown")
    @commands.is_owner()
    async def shutdown(self,ctx:commands.Context):
        await ctx.send("The bot has activated the completion process!")
        await self.bot.close()

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def subo(self,ctx:commands.Context,member:nextcord.Member,*,command:str):
        ctx.message.author = member
        await self.bot.process_with_str(ctx.message,command)

    @commands.command()
    async def ping(self,ctx: commands.Context):
        await ctx.send(f"Pong!🥍🎉\n{ctx.author.name}")




def setup(bot):
    bot.add_cog(main(bot))