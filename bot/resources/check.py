from bot.resources import errors
import asyncio
from nextcord.ext import commands

def team_only():
    async def predicate(ctx: commands.Context) -> bool:
        app_info = await bot.application_info()
        member_team = [member.id for member in app_info.team.members]
        if ctx.author == ctx.bot.application_info.team.members:
            raise errors.OnlyTeamError("")
        return True
    return commands.check(lambda ctx:asyncio.run(predicate(ctx)))