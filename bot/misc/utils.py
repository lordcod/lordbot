from __future__ import annotations
import nextcord
from nextcord.ext import commands


import inspect
import regex
import string
import random
import aiohttp
import asyncio
import time
import emoji
import orjson

from asyncio import TimerHandle
from collections import namedtuple
from typing import (Coroutine, Dict,  Optional,  Tuple, Union,
                    Mapping, Any, Iterable, SupportsIndex, Self, List)
from typing import Any, Coroutine, Dict, Iterable,  Optional, Self, SupportsIndex,  Tuple, Union, Mapping
from datetime import datetime
from captcha.image import ImageCaptcha
from io import BytesIO
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
from easy_pil import Editor, Font, load_image_async

from bot.databases.handlers.guildHD import GuildDateBases
from cryptography.fernet import Fernet


T = TypeVar('T')
wel_mes = namedtuple("WelcomeMessageItem", ["name", "link", "description"])

welcome_message_items = {
    "None": wel_mes("None", None, None),
    "my-image": wel_mes("My image", ..., "You will be able to enter a link to an image."),
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


class Tokenizer:
    @staticmethod
    def encrypt(message: bytes, key: bytes) -> bytes:
        return Fernet(key).encrypt(message)

    @staticmethod
    def decrypt(token: bytes, key: bytes) -> bytes:
        return Fernet(key).decrypt(token)

    @staticmethod
    def generate_key() -> bytes:
        return Fernet.generate_key()


_blackjack_games = {}


class BlackjackGame:
    cards = {
        '<:hearts_of_ace:1236254919347142688>': None, '<:hearts_of_two:1236254940016545843>': 2, '<:hearts_of_three:1236254938158338088>': 3, '<:hearts_of_four:1236254924757536799>': 4, '<:hearts_of_five:1236254923050586212>': 5, '<:hearts_of_six:1236254934920593438>': 6, '<:hearts_of_seven:1236254933309718641>': 7, '<:hearts_of_eight:1236254921272066078>': 8, '<:hearts_of_nine:1236254929803280394>': 9, '<:hearts_of_ten:1236254936514428948>': 10, '<:hearts_of_jack:1236254926263418932>': 10, '<:hearts_of_queen:1236254931464228905>': 10, '<:hearts_of_king:1236254928104587336>': 10,
        '<:spades_of_ace:1236254941820092506>': None, '<:spades_of_two:1236256183048863836>': 2, '<:spades_of_three:1236256162933112862>': 3, '<:spades_of_four:1236254946454667325>': 4, '<:spades_of_five:1236256181433929768>': 5, '<:spades_of_six:1236256158835277846>': 6, '<:spades_of_seven:1236256156834594836>': 7, '<:spades_of_eight:1236254943632162857>': 8, '<:spades_of_nine:1236254952901316659>': 9, '<:spades_of_ten:1236256161024708619>': 10, '<:spades_of_jack:1236254949072048200>': 10, '<:spades_of_queen:1236254955099262996>': 10, '<:spades_of_king:1236254951001292840>': 10,
        '<:clubs_of_ace:1236254878867918881>': None, '<:clubs_of_two:1236254897243029607>': 2, '<:clubs_of_three:1236254896026812508>': 3, '<:clubs_of_four:1236254884232167474>': 4, '<:clubs_of_five:1236254882533740614>': 5, '<:clubs_of_six:1236254893015175220>': 6, '<:clubs_of_seven:1236254891572334644>': 7, '<:clubs_of_eight:1236254880981586021>': 8, '<:clubs_of_nine:1236254888833581116>': 9, '<:clubs_of_ten:1236254894525120522>': 10, '<:clubs_of_jack:1236254886119739423>': 10, '<:clubs_of_queen:1236254890234347540>': 10, '<:clubs_of_king:1236254887474368533>': 10,
        '<:diamonds_of_ace:1236254898799247441>': None, '<:diamonds_of_two:1236254917266636912>': 2, '<:diamonds_of_three:1236254916394225696>': 3, '<:diamonds_of_four:1236254903140220988>': 4, '<:diamonds_of_five:1236254901835661333>': 5, '<:diamonds_of_six:1236254913412202496>': 6, '<:diamonds_of_seven:1236254911797268500>': 7, '<:diamonds_of_eight:1236254900338430042>': 8, '<:diamonds_of_nine:1236254908164870164>': 9, '<:diamonds_of_ten:1236254914867626064>': 10, '<:diamonds_of_jack:1236254904931061800>': 10, '<:diamonds_of_queen:1236254909813358602>': 10, '<:diamonds_of_king:1236254906562777191>': 10
    }

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


def translate_flags(text: str) -> dict:
    return dict(map(
        lambda item: (item[0], item[1]) if item[1] else (item[0], True),
        regex.findall(
            r"\-\-([a-zA-Z0-9\_\-]+)=?([a-zA-Z0-9\_\-]+)?(\s|$)",
            text
        )
    ))


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
            print(f"Create new timer handle {coro.__name__}(ID:{key})")
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


class FissionIterator:
    def __init__(self, iterable: Iterable[Any], count: int) -> None:
        self.iterable = list(iterable)
        self.count = count
        self.value = 0
        self.max_value = False

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> Any:
        if self.max_value:
            raise StopIteration
        items = []
        stop = self.value+self.count
        if stop >= len(self.iterable):
            stop = len(self.iterable)
            self.max_value = True
        for item in self.iterable[self.value:stop]:
            items.append(item)
        self.value = stop
        return items

    def __getitem__(self, __value: Union[SupportsIndex, slice]) -> Any:
        return list(iter(self))[__value]

    def to_list(self):
        return list(iter(self))


def clamp(val: Union[int, float],
          minv: Union[int, float],
          maxv: Union[int, float]) -> Union[int, float]:
    return min(maxv, max(minv, val))


def is_emoji(text: str) -> bool:
    text = text.strip()
    return any((regex.fullmatch(r'<a?:.+?:\d{18,}>', text), text in emoji.EMOJI_DATA))


def randquan(quan: int) -> int:
    if 0 >= quan:
        raise ValueError
    return random.randint(10**(quan-1), int('9'*quan))


def generate_random_token() -> Tuple[str, str]:
    message = randquan(100).to_bytes(100)
    key = Fernet.generate_key()
    token = Tokenizer.encrypt(message, key)
    return key.decode(), token.decode()


def decrypt_token(key: str, token: str) -> int:
    res = Tokenizer.decrypt(token.encode(), key.encode())
    return int.from_bytes(res)


async def get_random_quote(lang: str = 'en'):
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

    @overload
    def convert(
        self,
        argument: str
    ) -> T:
        pass

    @overload
    def convert(
        self,
        ctx: commands.Context,
        argument: str
    ) -> Coroutine[Any, Any, T]:
        pass

    def convert(self, *args) -> T | Coroutine[Any, Any, T]:
        try:
            return self.async_convert(*args)
        except KeyboardInterrupt:
            raise
        except Exception:
            pass

        try:
            return self.basic_convert(*args)
        except KeyboardInterrupt:
            raise
        except Exception:
            pass

        raise TypeError

    def basic_convert(
        self,
        argument: Any
    ) -> T:
        if not (isinstance(argument, str)
                and regex.fullmatch(r'\s*(\d+[a-zA-Z\s]+){1,}', argument)):
            raise TypeError('Format time is not valid!')

        timedate: list[tuple[str, str]] = regex.findall(
            r'(\d+)([a-zA-Z\s]+)', argument)
        ftime = 0

        for number, word in timedate:
            if word.strip() not in self.coefficients:
                raise TypeError('Format time is not valid!')

            multiplier = self.coefficients[word.strip()]
            ftime += int(number)*multiplier

        if not ftime:
            raise TypeError('Format time is not valid!')
        if self.operatable_time:
            ftime += time.time()

        return self.refundable(ftime)

    async def async_convert(
        self,
        ctx: commands.Context,
        argument: Any
    ) -> T:
        return self.basic_convert(argument)


def translate_to_timestamp(arg: str) -> int | None:
    try:
        tdt = datetime.strptime(arg, '%H:%M')
        return datetime(
            year=datetime.today().year,
            month=datetime.today().month,
            day=datetime.today().day,
            hour=tdt.hour,
            minute=tdt.minute
        ).timestamp()
    except ValueError:
        pass
    try:
        tdt = datetime.strptime(arg, '%H:%M:%S')
        return datetime(
            year=datetime.today().year,
            month=datetime.today().month,
            day=datetime.today().day,
            hour=tdt.hour,
            minute=tdt.minute,
            second=tdt.second
        ).timestamp()
    except ValueError:
        pass

    try:
        return datetime.strptime(arg, '%d.%m.%Y').timestamp()
    except ValueError:
        pass
    try:
        return datetime.strptime(arg, '%d.%m.%Y %H:%M').timestamp()
    except ValueError:
        pass
    try:
        return datetime.strptime(arg, '%d.%m.%Y %H:%M:%S').timestamp()
    except ValueError:
        pass
    try:
        return datetime.strptime(arg, '%H:%M %d.%m.%Y').timestamp()
    except ValueError:
        pass
    try:
        return datetime.strptime(arg, '%H:%M:%S %d.%m.%Y').timestamp()
    except ValueError:
        pass

    try:
        return datetime.strptime(arg, '%Y-%m-%d').timestamp()
    except ValueError:
        pass
    try:
        return datetime.strptime(arg, '%H:%M %Y-%m-%d').timestamp()
    except ValueError:
        pass
    try:
        return datetime.strptime(arg, '%H:%M:%S %Y-%m-%d').timestamp()
    except ValueError:
        pass
    try:
        return datetime.strptime(arg, '%Y-%m-%d %H:%M').timestamp()
    except ValueError:
        pass
    try:
        return datetime.strptime(arg, '%Y-%m-%d %H:%M:%S').timestamp()
    except ValueError:
        pass

    try:
        return TimeCalculator(operatable_time=True).convert(arg)
    except ValueError:
        pass

    return None


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
    background_image = await load_image_async(background_link, session=member._state.http.__session)
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
