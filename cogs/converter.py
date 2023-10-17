from nextcord.ext import commands
import nextcord
from typing import *

class JoinDistanceConverter(commands.MemberConverter):
        async def convert(self, ctx, argument):
            member = await super().convert(ctx, argument)
            return member.joined_at - member.created_at

class proba(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def con(self,ctx:commands.Context,arg:JoinDistanceConverter):
        is_new = arg.delta.days < 100
        if is_new:
            await ctx.send("Hey you're pretty new!")
        else:
            await ctx.send("Hm you're not so new.")

    @commands.command()
    async def shop(self,ctx, buy_sell: Literal['buy', 'sell'], amount: Literal[1, 2], *, item: str):
        await ctx.send(f'{buy_sell.capitalize()}ing {amount} {item}(s)!')

    @commands.command()
    async def fun(self,ctx, arg: Annotated[str, lambda s: s]):
        await ctx.send(arg)

    @commands.command()
    async def slap(self,ctx, members: commands.Greedy[nextcord.Member], *, reason='no reason'):
        slapped = ", ".join(x.name for x in members)
        await ctx.send(f'{slapped} just got slapped for {reason}')

    class WebhookFlags(commands.FlagConverter):
        name: str
        message: str

    @commands.command()
    async def send(self,ctx:commands.Context, *, flags: WebhookFlags):
        webhooks = await ctx.guild.webhooks()
        webhook = get(webhooks,name=flags.name)
        if webhook.channel.permissions_for(ctx.author).manage_webhooks:
            await webhook.send(flags.message)



def setup(bot):
    bot.add_cog(proba(bot))