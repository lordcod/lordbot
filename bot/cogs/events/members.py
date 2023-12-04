import nextcord
from nextcord.ext import commands

from bot.misc import utils
from bot.databases.db import GuildDateBases

class members_event(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
    
    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        gdb = GuildDateBases(member.guild.id)
        roles_ids = gdb.get('auto_roles')
        roles = [member.guild.get_role(role_id) for role_id in roles_ids]
        
        utils.remove_none(roles)
        
        member.add_roles(*roles)




def setup(bot: commands.Bot):
    event = members_event(bot)
    
    bot.add_cog(event)