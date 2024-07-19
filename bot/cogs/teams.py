import nextcord
from nextcord.ext import commands

from bot.databases import localdb
from bot.misc.lordbot import LordBot
from bot.resources import check
from bot.resources.ether import Emoji


class Teams(commands.Cog):
    def __init__(self, bot: LordBot):
        self.bot = bot

    @commands.command()
    @check.team_only()
    async def shutdown(self, ctx: commands.Context):
        await ctx.send("The bot has activated the completion process!")
        self.bot.dispatch('disconnect')
        await self.bot.close()

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
    async def get_api_config(self, ctx: commands.Context):
        api = self.bot.apisite
        await ctx.send('ApiSite is worked\n'
                       f'Public url: {api.callback_url}\n'
                       f'Password: {api.password}')

    @commands.command()
    @check.team_only()
    async def unload_extension(self, ctx: commands.Context, name):
        if name == "teams":
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
        for ext in exts.values():
            name = ext.__name__
            self.bot.reload_extension(name)

        await ctx.send("All services have been successfully restarted")

    @commands.command()
    @check.team_only()
    async def extensions(self, ctx: commands.Context):
        exts = self.bot.extensions
        name_exts = [ext.__name__ for ext in exts.values()]
        string = "\n".join(name_exts)
        await ctx.send(string)

    @commands.command()
    @check.team_only()
    async def sql_execute(
        self,
        ctx: commands.Context,
        *,
        query: str
    ):
        self.bot.engine.execute(query)
        await ctx.message.add_reaction(Emoji.success)

    @commands.command()
    @check.team_only()
    async def update_redis(
        self,
        ctx: commands.Context
    ):
        await localdb._update_db(__name__)
        await ctx.message.add_reaction(Emoji.success)


def setup(bot):
    bot.add_cog(Teams(bot))
