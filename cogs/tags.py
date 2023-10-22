import nextcord
from nextcord.ext import commands

class tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def is_post(ctx: commands.Context):
        if ctx.channel.type!=nextcord.enums.ChannelType.public_thread:
            raise Exception('No post')
        if ctx.channel.parent.type!=nextcord.enums.ChannelType.forum:
            raise Exception('No forum')
        return True

    @commands.group(invoke_without_command=False)
    @commands.check(is_post)
    async def tag(self, ctx: commands.Context):
        pass
    
    @tag.command()
    async def add(self,ctx: commands.Context,*,tag_name):
        await ctx.message.delete()
        tags = ctx.channel.applied_tags
        for tagn in ctx.channel.parent.available_tags:
            if tagn.name.lower() == tag_name.lower():
                tag = tagn
        if tag not in tags:
            tags.append(tag)
        await ctx.channel.edit(applied_tags=tags)
    
    @tag.command()
    async def remove(self,ctx: commands.Context,*,tag_name):
        await ctx.message.delete()
        tags = ctx.channel.applied_tags
        tag = None
        for tagn in ctx.channel.parent.available_tags:
            if tagn.name.lower() == tag_name.lower():
                tag = tagn
        if tag in tags:
            tags.remove(tag)
        await ctx.channel.edit(applied_tags=tags)



def setup(bot):
    bot.add_cog(tags(bot))