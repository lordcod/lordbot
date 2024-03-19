from __future__ import annotations
import asyncio
from collections import namedtuple
import time
from typing import Any, TypeVar
import emoji

import nextcord
from nextcord.ext import commands


import inspect
import regex
import string
import random
import aiohttp
import orjson
import threading

from asyncio import TimerHandle
from typing import Coroutine, Dict,  Optional,  Tuple, Union, Mapping
from datetime import datetime
from captcha.image import ImageCaptcha
from io import BytesIO
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
from easy_pil import Editor, Font, load_image_async


T = TypeVar('T')
wel_mes = namedtuple("WelcomeMessageItem", ["name", "link", "description"])

welcome_message_items = {
    "None": wel_mes("None", None, None),
    "my-image": wel_mes("My image", "Nope", "You will be able to enter a link to an image."),
    "view-from-mountain": wel_mes("View from mountain", "https://i.postimg.cc/Hnpz0ycb/view-from-mountain.jpg", "Summer vibes, mountain views, sunset - all adds charm."),
    "autumn-street": wel_mes("Autumn street", "https://i.postimg.cc/sXnQ8QHY/autumn-street.jpg", "The joy of a bright autumn morning, surrounded by a stunning building and the atmosphere of autumn."),
    "winter-day": wel_mes("Winter day", "https://i.postimg.cc/qBhyYQ0g/winter-day.jpg", "Dazzling winter day, majestic mountain, small buildings, sparkling highway, snow-white covers."),
    "magic-city": wel_mes("Magic city", "https://i.postimg.cc/hjJzk4kN/magic-city.jpg", "The beautiful atmosphere and scenic views from the boat."),
    "city-dawn": wel_mes("City dawn", "https://i.postimg.cc/13J84NPL/city-dawn.jpg", "Starry sky, breeze, rustling leaves, crickets, fireflies, bonfire - perfect night.")
}


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


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class __LordFormatingTemplate(string.Template):
    pattern = r"""
        \{(\s*)(?:
        (?P<escaped>\{) |
        (?P<named>[\._a-z][\._a-z0-9]*)(\s*)\} |
        (?P<braced>[\._a-z][\._a-z0-9]*)(\s*)\} |
        (?P<invalid>)
        )
    """

    def format(self, __mapping: Mapping[str, object]):
        return self.safe_substitute(__mapping)


def lord_format(
    __value: object,
    __mapping: Mapping[str, object]
) -> str:
    return __LordFormatingTemplate(__value).format(__mapping)


async def clone_message(message: nextcord.Message) -> dict:
    content = message.content
    embeds = message.embeds
    files = []
    for attach in message.attachments:
        filebytes = await attach.read()
        files.append(nextcord.File(
            fp=filebytes,
            filename=attach.filename,
            description=attach.description,
            spoiler=attach.is_spoiler()
        ))

    return {
        "content": content,
        "embeds": embeds,
        "files": files
    }


class LordTimerHandler:
    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        self.data: Dict[Union[str, int], TimerHandle] = {}

    def create_timer_handler(
        self,
        delay: float,
        coro: Coroutine,
        key: Optional[Union[str, int]] = None
    ):
        th = self.loop.call_later(delay,  self.loop.create_task, coro)
        if key is not None:
            self.data[key] = th

    def close_as_key(self, key: Union[str, int]):
        th = self.data.get(key)
        if th is None:
            return
        arg = th._args[0]
        if asyncio.iscoroutine(arg):
            arg.close()
        th.cancel()

    def close_as_th(self, th: TimerHandle):
        arg = th._args and th._args[0]
        if asyncio.iscoroutine(arg):
            arg.close()
        th.cancel()

    def call_as_key(self, key: Union[str, int]):
        th = self.data.get(key)
        if th is None:
            return
        th._run()
        self.close_as_th(th)


def clamp(val: Union[int, float],
          minv: Union[int, float],
          maxv: Union[int, float]) -> Union[int, float]:
    return min(maxv, max(minv, val))


def is_emoji(text: str) -> bool:
    text = text.strip()
    if regex.fullmatch(r'<a?:.+?:\d{18}>', text):
        return True
    if text in emoji.EMOJI_DATA:
        return True
    return False


async def getRandomQuote(lang: str = 'en'):
    url = f"https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang={lang}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as responce:
            json = await responce.json()
            return json


