import nextcord
from nextcord.ext import commands
from bot.resources import check

class teams(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="shutdown")
    @check.team_only()
    async def shutdown(self,ctx:commands.Context):
        await ctx.send("The bot has activated the completion process!")
        await self.bot.close()

    @commands.command()
    @commands.guild_only()
    @check.team_only()
    async def subo(self,ctx:commands.Context,member:nextcord.Member,*,command:str):
        ctx.message.author = member
        await self.bot.process_with_str(ctx.message,command)

    @commands.command()
    @check.team_only()
    async def load_extension(self,ctx:commands.Context,name):
        self.bot.load_extension(f"bot.cogs.{name}")

    @commands.command()
    @check.team_only()
    async def unload_extension(self,ctx:commands.Context,name):
        self.bot.unload_extension(f"bot.cogs.{name}")

    @commands.command()
    @check.team_only()
    async def extensions(self,ctx:commands.Context):
        exts = self.bot.extensions
        name_exts = []
        for ext in exts.values():
            name_exts.append(ext.__name__)
        await ctx.send(name_exts)

def setup(bot):
    bot.add_cog(teams(bot))