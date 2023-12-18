import nextcord
from nextcord.ext import commands

from bot.resources import check

import sys, os


class teams(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="shutdown")
    @check.team_only()
    async def shutdown(self, ctx: commands.Context):
        await ctx.send("The bot has activated the completion process!")
        os._exit(1)

    @commands.command()
    @commands.guild_only()
    @check.team_only()
    async def subo(
        self, ctx: commands.Context, member: nextcord.Member, *, command: str
    ):
        ctx.message.author = member
        await self.bot.process_with_str(ctx.message, command)

    @commands.command()
    @check.team_only()
    async def load_extension(self, ctx: commands.Context, name):
        self.bot.load_extension(f"bot.cogs.{name}")
        await ctx.send(f"Service **{name}** successfully enabled")

    @commands.command()
    @check.team_only()
    async def unload_extension(self, ctx: commands.Context, name):
        if name=="teams":
            return
        
        self.bot.unload_extension(f"bot.cogs.{name}")
        await ctx.send(f"Service **{name}** successfully shut down")

    @commands.command()
    @check.team_only()
    async def reload_extension(self, ctx: commands.Context, name):
        self.bot.reload_extension(f"bot.cogs.{name}")
        await ctx.send(f"The **{name}** service has been successfully reloaded!")

    @commands.command()
    @check.team_only()
    async def reload_all_extensions(self, ctx: commands.Context):
        exts = self.bot.extensions
        for ext in list(exts.values()):
            name = ext.__name__
            self.bot.reload_extension(name)
        
        await ctx.send(f"All services have been successfully restarted")

    @commands.command()
    @check.team_only()
    async def extensions(self, ctx: commands.Context):
        exts = self.bot.extensions
        name_exts = [ext.__name__ for ext in exts.values()]
        string = "\n".join(name_exts)
        await ctx.send(string)


def setup(bot):
    bot.add_cog(teams(bot))
