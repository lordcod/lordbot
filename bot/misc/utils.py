import asyncio
from collections import namedtuple
import emoji

import nextcord

import inspect
import regex
import string
import random
import aiohttp
import orjson

from asyncio import TimerHandle
from typing import Coroutine, Dict, List,  Optional,  Tuple, Union, Mapping
from datetime import datetime
from captcha.image import ImageCaptcha
from io import BytesIO
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
from easy_pil import Editor, Font, load_image_async

from bot.databases.handlers.guildHD import GuildDateBases


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


_blackjack_games = {}


class BlackjackGame:
    cards = {'2 S': 2, '2 C': 2, '2 D': 2, '2 G': 2, '3 S': 3, '3 C': 3, '3 D': 3, '3 G': 3, '4 S': 4, '4 C': 4, '4 D': 4, '4 G': 4, '5 S': 5, '5 C': 5, '5 D': 5, '5 G': 5, '6 S': 6, '6 C': 6, '6 D': 6, '6 G': 6, '7 S': 7, '7 C': 7, '7 D': 7, '7 G': 7, '8 S': 8, '8 C': 8, '8 D': 8,
             '8 G': 8, '9 S': 9, '9 C': 9, '9 D': 9, '9 G': 9, '10 S': 10, '10 C': 10, '10 D': 10, '10 G': 10, 'J S': 10, 'J C': 10, 'J D': 10, 'J G': 10, 'Q S': 10, 'Q C': 10, 'Q D': 10, 'Q G': 10, 'K S': 10, 'K C': 10, 'K D': 10, 'K G': 10, 'A S': None, 'A C': None, 'A D': None, 'A G': None}

    def __init__(self, member: nextcord.Member, amount: int) -> None:
        if _blackjack_games.get(f'{member.guild.id}:{member.id}'):
            raise TypeError

        _blackjack_games[f'{member.guild.id}:{member.id}'] = self
        self.member = member
        self.amount = amount

        self.cards = self.cards.copy()
        self.your_cards = [self.get_random_cart() for _ in range(2)]
        self.dealer_cards = [self.get_random_cart() for _ in range(2)]

    @property
    def your_value(self) -> int:
        return self.calculate_result(self.your_cards)

    @property
    def dealer_value(self) -> int:
        return self.calculate_result(self.dealer_cards)

    @property
    def completed_embed(self) -> nextcord.Embed:
        gdb = GuildDateBases(self.member.guild.id)
        color = gdb.get('color')

        embed = nextcord.Embed(
            title="Blackjack",
            description=f"Result: {self.get_winner_title()}",
            color=color
        )
        embed.add_field(
            name="Your Hand",
            value=(
                f"{' '.join(self.your_cards)}\n\n"
                f"Value: {self.your_value}"
            )
        )
        embed.add_field(
            name="Dealer Hand",
            value=(
                f"{' '.join(self.dealer_cards)}\n\n"
                f"Value: {self.dealer_value}"
            )
        )
        return embed

    @property
    def embed(self) -> nextcord.Embed:
        gdb = GuildDateBases(self.member.guild.id)
        color = gdb.get('color')
        economic_settings: dict = gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')

        embed = nextcord.Embed(
            title="Blackjack",
            description=f"Bet: {self.amount}{currency_emoji}",
            color=color
        )
        embed.add_field(
            name="Your Hand",
            value=(
                f"{' '.join(self.your_cards)}\n\n"
                f"Value: {self.your_value}"
            )
        )
        embed.add_field(
            name="Dealer Hand",
            value=(
                f"{self.dealer_cards[0]} <:test_carts:1235931588273897492>\n\n"
                f"Value: {self.calculate_result(self.dealer_cards[0:1])}"
            )
        )
        return embed

    def is_avid_winner(self) -> Optional[int]:
        if (self.your_value == 21
                and self.dealer_value == 21
                and 2 == len(self.your_cards)
                and 2 == len(self.dealer_cards)):
            return 2
        elif self.your_value == 21 and 2 == len(self.your_cards):
            return 1
        elif self.dealer_value == 21 and 2 == len(self.dealer_cards):
            return 0
        return None

    def is_winner(self) -> int:
        if self.is_exceeds_dealer():
            return 1
        if self.is_exceeds_your():
            return 0

        if self.your_value == self.dealer_value:
            return 2
        if self.your_value > self.dealer_value:
            return 1
        if self.dealer_value > self.your_value:
            return 0

    def get_winner_title(self) -> int:
        gdb = GuildDateBases(self.member.guild.id)
        economic_settings: dict = gdb.get('economic_settings')
        currency_emoji = economic_settings.get('emoji')

        match self.is_winner():
            case 2:
                return f"Draw {self.amount}{currency_emoji}"
            case 1:
                return f"Won {int(1.5*self.amount)}{currency_emoji}" if self.is_avid_winner() == 1 else f"Won {self.amount}{currency_emoji}"
            case 0:
                return f"Loss -{self.amount}{currency_emoji}"

    def is_exceeds_your(self) -> int:
        return self.your_value > 21

    def is_exceeds_dealer(self) -> int:
        return self.dealer_value > 21

    def go_dealer(self) -> int:
        while 18 > self.dealer_value:
            self.add_dealer_card()

    def add_dealer_card(self) -> None:
        self.dealer_cards.append(self.get_random_cart())

    def add_your_card(self) -> None:
        self.your_cards.append(self.get_random_cart())

    def complete(self) -> None:
        _blackjack_games.pop(f'{self.member.guild.id}:{self.member.id}', None)

    @staticmethod
    def calculate_result(_cards: List[Optional[int]]) -> int:
        result = 0
        count_of_none = 0
        for val in map(BlackjackGame.cards.__getitem__, _cards):
            if val is None:
                count_of_none += 1
            else:
                result += val
        for _ in range(count_of_none):
            if result+11 > 21:
                result += 1
            else:
                result += 11
        return result

    def get_random_cart(self) -> str:
        val = random.choice(list(self.cards))
        self.cards.pop(val)
        return val


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
        coro: Coroutine = th._args[0]
        coro.close()
        th.cancel()

    def close_as_th(th: TimerHandle):
        coro: Coroutine = th._args[0]
        coro.close()
        th.cancel()


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


def calculate_time(string: str) -> int:
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
