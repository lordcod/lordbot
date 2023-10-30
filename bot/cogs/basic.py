from nextcord.ext import commands
import nextcord
from bot.misc import utils

class basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def captcha(ctx:commands.Context):
        lang = guilds(ctx.guild.id).get_lang()
        data,text = await recaptcha.generator(random.randint(3,7))
        image_file = nextcord.File(data,filename="cap.png",description="Captcha",spoiler=True)
        await ctx.send(content=languages.captcha.enter[lang],file=image_file)
        try:
            check = lambda m: m.channel==ctx.channel and m.author==ctx.author
            mes:nextcord.Message = await bot.wait_for("message",timeout=30,check=check)
        except asyncio.TimeoutError:
            await ctx.send(content=languages.captcha.failed[lang])
            return
        
        if mes.content.lower() == text.lower():
            await ctx.send(f"{languages.Emoji.congratulation}{languages.captcha.congratulation[lang]}")
        else:
            await ctx.send(content=languages.captcha.failed[lang])

    @commands.command()
    async def ping(self,ctx: commands.Context):
        await ctx.send(f"Pong!🥍🎉\n{ctx.author.name}")




def setup(bot):
    bot.add_cog(basic(bot))