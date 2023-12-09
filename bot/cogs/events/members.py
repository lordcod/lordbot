import nextcord
from nextcord.ext import commands

from bot.misc import utils
from bot.misc.logger import Logger
from bot.databases.db import GuildDateBases

import asyncio


class members_event(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
    
    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        gdb = GuildDateBases(member.guild.id)
        
        tasks = [
            self.auto_roles(member, gdb),
            self.auto_message(member, gdb)
        ]
        
        await asyncio.gather(*tasks)
    
    
    def on_error(func):
        async def wrapped(self, member, gdb):
            try:
                result = await func(self, member, gdb)
                return result
            except Exception as err:
                Logger.error(err)
        return wrapped
    
    @on_error
    async def auto_roles(self, member: nextcord.Member, gdb: GuildDateBases):
        roles_ids = gdb.get('auto_roles')
        
        if not roles_ids:
            return
        
        roles = [member.guild.get_role(role_id) for role_id in roles_ids]
        
        utils.remove_none(roles)
        
        await member.add_roles(*roles,atomic=False)
    
    @on_error
    async def auto_message(self, member: nextcord.Member, gdb: GuildDateBases):
        guild = member.guild
        greeting_message: dict = gdb.get('greeting_message')
        
        if not greeting_message:
            return
        
        
        channel_id: int = greeting_message.get("channel_id")
        channel = guild.get_channel(channel_id)
        
        if not channel:
            return
        
        
        member_payload = utils.MemberPayload(member)
        guild_payload = utils.GuildPayload(guild)
        data_payload = guild_payload|member_payload
        
        content: str = greeting_message.get('message')
        
        templete = utils.GreetingTemplate(content)
        message_format = templete.safe_substitute(data_payload)
        message_data = await utils.generate_message(message_format)
        
        await channel.send(**message_data)




def setup(bot: commands.Bot):
    event = members_event(bot)
    
    bot.add_cog(event)