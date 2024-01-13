import nextcord
from nextcord.ext import commands

from bot.misc import utils
from bot.misc.logger import Logger
from bot.databases.db import GuildDateBases, EconomyMembedDB

import time
import asyncio

def on_error(func):
    async def wrapped(self, member, gdb):
        try:
            result = await func(self, member, gdb)
            return result
        except Exception as err:
            Logger.error(err)
    return wrapped

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
    
    @on_error
    async def auto_roles(self, member: nextcord.Member, gdb: GuildDateBases):
        roles_ids = gdb.get('auto_roles')
        
        if not roles_ids:
            return
        
        roles = [member.guild.get_role(role_id) for role_id in roles_ids]
        
        utils.remove_none(roles)
        
        await member.add_roles(*roles, atomic=False)
    
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
        
        
        member_payload = utils.MemberPayload(member).to_dict()
        guild_payload = utils.GuildPayload(guild).to_dict()
        data_payload = guild_payload|member_payload
        
        content: str = greeting_message.get('message')
        
        templete = utils.GreetingTemplate(content)
        message_format = templete.safe_substitute(data_payload)
        message_data = await utils.generate_message(message_format)
        
        await channel.send(**message_data)
    
    
    @commands.Cog.listener()
    async def on_member_update(self, before: nextcord.Member, after: nextcord.Member, *, timeout: float = None):
        if timeout is not None:
            await self.tmoutmm(f"Прошел {after.name} - {timeout}")
        elif (
            before.communication_disabled_until is not None and
            after.communication_disabled_until is None
        ):
            await self.process_untimeout(before, after)
        elif (
            before.communication_disabled_until is None and
            after.communication_disabled_until is not None
        ):
            await self.process_timeout(before, after)
    
    async def tmoutmm(self, t):
        print(t)
    
    async def process_untimeout(self, before: nextcord.Member, after: nextcord.Member):
        if not hasattr(self.bot, 'timeouts'):
            return
        
        if self.bot.timeouts[after.id] is None:
            return
        
        self.bot.dispatch("member_update", before, after, timeout=self.bot.timeouts[after.id][0])
        
        self.bot.timeouts[after.id] = None
    
    async def process_timeout(self, before: nextcord.Member, after: nextcord.Member):
        timing = after.communication_disabled_until.timestamp()
        temp = timing-time.time()
        
        if not hasattr(self.bot, 'timeouts'):
            self.bot.timeouts = {}
        
        self.bot.timeouts[after.id] = (temp, timing)
        self.bot.loop.call_later(temp, asyncio.create_task, self.process_untimeout(before, after))
    
    
    
    @commands.command()
    async def istimeout(self, ctx: commands.Context, member: nextcord.Member):
        await ctx.send(f"{member.name} - {member.communication_disabled_until: '%m-%d-%Y %H:%M:%S'}")



def setup(bot: commands.Bot):
    event = members_event(bot)
    
    bot.add_cog(event)