import nextcord
from nextcord.ext import commands,application_checks

from bot.misc import utils
from bot.resources import errors
from bot.views import views

import io
import asyncio



class moderations(commands.Cog):
    def __init__(self, bot):
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
    @commands.guild_only()
    async def settings(self, ctx: commands.Context):
        view = views.SettingsView(ctx.author)
        
        await ctx.send(embed=view.embed,view=view)

    @nextcord.slash_command(
        name='clone',
        guild_ids=[1179069504186232852]
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
            colour=role.colour,
            hoist=role.hoist,
            mentionable=role.mentionable,
            icon=role.icon
        )
        
        await interaction.response.send_message(f'Successfully created a new role - {new_role.mention}', ephemeral=True)

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self,ctx: commands.Context, limit: int):
        deleted = await ctx.channel.purge(limit=limit)
        await ctx.send(f'Deleted {len(deleted)} message(s)',delete_after=5.0)

    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def user(self,ctx: commands.Context,member: nextcord.Member,limit: int):
        if limit > 100:
            raise commands.CommandError("The maximum number of messages to delete is `100`")
        
        tasks = []
        
        deleted = 0
        async for message in ctx.channel.history(limit=250):
            if deleted >= limit:
                break
            if message.author == member:
                
                task = asyncio.ensure_future(message.delete())
                tasks.append(task)
                
                deleted += 1
        
        await asyncio.wait(tasks)
        
        await ctx.send(f'Deleted {deleted} message(s)',delete_after=5.0)

    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def between(self,ctx: commands.Context, message_start:nextcord.Message, messsage_finish:nextcord.Message=None):
        if not messsage_finish:
            messsage_finish = (await message_start.channel.history(limit=1).flatten())[0]
        if message_start.channel != messsage_finish.channel:
            raise commands.CommandError("Channel error")
        deleted = 0
        finder = False
        async for message in message_start.channel.history(limit=100):
            if message == messsage_finish:
                finder = True
            if finder:
                deleted += 1
                await message.delete()
            if message == message_start or deleted >= 50:
                break
        
        await ctx.send(f'Deleted {deleted} message(s)',delete_after=5.0)


def setup(bot: commands.Bot):
    bot.add_cog(moderations(bot))