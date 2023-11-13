import nextcord,string,random,re,orjson
from nextcord.ext import commands
from captcha.image import ImageCaptcha
from bot.resources import errors
import aiohttp
from io import BytesIO
from PIL import Image
from bot.databases.db import GuildDateBases

async def getRandomQuote(lang='en'):
    url = f"https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang={lang}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as responce:
            json = await responce.json()
            return json

def get_prefix(guild_id):
    gdb = GuildDateBases(guild_id)
    prefix = gdb.get('prefix')
    return prefix

async def get_webhook(channel: nextcord.TextChannel, user) -> nextcord.Webhook:
    if channel.type.value not in [0,2,5,13]:
        raise  errors.ErrorTypeChannel("Channel error")
    
    webhooks = await channel.webhooks()
    for wh in webhooks:
        if wh.user==user:
            return wh
    else:
        wh = await channel.create_webhook(name=user.name)
        return wh

def is_builtin_class_instance(obj):
    return obj in (str, int, float, bool)

def clord(value,cls,default=None):
        if type(value) == cls:
            return value
        
        if not is_builtin_class_instance(cls):
            return default
        
        try:
            return cls(value)
        except:
            return default

async def generate_message(content):
    message = {}
    try:
        content: dict = orjson.loads(content)
        
        message['content'] = content.get('plainText',None)
        embed = nextcord.Embed(
            title=content.get('title',None),
            description=content.get('description',None),
            color=content.get('color',None),
            url=content.get('url',None),
        )
        
        thumbnail = content.get('thumbnail')
        if thumbnail:
            embed.set_thumbnail(thumbnail)
        
        author = content.get('author',{})
        if author:
            embed.set_author(
                name=author.get('name',None),
                url=author.get('url',None),
                icon_url=author.get('icon_url',None),
            )
        
        footer = content.get('footer',None)
        if footer:
            embed.set_footer(
                text=footer.get('text'),
                icon_url=footer.get('icon_url'),
            )
        
        fields = content.get('fields',[])
        for field in fields:
            embed.add_field(
                name=field.get('name',None),
                value=field.get('value',None),
                inline=field.get('inline',None)
            )
        message['embed'] = embed
    except orjson.JSONDecodeError:
        message['content'] = content
    return message

async def check_invite(content):
    regex_string = '(https:\/\/discord.gg\/|https:\/\/discord.com\/invite\/)([a-zA-Z0-9_-]+)(\/|\s|\?|$)'
    pattern = re.fullmatch(regex_string,content)
    if pattern:
        return pattern.groups()[1]

async def generator_captcha(num):
    text = "".join([random.choice(string.ascii_uppercase) for _ in range(num)])
    captcha_image = ImageCaptcha(
        width=400,
        height=220,
        font_sizes=(40,70,100)
    )
    data:BytesIO = captcha_image.generate(text)
    return data,text
