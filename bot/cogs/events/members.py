import nextcord
from nextcord.ext import commands

from bot.misc import utils
from bot.misc.logger import Logger
from bot.databases.db import GuildDateBases



class members_event(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
    
    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        gdb = GuildDateBases(member.guild.id)
        
        await self.auto_roles(member, gdb)
        await self.auto_message(member, gdb)
    
    async def auto_roles(self, member: nextcord.Member, gdb: GuildDateBases):
        roles_ids = gdb.get('auto_roles')
        
        if not roles_ids:
            return
        
        roles = [member.guild.get_role(role_id) for role_id in roles_ids]
        
        utils.remove_none(roles)
        
        await member.add_roles(*roles,atomic=False)
    
    async def auto_message(self, member: nextcord.Member, gdb: GuildDateBases):
        requst: dict = gdb.get('greeting_message')
        
        if not requst:
            return
        
        guild = member.guild
        
        member_payload = utils.MemberPayload(member)
        guild_payload = utils.GuildPayload(guild)
        
        channel_id: int = requst.get("channel_id")
        channel = self.bot.get_channel(channel_id)
        
        message_payload: str = requst.get("message")
        message_format_json = message_payload.format(
            member=member_payload,
            guild=guild_payload
        )
        
        message = await utils.generate_message(message_format_json)
        
        Logger.info(message)
        
        await channel.send(**message)




def setup(bot: commands.Bot):
    event = members_event(bot)
    
    bot.add_cog(event)