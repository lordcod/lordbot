import nextcord
from nextcord.ext import commands,application_checks
import io
from bot.misc import utils
from bot.resources import errors
from bot.views import views



class moderations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def say(self, ctx:commands.Context, *, message: str=None):
        files = []
        for attach in ctx.message.attachments:
            data = io.BytesIO(await attach.read())
            files.append(nextcord.File(data, attach.filename))
        
        res = await utils.generate_message(message)
        
        await ctx.send(**res,files=files)
        
        await ctx.message.delete()

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
        
        deleted = 0
        async for message in ctx.channel.history(limit=250):
            if deleted >= limit:
                break
            if message.author == member:
                await message.delete()
                deleted += 1
        
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
        async for message in message_start.channel.history(limit=250):
            if message == messsage_finish:
                finder = True
            if finder:
                deleted += 1
                await message.delete()
            if message == message_start:
                break
        
        await ctx.send(f'Deleted {deleted} message(s)',delete_after=5.0)


def setup(bot):
    bot.add_cog(moderations(bot))