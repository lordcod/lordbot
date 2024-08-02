from os import environ
import nextcord
from nextcord.ext import commands

from bot.databases import localdb
from bot.misc.lordbot import LordBot
from bot.resources import errors
from bot.resources.ether import Emoji


class Teams(commands.Cog):
    def __init__(self, bot: LordBot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> bool:
        app_info = await self.bot.application_info()
        self.bot.owner_ids
        member_teams = [member.id for member in (
            app_info.team.members)] if app_info.team else [app_info.owner]
        if ctx.author.id not in member_teams:
            raise errors.OnlyTeamError(author=ctx.author)
        return True

    @commands.command()
    async def shutdown(self, ctx: commands.Context):
        await self.bot._LordBot__session.close()
        await localdb._update_db(__name__)
        await localdb.cache.close()

        conn = self.bot.engine._DataBase__connection
        if conn and not conn.closed:
            conn.close()

        await ctx.send("The bot has activated the completion process!")
        await self.bot.close()

    @commands.command(aliases=['sudo'])
    @commands.guild_only()
    async def subo(
        self, ctx: commands.Context, member: nextcord.Member, *, command: str
    ):
        ctx.message.author = member
        await self.bot.process_with_str(ctx.message, command)

    @commands.command(aliases=['load_cog'])
    async def load_extension(self, ctx: commands.Context, name):
        self.bot.load_extension(f"bot.cogs.{name}")
        await ctx.send(f"Service **{name}** successfully enabled")

    @commands.command(aliases=['api_config'])
    async def get_api_config(self, ctx: commands.Context):
        api = self.bot.apisite
        if not api.is_running():
            return

        await ctx.send('ApiSite is worked\n'
                       f'Public url: {api.callback_url}\n'
                       f'Password: {api.password}')

    @commands.command()
    async def update_api_config(self, ctx: commands.Context):
        await self.bot.update_api_config()

    @commands.command(aliases=['unload_cog'])
    async def unload_extension(self, ctx: commands.Context, name):
        if name == "teams":
            return

        self.bot.unload_extension(f"bot.cogs.{name}")
        await ctx.send(f"Service **{name}** successfully shut down")

    @commands.command(aliases=['reload_cog'])
    async def reload_extension(self, ctx: commands.Context, name):
        self.bot.reload_extension(f"bot.cogs.{name}")
        await ctx.send(f"The **{name}** service has been successfully reloaded!")

    @commands.command(aliases=['reload_cogs', 'reload_all_cogs'])
    async def reload_all_extensions(self, ctx: commands.Context):
        exts = self.bot.extensions
        for ext in exts.values():
            name = ext.__name__
            self.bot.reload_extension(name)

        await ctx.send("All services have been successfully restarted")

    @commands.command(aliases=['cogs'])
    async def extensions(self, ctx: commands.Context):
        exts = self.bot.extensions
        name_exts = [ext.__name__ for ext in exts.values()]
        string = "\n".join(name_exts)
        await ctx.send(string)

    @commands.command()
    async def sql_execute(
        self,
        ctx: commands.Context,
        *,
        query: str
    ):
        self.bot.engine.execute(query)
        await ctx.message.add_reaction(Emoji.success)

    @commands.command(aliases=['update_db'])
    async def update_redis(
        self,
        ctx: commands.Context
    ):
        await localdb._update_db(__name__)
        await ctx.message.add_reaction(Emoji.success)


def setup(bot):
    bot.add_cog(Teams(bot))
