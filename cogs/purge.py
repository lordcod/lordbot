import nextcord
from nextcord.ext import commands

content_type_list = {
    "pdf":["application/pdf"],
    "zip":["application/zip"],
    "audio":["audio/mpeg","audio/ogg"],
    "image":["image/avif","image/jpeg","image/png","image/svg+xml"],
    "text":["text/plain""text/css","text/csv","text/html","text/javascript(.js)","text/xml"],
}

class purges(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def purge(self,ctx: commands.Context, limit: int):
        deleted = await ctx.channel.purge(limit=limit)
        await ctx.send(f'Deleted {len(deleted)} message(s)',delete_after=5.0)

    @commands.command()
    async def user(self,ctx: commands.Context,member: nextcord.Member,limit: int):
        if limit > 100:
            raise CommandError("The maximum number of messages to delete is `100`")
        
        deleted = 0
        async for message in ctx.channel.history(limit=250):
            if deleted >= limit:
                break
            if message.author == member:
                await message.delete()
                deleted += 1
        
        await ctx.send(f'Deleted {deleted} message(s)',delete_after=5.0)

    @commands.command()
    async def between(self,ctx: commands.Context, message_start:nextcord.Message, messsage_finish:nextcord.Message=None):
        if not messsage_finish:
            messsage_finish = (await message_start.channel.history(limit=1).flatten())[0]
        if message_start.channel != messsage_finish.channel:
            raise CommandError("Channel error")
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

    @commands.command()
    async def type(self,ctx: commands.Context,content_type: str,limit: int):
        if limit > 100:
            raise CommandError("The maximum number of messages to delete is `100`")
        elif content_type not in content_type_list:
            raise CommandError("The content type parameter is specified incorrectly")
        cto = content_type_list[content_type]
        
        deleted = 0
        async for message in ctx.channel.history(limit=250):
            if deleted >= limit:
                break
            for attach in message.attachments:
                if attach.content_type in cto:
                    deleted += 1
                    await message.delete()
        
        await ctx.send(f'Deleted {deleted} message(s)',delete_after=5.0)




def setup(bot):
    bot.add_cog(purges(bot))