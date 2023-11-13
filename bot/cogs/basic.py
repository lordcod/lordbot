import asyncio
from bot.resources import languages
from bot.misc import utils
from nextcord.ext import commands
import nextcord,random
from bot.misc import utils
from bot.databases.db import GuildDateBases
import googletrans
from nextcord.utils import find

translator = googletrans.Translator()

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

    
    @nextcord.message_command(name="Translate",default_member_permissions=8)
    async def reping(inters: nextcord.Interaction, message: nextcord.Message):
        local = find(lambda lan:lan['locale']==inters.locale,languages.Languages_information)
        result = translator.translate(text=message.content, dest=local['google_language'])
        view = nextcord.ui.View(timeout=None)
        select = nextcord.ui.Select(
            placeholder="Will choose the appropriate language:",
            min_values=1,
            max_values=1,
            options=[
                nextcord.SelectOption(
                    label=lang['native_name'],
                    description=lang['language_name'],
                    emoji=lang['flag'],
                    value=lang['google_language']
                )
                for lang in languages[:25]
            ]
        )
        
        async def _callback(_inter: nextcord.Interaction):
            result = translator.translate(text=message.content, dest=select.values[0])
            await _inter.response.send_message(content=result.text,ephemeral=True)
        select.callback = _callback
        
        view.add_item(select)
        await inters.response.send_message(content=result.text,view=view,ephemeral=True)



def setup(bot):
    bot.add_cog(basic(bot))