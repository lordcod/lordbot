import nextcord
from nextcord.ext import commands

from bot.databases.db import GuildDateBases
from bot.misc import utils
from bot.resources import errors
from bot import languages

import googletrans

translator = googletrans.Translator()


class message_event(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
    
    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return
        
        guild_data = GuildDateBases(message.guild.id)
        colour = guild_data.get('color')
        reactions = guild_data.get('reactions')
        auto_translate = guild_data.get('auto_translate')
        lang = guild_data.get('language')
        prefix = utils.get_prefix(message.guild.id,markdown=False)
        
        if message.channel.id in reactions:
            for react in reactions[message.channel.id]:
                await message.add_reaction(react)
        
        if message.channel.id in auto_translate:
            result = translator.translate(message.content,dest=auto_translate[message.channel.id])
            if result.src != auto_translate:
                embed = nextcord.Embed(
                    title="",
                    description=f'### {result.text}',
                    color=colour
                )
                embed._fields = [
                    {
                        'name':f'{languages.auto_translate.field_name_from.get(lang)} {googletrans.LANGUAGES[result.src]}',
                        'value':f'',
                        'inline':True
                    },
                    {
                        'name':f'{languages.auto_translate.field_name_to.get(lang)} {googletrans.LANGUAGES[result.dest]}',
                        'value':f'',
                        'inline':True
                    },
                ]
                embed.set_footer(text='Performed with LordBot',icon_url=self.bot.user.avatar.url)
                await message.channel.send(embed=embed)
        
        if message.content.strip() == self.bot.user.mention:
            embed = nextcord.Embed(
                title=f'{self.bot.user.display_name} — это многофункциональный бот',
                description=(
                    f'Бот предназначен для облегчения управления сервером и оснащен различными средствами автоматизации'
                ),
                color=colour
            )
            embed.add_field(
                name='Информация о сервере',
                value=f'> Префикс сервера - `{prefix}`'
            )
            
            await message.channel.send(embed=embed)
    

    
    


def setup(bot: commands.Bot):
    event = message_event(bot)
    
    bot.add_cog(event)