import nextcord,string,random,re,orjson
from nextcord.ext import commands
from captcha.image import ImageCaptcha
from bot.resources import errors
from io import BytesIO
from PIL import Image
from bot.databases.db import GuildDateBases

class CallbackCommandError:
    def __init__(self,ctx: commands.Context,error) -> None:
        self.ctx = ctx
        self.error = error
    
    async def process(self):
        for error in self.errors:
            name = error.__name__
            if isinstance(self.error,getattr(commands,name)):
                await error(self)
                break
        else:
            await self.OfterError()
    
    async def MissingPermissions(self):
        content = "The user does not have enough rights"
    
    async def MissingRole(self):
        content = "You don't have the right role to execute the command"
    
    async def MissingAnyRole(self):
        content = "You don't have the right or the right roles to execute the command"
    
    async def BotMissingPermissions(self):
        content = "The bot doesn't have enough rights"
    
    async def CommandNotFound(self):
        content = "There is no such command"
        await self.ctx.send(content)
    
    async def CommandOnCooldown(self):
        embed = nextcord.Embed(
            title='The command is on hold',
            description=f'Repeat after {self.error.retry_after :.0f} seconds',
            colour=nextcord.Color.red()
        )
        await self.ctx.send(embed=embed, delete_after=5.0)
    
    async def NotOwner(self):
        content = "This command is intended for the bot owner"
    
    async def CheckFailure(self):
        content = "You don't fulfill all the conditions"
    
    async def BadArgument(self):
        content = "Incorrect arguments"
    
    async def OfterError(self):
        pass
    
    errors = [
        MissingPermissions,MissingRole,MissingAnyRole,BotMissingPermissions,
        CommandNotFound,CommandOnCooldown,NotOwner,CheckFailure,BadArgument,
    ]



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
