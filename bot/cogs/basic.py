import asyncio
from bot.resources import languages
from bot.misc import utils
from nextcord.ext import commands
import nextcord,random
from bot.misc import utils
from bot.databases.db import GuildDateBases

class basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def captcha(self, ctx:commands.Context):
        lang = GuildDateBases(ctx.guild.id).language
        data,text = await utils.generator_captcha(random.randint(3,7))
        image_file = nextcord.File(data,filename="cap.png",description="Captcha",spoiler=True)
        await ctx.send(content=languages.captcha.enter[lang],file=image_file)
        try:
            check = lambda m: m.channel==ctx.channel and m.author==ctx.author
            mes:nextcord.Message = await self.bot.wait_for("message",timeout=30,check=check)
        except asyncio.TimeoutError:
            await ctx.send(content=languages.captcha.failed[lang])
            return
        
        if mes.content.lower() == text.lower():
            await ctx.send(f"{languages.Emoji.congratulation}{languages.captcha.congratulation[lang]}")
        else:
            await ctx.send(content=languages.captcha.failed[lang])

    @commands.command()
    async def ping(self,ctx: commands.Context):
        await ctx.send(f"Pong!🥍🎉")




def setup(bot):
    bot.add_cog(basic(bot))