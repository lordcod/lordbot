import nextcord
from nextcord.ext import commands

from bot.misc import logstool
from bot.misc.lordbot import LordBot


class RolesEvent(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_member_update(self, before: nextcord.Member, after: nextcord.Member):
        if set(before.roles)-set(after.roles):
            role = list(set(before.roles)-set(after.roles))[0]
            await logstool.pre_remove_role(after, role)
        if set(after.roles)-set(before.roles):
            role = list(set(after.roles)-set(before.roles))[0]
            await logstool.pre_add_role(after, role)


def setup(bot):
    bot.add_cog(RolesEvent(bot))
