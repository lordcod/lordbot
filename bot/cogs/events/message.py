import nextcord
from nextcord.ext import commands

from bot.databases.db import GuildDateBases
from bot.views.views import TranslateView
from bot.languages import BotInfo

import googletrans

translator = googletrans.Translator()

class Reactions:
    def __init__(self, message: nextcord.Message, data: list) -> None:
        self.message = message
        self.data = data
    
    async def process(self):
        message = self.message
        data = self.data
        
        if not isinstance(data, list):        
            return
        
        for reat in data:
            await message.add_reaction(reat)


class Translates:
    def __init__(
        self,
        message: nextcord.Message, 
        data: dict, 
        color: int,
        lang:str,
    ) -> None:
        self.mes = message
        self.data = data
        self.color = color
        self.lang = lang
    
    async def process(self):
        data = self.data
        type = data.get('type')
        dest = data.get('dest')
        whitelist = data.get('whitelist')
        
        func = self.select_types.get(type)
        await func(self, dest, whitelist)
    
    
    async def message(self,dest,whitelist):
        mes = self.mes
        color  = self.color
        
        result = translator.translate(
            text=mes.content,
            dest=dest
        )
        if result.src in whitelist:
            return
        
        view = TranslateView(mes.guild.id)
        
        embed = nextcord.Embed(
            title='Auto Translator',
            description=result.text,
            color=color
        )
        embed.set_author(
            name=mes.author.display_name,
            icon_url=mes.author.display_avatar
        )
        
        await mes.channel.send(mes.content,embed=embed,view=view)
        await mes.delete()

    select_types = {
        'message':message
    }

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
        
        color = guild_data.get('color')
        lang = guild_data.get('language')
        prefix = guild_data.get('prefix')
        locale = guild_data.get('language')
        
        reactions: dict = guild_data.get('reactions')
        auto_translate: dict = guild_data.get('auto_translate')
        
        data_reactions = reactions.get(message.channel.id)
        data_translate = auto_translate.get(message.channel.id)
        
        if data_reactions:
            reaction_handelers = Reactions(message,data_reactions)
            await reaction_handelers.process()
        
        if data_translate:
            translate_handelers = Translates(message,data_translate,color,lang)
            # await translate_handelers.process()
        
        if message.content.strip() == self.bot.user.mention:
            embed = nextcord.Embed(
                title=f'{self.bot.user.display_name} — {BotInfo.title.get(locale)}',
                description=BotInfo.description.get(locale),
                color=color
            )
            embed.add_field(
                name=BotInfo.info_server.get(locale),
                value=f'> {BotInfo.prefix_server.get(locale)} - `{prefix}`'
            )
            
            await message.channel.send(embed=embed)
        
        



def setup(bot: commands.Bot):
    event = message_event(bot)
    
    bot.add_cog(event)