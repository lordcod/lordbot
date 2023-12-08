from typing import Any
import nextcord
from nextcord.ext import commands
from nextcord.utils import escape_markdown

from bot.resources import errors
from bot.databases.db import GuildDateBases

import re
import string
import random
import aiohttp
import orjson

from datetime import datetime
from captcha.image import ImageCaptcha
from io import BytesIO


class GuildPayload:
    guild: nextcord.Guild
    
    def __init__(self, guild: nextcord.Guild) -> None:
        self.guild = guild
    
    @property
    def id(self) -> int:
        return self.guild.id
    
    @property
    def name(self) -> str:
        return self.guild.name
    
    @property
    def icon(self) -> str:
        guild = self.guild
        if not (guild.icon and guild.icon.url):
            return None
        return guild.icon.url
    
    @property
    def memberCount(self) -> int:
        return self.guild.member_count
    
    @property
    def createdAt(self) -> datetime:
        return self.guild.created_at
    
    @property
    def premiumSubscriptionCount(self) -> int:
        return self.guild.premium_subscription_count


    def to_dict(self):
        starter = 'guild.'
        ret = {
            f'{starter}id':self.id,
            f'{starter}name':self.name,
            f'{starter}icon':self.icon,
            f'{starter}memberCount':self.memberCount,
            f'{starter}createdAt':self.createdAt,
            f'{starter}premiumSubscriptionCount':self.premiumSubscriptionCount,
        }
        
        return ret

    def __getattr__(self, name: str) -> Any:
        return f'{"{"}{name}{"}"}'
    
    def __str__(self) -> str:
        return self.name

class MemberPayload:
    member: nextcord.Member
    
    def __init__(self, member: nextcord.Member) -> None:
        self.member = member
    
    @property
    def id(self) -> int:
        return self.member.id
    
    @property
    def mention(self) -> str:
        return self.member.mention
    
    @property 
    def username(self) -> str:
        return self.member.name
    
    @property 
    def displayName(self) -> str:
        return self.member.display_name
    
    @property
    def discriminator(self) -> int:
        return self.member.discriminator
    
    @property
    def tag(self) -> str:
        member = self.member
        tag = f'{member.name}#{member.discriminator}'
        return tag
    
    @property
    def avatar(self) -> str:
        member = self.member
        if not (member.display_avatar and member.display_avatar.url):
            return None
        return member.display_avatar.url
    
    
    def to_dict(self):
        starter = 'member.'
        ret = {
            f'{starter}id':self.id,
            f'{starter}mention':self.mention,
            f'{starter}username':self.username,
            f'{starter}displayName':self.displayName,
            f'{starter}discriminator,':self.discriminator,
            f'{starter}tag':self.tag,
            f'{starter}avatar':self.avatar,
        }
        
        return ret
    
    def __getattr__(self, name: str) -> str:
        return f'{"{"}{name}{"}"}'

    def __str__(self) -> str:
        return self.tag

class GreetingTemplate(string.Template):
    pattern = r'''
        \{(?:
        (?P<escaped>\{) |
        (?P<named>[\._a-z][\._a-z0-9]*)\} |
        (?P<braced>[\._a-z][\._a-z0-9]*)\} |
        (?P<invalid>)
        )
    '''


async def getRandomQuote(lang='en'):
    url = f"https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang={lang}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as responce:
            json = await responce.json()
            return json

def remove_none(dlist: list) -> None:
    for arg in dlist:
        if arg is None:
            dlist.remove(arg)

def is_emoji(emoji):
    pattern = ":(.+):"
    check = re.fullmatch(pattern,emoji)
    
    if not check:
        return False
    
    groups = check.groups()
    payload = {
        'name':groups[0],
        'id':groups[1]
    }
    return payload

def to_color(colour: int) -> str:
    color = hex(colour).replace('0x', '#').upper()
    return color

def from_color(color: str) -> int:
    colour = int(color[1:], 16)
    return colour

def get_prefix(guild_id: int, *, markdown: bool = False, GuildData: GuildDateBases = None) -> str:
    gdb = GuildData or GuildDateBases(guild_id)
    prefix = gdb.get('prefix')
    if markdown:
        return escape_markdown(prefix)
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

async def generate_message(content) -> dict|str:
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
        
        author: dict = content.get('author',{})
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

