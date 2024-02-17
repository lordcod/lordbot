import nextcord

import inspect
import regex
import string
import random
import aiohttp
import orjson

from asyncio import TimerHandle
from typing import Coroutine, Self, Union
from datetime import datetime
from captcha.image import ImageCaptcha
from io import BytesIO
from functools import lru_cache
from easy_pil import Editor, Font, load_image_async


number_type = Union[int, float]


class TempletePayload:
    _prefix = None

    def to_dict(self):
        if self._prefix is not None:
            prefix = str(self._prefix)
        else:
            prefix = self.__class__.__name__

        base = {}

        for name, arg in inspect.getmembers(self):
            if name.startswith("_") or name == "to_dict":
                continue

            base[f"{prefix}.{name}"] = arg

        return base


class GuildPayload(TempletePayload):
    _prefix = 'guild'

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
    _prefix = 'member'

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
        \{(\s*)(?:
        (?P<escaped>\{) |
        (?P<named>[\._a-z][\._a-z0-9]*)(\s*)\} |
        (?P<braced>[\._a-z][\._a-z0-9]*)(\s*)\} |
        (?P<invalid>)
        )
    '''


class DataRoleTimerHandlers:
    __instance = None
    data = None

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.data = {}
        return cls.__instance

    def __init__(self) -> None:
        pass

    def register(self,
                 guild_id: int,
                 member_id: int):
        if guild_id not in self.data:
            self.data[guild_id] = {}
        if member_id not in self.data[guild_id]:
            self.data[guild_id][member_id] = {}

    def add_th(self,
               guild_id: int,
               member_id: int,
               role_id: int,
               rth: TimerHandle):
        self.register(guild_id, member_id)
        self.data[guild_id][member_id][role_id] = rth

    def cancel_th(self,
                  guild_id: int,
                  member_id: int,
                  role_id: int):
        self.register(guild_id, member_id)
        th = self.data[guild_id][member_id].get(role_id)
        if th is None:
            return
        cancel_atimerhandler(th)


def cancel_atimerhandler(th: TimerHandle):
    coro: Coroutine = th._args[0]
    coro.close()
    th.cancel()


def clamp(val: number_type,
          minv: number_type,
          maxv: number_type) -> number_type:
    return min(maxv, max(minv, val))


async def getRandomQuote(lang='en'):
    url = f"https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang={lang}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as responce:
            json = await responce.json()
            return json


def calculate_time(string: str) -> (int | None):
    coefficients = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400
    }
    timedate = regex.findall(r'(\d+)([a-zA-Z]+)', string)
    ftime = 0
    for number, word in timedate:
        if word not in coefficients:
            raise TypeError('Format time is not valid!')

        number = int(number)
        multiplier = coefficients[word]

        ftime += number*multiplier

    return ftime


@lru_cache()
def get_award(number):
    awards = {
        1: '🥇',
        2: '🥈',
        3: '🥉'
    }
    award = awards.get(number, number)
    return award


async def generate_message(content: str) -> dict:
    content = str(content)
    message = {}
    try:
        content: dict = orjson.loads(content)

        message_content = content.get('plainText')

        title = content.get('title')
        description = content.get('description')
        color = content.get('color')
        url = content.get('url')
        fields = content.get('fields', [])

        message['content'] = message_content

        embed = nextcord.Embed(
            title=title,
            description=description,
            color=color,
            url=url,
        )

        if thumbnail := content.get('thumbnail'):
            embed.set_thumbnail(thumbnail)

        if author := content.get('author'):
            embed.set_author(
                name=author.get('name'),
                url=author.get('url'),
                icon_url=author.get('icon_url'),
            )

        if footer := content.get('footer'):
            embed.set_footer(
                text=footer.get('text'),
                icon_url=footer.get('icon_url'),
            )

        if image := content.get('image'):
            embed.set_image(image)

        for field in fields:
            embed.add_field(
                name=field.get('name', None),
                value=field.get('value', None),
                inline=field.get('inline', None)
            )

        if (title or description or image or thumbnail
                or author or footer or fields):
            message['embed'] = embed
        elif not message_content:
            raise ValueError()
    except (TypeError, ValueError, orjson.JSONDecodeError):
        message['content'] = content
    return message


async def generator_captcha(num):
    text = "".join([random.choice(string.ascii_uppercase) for _ in range(num)])
    captcha_image = ImageCaptcha(
        width=400,
        height=220,
        font_sizes=(40, 70, 100)
    )
    data: BytesIO = captcha_image.generate(text)
    return data, text


def cut_back(string: str, length: int):
    ellipsis = "..."
    current_lenght = len(string)
    if length >= current_lenght:
        return string

    cropped_string = string[:length-len(ellipsis)].strip()
    new_string = f"{cropped_string}{ellipsis}"
    return new_string


async def generate_welcome_message(member: nextcord.Member) -> bytes:
    background = Editor("assets/background.jpeg").resize((800, 450))

    nunito = Font("assets/Nunito-ExtraBold.ttf", 50)
    nunito_small = Font("assets/Nunito-Black.ttf", 25)
    nunito_light = Font("assets/Nunito-Black.ttf", 20)

    profile_image = await load_image_async(
        member.display_avatar.with_size(128).url)
    profile = Editor(profile_image).resize((150, 150)).circle_image()

    background.paste(profile, (325, 90))
    background.ellipse((325, 90), 150, 150, outline=(
        125, 249, 255), stroke_width=4)
    background.text(
        (400, 260),
        f"WELCOME TO {cut_back(member.guild.name.upper(), 14)}",
        color="white",
        font=nunito,
        align="center"
    )
    background.text(
        (400, 320),
        member.display_name,
        color="white",
        font=nunito_small,
        align="center"
    )
    background.text(
        (400, 360),
        f"You are the {member.guild.member_count}th Member",
        color="#F5923B",
        font=nunito_light,
        align="center",
    )

    return background.image_bytes
