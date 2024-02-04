import nextcord
from nextcord.ext import commands,application_checks

from bot.misc import utils
from bot.views import settings_menu
from bot.databases.db import RoleDateBases, GuildDateBases
from bot.resources.ether import Emoji

import io
import asyncio
import time
from typing import Optional

class moderations(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def say(self, ctx:commands.Context, *, message: str):
        files = []
        for attach in ctx.message.attachments:
            data = io.BytesIO(await attach.read())
            files.append(nextcord.File(data, attach.filename))
        
        res = await utils.generate_message(message)
        
        await ctx.send(**res,files=files)
        
        await ctx.message.delete()

    
    @commands.command(aliases=["set","setting"])
    @commands.has_permissions(manage_guild=True)
    async def settings(self, ctx: commands.Context):
        view = settings_menu.SettingsView(ctx.author)
        
        await ctx.send(embed=view.embed,view=view)


    @commands.group(name='temp-role',invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    async def temp_role(
        self, 
        ctx: commands.Context, 
        member: nextcord.Member, 
        roles: commands.Greedy[nextcord.Role],
        stime: Optional[str] = None
    ):
        await member.add_roles(*roles)
        
        if stime is not None:
            rsdb = RoleDateBases(ctx.guild.id, member.id)
            ftime = utils.calculate_time(stime)
            if ftime is None:
                await ctx.send("The role was given forever because you specified the wrong amount of time")
                return
            
            
            for role in roles:
                data = {
                    'time': int(time.time()+ftime),
                    'role_id': role.id
                }
                rsdb.add(data)
                
                self.bot.loop.call_later(ftime, asyncio.create_task, member.remove_roles(role))
                self.bot.loop.call_later(ftime, asyncio.create_task, rsdb.aremove(data))
        
        await ctx.send(f"{Emoji.congratulation}The roles were issued successfully")

    @temp_role.command(name='list')
    async def temp_role_list(self, ctx: commands.Context, member: Optional[nextcord.Member] = None):
        gdb = GuildDateBases(ctx.guild.id)
        color = gdb.get('color')
        
        if member is not None:
            rsdb = RoleDateBases(ctx.guild.id, member.id)
            predata = rsdb.get_as_member()
            datas = [predata] if predata else []
        else:
            rsdb = RoleDateBases(ctx.guild.id)
            datas = rsdb.get_as_guild()
        
        quantity = 0
        message = ""
        
        for dat in datas:
            member_id = dat[1]
            roles_data = dat[2]
            
            for rol_data in roles_data:
                quantity += 1
                
                time = rol_data.get("time")
                role_id = rol_data.get("role_id")
                
                member = ctx.guild.get_member(member_id)
                role = ctx.guild.get_role(role_id)
                
                message += f"{quantity}. {member.mention} → {role.mention} (<t:{time}:R>)\n"
        
        message = message or "There are no registered temporary roles on this server"
        embed = nextcord.Embed(
            title="Temp Roles",
            description=message,
            color=color
        )
        
        await ctx.send(embed=embed)
    
    
    @nextcord.slash_command(
        name='clone',
        default_member_permissions=268435456
    )
    async def clone(
        self,
        interaction: nextcord.Interaction
    ) -> None:
        pass

    @clone.subcommand(
        name='role',
        description='If you want to copy the role but still keep the rights, then this is the command for you'
    )
    async def clone_role(
        self,
        interaction: nextcord.Interaction,
        role: nextcord.Role = nextcord.SlashOption(
            name='role',
            description='Select the role you want to copy',
            required=True
        ),
        name: str = nextcord.SlashOption(
            name='name',
            description='When creating a new role, this name will be specified',
            required=False
        )
    ) -> None:
        role_name = name or role.name
        
        new_role = await interaction.guild.create_role(
            reason="Copying a role with rights",
            name=role_name,
            permissions=role.permissions,
            color=role.color,
            hoist=role.hoist,
            mentionable=role.mentionable,
            icon=role.icon
        )
        
        await interaction.response.send_message(f'Successfully created a new role - {new_role.mention}', ephemeral=True)


    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self,ctx: commands.Context, limit: int):
        if limit > 200:
            raise commands.CommandError("The maximum number of messages to delete is `100`")
        
        deleted = await ctx.channel.purge(limit=limit)
        await ctx.send(f'Deleted {len(deleted)} message(s)',delete_after=5.0)

    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def user(self,ctx: commands.Context,member: nextcord.Member,limit: int):
        if limit > 100:
            raise commands.CommandError("The maximum number of messages to delete is `100`")
        
        messages = []
        
        minimum_time = int((time.time() - 14 * 24 * 60 * 60) * 1000.0 - 1420070400000) << 22
        
        async for message in ctx.channel.history(limit=250):
            if len(messages) >= limit:
                break
            if message.author == member:
                messages.append(message)
            
            if message.id < minimum_time:
                break
        
        await ctx.channel.delete_messages(messages)
        
        await ctx.send(f'Deleted {len(messages)} message(s)',delete_after=5.0)

    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def between(self,ctx: commands.Context, message_start:nextcord.Message, messsage_finish:nextcord.Message=None):
        if messsage_finish and message_start.channel != messsage_finish.channel:
            raise commands.CommandError("Channel error")
        
        messages = []
        finder = False
        minimum_time = int((time.time() - 14 * 24 * 60 * 60) * 1000.0 - 1420070400000) << 22
        
        async for message in message_start.channel.history(limit=100):
            if not messsage_finish:
                messsage_finish = message
            
            if message == messsage_finish:
                finder = True
            
            if finder:
                messages.append(message)
            
            if message == message_start or len(messages) >= 50 or message.id < minimum_time:
                break
        
        await ctx.channel.delete_messages(messages)
        
        await ctx.send(f'Deleted {len(messages)} message(s)',delete_after=5.0)


def setup(bot: commands.Bot):
    bot.add_cog(moderations(bot))