from bot.resources import errors
import asyncio
from nextcord.ext import commands

def team_only():
    async def predicate(ctx: commands.Context) -> bool:
        try:
            app_info = await ctx.bot.application_info()
            member_teams = [member.id for member in app_info.team.members]
            if ctx.author.id not in member_teams:
                raise errors.OnlyTeamError("This command can only be used by the bot team")
            return True
        except:
            if ctx.author != ctx.bot.owner:
                raise errors.OnlyTeamError("This command can only be used by the bot team")
            return True
    return commands.check(predicate)