class TimeCalculator:
    def __init__(
        self,
        default_coefficient: int = 60,
        refundable: T = int,
        coefficients: Optional[dict] = None,
        operatable_time: bool = False
    ) -> None:
        self.default_coefficient = default_coefficient
        self.refundable = refundable
        self.operatable_time = operatable_time

        if coefficients is None:
            self.coefficients = {
                's': 1,
                'm': 60,
                'h': 3600,
                'd': 86400
            }
        else:
            self.coefficients = coefficients

    def convert(self, *args) -> T:
        try:
            return self.basic_convert(*args)
        except Exception:
            pass

        try:
            return self.async_convert(*args)
        except Exception:
            pass

        raise TypeError

    @staticmethod
    def get_numeric(argument: str) -> Optional[Union[int, float]]:
        try:
            return int(argument)
        except ValueError:
            pass
        try:
            return float(argument)
        except ValueError:
            pass
        return None

    def basic_convert(
        self,
        argument: Any
    ) -> T:
        if not isinstance(argument, str):
            raise TypeError

        if numeric := self.get_numeric(argument):
            ftime = numeric*self.default_coefficient
            if self.operatable_time:
                ftime += time.time()
            return self.refundable(ftime)

        timedate = regex.findall(r'(\d+)([a-zA-Z]+)', argument)
        ftime = 0

        for number, word in timedate:
            if word not in self.coefficients:
                raise TypeError('Format time is not valid!')

            multiplier = self.coefficients[word]
            ftime += int(number)*multiplier

        if self.operatable_time:
            ftime += time.time()

        return self.refundable(ftime)

    async def async_convert(
        self,
        ctx: commands.Context,
        argument: Any
    ) -> T:
        return self.basic_convert(argument)


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
        message['content'] = message_content

        title = content.get('title')
        description = content.get('description')
        color = content.get('color')
        url = content.get('url')
        fields = content.get('fields', [])

        embed = nextcord.Embed(
            title=title,
            description=description,
            color=color,
            url=url
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
            raise ValueError
    except (TypeError, ValueError, orjson.JSONDecodeError):
        message['content'] = content
    return message


async def generator_captcha(num):
    text = "".join([random.choice(string.ascii_uppercase) for _ in range(num)])
    captcha_image = ImageCaptcha(
        width=400,
        height=220,
        fonts=["assets/Nunito-Black.ttf"],
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


def draw_gradient(
    img: Image.Image,
    start: Tuple[int, int, int],
    end: Tuple[int, int, int]
):
    px = img.load()
    for y in range(0, img.height):
        color = tuple(int(start[i] + (end[i] - start[i])
                      * y / img.height) for i in range(3))
        for x in range(0, img.width):
            px[x, y] = color


def add_gradient(
    backgroud: Image.Image,
    font: ImageFont.FreeTypeFont,
    text: str,
    height: int,
    color_start: Tuple[int, int, int],
    color_stop: Tuple[int, int, int]
) -> None:
    w, h = font.getbbox(text)[2:]

    gradient = Image.new("RGB", (w, h))
    draw_gradient(gradient, color_start, color_stop)

    im_text = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(im_text)
    d.text((0, 0), text, font=font)

    backgroud.draft("RGBA", backgroud.size)
    backgroud.paste(
        gradient,
        (int(backgroud.size[0]/2-im_text.size[0]/2), height),
        im_text
    )


async def generate_welcome_image(member: nextcord.Member, background_link: str) -> bytes:
    background_image = await load_image_async(background_link)
    background = Editor(background_image).resize((800, 450))

    profile_image = await load_image_async(
        member.display_avatar.with_size(128).url)
    profile = Editor(profile_image).resize((150, 150)).circle_image()\

    nunito = Font("assets/Nunito-ExtraBold.ttf", 40)
    nunito_small = Font("assets/Nunito-Black.ttf", 25)
    nunito_light = Font("assets/Nunito-Black.ttf", 20)

    background.paste(profile, (325, 90))
    background.ellipse((325, 90), 150, 150, outline=(
        125, 249, 255), stroke_width=4)
    add_gradient(
        background.image,
        nunito.font,
        f"WELCOME TO {member.guild.name.upper()}",
        260,
        (253, 187, 45),
        (34, 193, 195)
    )
    background.text(
        (400, 320),
        member.display_name,
        color=0xff0000,
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
