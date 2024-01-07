from typing import Any
import nextcord
from nextcord.ext import commands
from nextcord.utils import escape_markdown

from bot.resources import errors
from bot.databases.db import GuildDateBases, RoleDateBases

import inspect
import re
import string
import random
import time
import asyncio
import aiohttp
import orjson

from datetime import datetime
from captcha.image import ImageCaptcha
from io import BytesIO


intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)



class TempletePayload:
    def to_dict(self, _prefix = None):
        if _prefix is None:
            prefix = self.__class__.__name__
        else:
            prefix = str(_prefix)
        
        base = {}
        
        for name, arg in inspect.getmembers(self):
            if name.startswith("_") or name == "to_dict":
                continue
            
            base[f"{prefix}.{name}"] = arg
        
        return base

class GuildPayload(TempletePayload):
    def __init__(self, guild: nextcord.Guild) -> None:
        self.id: int = guild.id
        self.name: str = guild.name
        self.memberCount: int = guild.member_count
        self.createdAt: datetime = guild.created_at
        self.premiumSubscriptionCount: int = guild.premium_subscription_count
        
        if not (guild.icon and guild.icon.url):
            self.icon = None
        else:
            self.icon: str = guild.icon.url

    def __str__(self) -> str:
        return self.name

class MemberPayload(TempletePayload): 
    def __init__(self, member: nextcord.Member) -> None:
        self.id: int = member.id
        self.mention: str = member.mention
        self.username: str = member.name
        self.displayName: str = member.display_name
        self.discriminator: str = member.discriminator
        self.tag = f'{member.name}#{member.discriminator}'
        
        if not (member.display_avatar and member.display_avatar.url):
            self.avatar = None
        else:
            self.avatar = member.display_avatar.url
    
    
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


async def process_role(
    member: nextcord.Member,
    role: nextcord.Role,
    unix_time: int
) -> None:
    rsdb = RoleDateBases(
        guild_id=member.guild.id,
        member_id=member.id
    )
    data = {
        'time':unix_time,
        'role_id': role.id
    }
    temp = unix_time - int(time.time())
    
    await asyncio.sleep(temp)
    
    await member.remove_roles(role)
    rsdb.remove(data)

async def getRandomQuote(lang='en'):
    url = f"https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang={lang}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as responce:
            json = await responce.json()
            return json

def calculate_time(string: str) -> (int|None):
    coefficients = {
        's':1,
        'm':60,
        'h':3600,
        'd':86400
    }
    timedate = re.findall(r'(\d+)([a-zA-Z]+)', string)
    ftime = 0
    for number, word in timedate:
        if word not in coefficients:
            return None
        
        number = int(number)
        multiplier = coefficients[word]
        
        ftime += number*multiplier
    
    return ftime

def get_award(number):
    awards = {
        1:'🥇',
        2:'🥈',
        3:'🥉'
    }
    award = awards.get(number,number)
    return award

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
    content = str(content)
    message = {}
    try:
        content: dict = orjson.loads(content)
        
        message_content = content.get('plainText')
        
        title = content.get('title')
        description=content.get('description')
        color=content.get('color')
        url=content.get('url')
        
        thumbnail = content.get('thumbnail')
        author = content.get('author')
        footer = content.get('footer')
        fields = content.get('fields', [])
        
        message['content'] = message_content
        
        embed = nextcord.Embed(
            title=title,
            description=description,
            color=color,
            url=url,
        )
        
        if thumbnail:
            embed.set_thumbnail(thumbnail)
        
        if author:
            embed.set_author(
                name=author.get('name',None),
                url=author.get('url',None),
                icon_url=author.get('icon_url',None),
            )
        
        if footer:
            embed.set_footer(
                text=footer.get('text'),
                icon_url=footer.get('icon_url'),
            )
        
        for field in fields:
            embed.add_field(
                name=field.get('name',None),
                value=field.get('value',None),
                inline=field.get('inline',None)
            )
        
        if title or description or thumbnail or author or footer or fields:
            message['embed'] = embed
        elif not message_content:
            raise ValueError()
    except:
        message['content'] = content
    return message

async def check_invite(content):
    regex_string = '(https:\/\/discord.gg\/|https:\/\/discord.com\/invite\/)([a-zA-Z0-9_-]+)(\/|\s|\?|$)'
    if pattern := re.fullmatch(regex_string,content):
        return pattern.group(2)

async def generator_captcha(num):
    text = "".join([random.choice(string.ascii_uppercase) for _ in range(num)])
    captcha_image = ImageCaptcha(
        width=400,
        height=220,
        font_sizes=(40,70,100)
    )
    data:BytesIO = captcha_image.generate(text)
    return data,text

def cut_back(string: str, length: int):
    ellipsis = "..."
    current_lenght = len(string)
    if length >= current_lenght:
        return string
    
    cropped_string = string[:length-len(ellipsis)].strip()
    new_string = f"{cropped_string}{ellipsis}"
    return new_string

def is_float(element: any) -> bool:
    if element is None: 
        return False
    
    try:
        float(element)
        return True
    except ValueError:
        return False

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])
