import nextcord
from nextcord.ext import commands
from bot.resources import errors


def team_only():
    async def predicate(ctx: commands.Context) -> bool:
        app_info: nextcord.AppInfo = await ctx.bot.application_info()
        member_teams = [member.id for member in (
            app_info.team.members if app_info.team else [app_info.owner])]
        if ctx.author.id not in member_teams:
            raise errors.OnlyTeamError(author=ctx.author)
        return True
    return commands.check(predicate)
