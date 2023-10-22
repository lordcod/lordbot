import nextcord
from nextcord.ext import commands

class tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx: commands.Context):
        if ctx.channel.type!=nextcord.enums.ChannelType.public_thread:
            return
        if ctx.channel.parent.type!=nextcord.enums.ChannelType.forum:
            return
        print("yes")
    
    @tag.command()
    async def add(self,ctx: commands.Context, tag_name):
        pass
    
    @tag.command()
    async def remove(self,ctx: commands.Context, tag_name):
        pass
    
    @tag.command()
    async def set(self,ctx: commands.Context, tag_name):
        pass


def setup(bot):
    bot.add_cog(tags(bot))