from dataclasses import dataclass
from string import printable
import time
import aiohttp
import asyncio
import enum

pintable = False
loop = asyncio.get_event_loop()
session = aiohttp.ClientSession()


class TextColors(enum.Enum):
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    OBLIQUE = '\033[3m'

    GREY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    VIOLET = '\033[95m'
    CYAN = '\033[96m'

    def __str__(self) -> str:
        return self.value


class DiscordTextColors(enum.Enum):
    RESET = '[0m'

    GREY = '[2;30m'
    RED = '[2;31m'
    GREEN = '[2;32m'
    YELLOW = '[2;33m'
    BLUE = '[2;34m'
    VIOLET = '[2;35m'
    CYAN = '[2;36m'

    def __str__(self) -> str:
        return self.value


@dataclass
class LogInfo:
    color: TextColors
    discord_color: DiscordTextColors
    service: str


async def post_mes(text: str, data: LogInfo, time_string: str) -> None:
    url = "https://discord.com/api/webhooks/1202680614772285450/GL1vm6jvvoaNLxb3hXeECOfGH2NuMdjB34h7SBazhDDYK18OMy-x_WV0sIEbRZ0r1BBj"
    data = {
        "content": (
            "```ansi\n"
            f"{data.discord_color}"
            f"[{time_string}][{data.service}]: {text}"
            f"{DiscordTextColors.RESET}"
            "```"
        )
    }

    async with session.post(url, data=data):
        pass


class Logger:
    @staticmethod
    def callback(text: str, data: LogInfo):
        named_tuple = time.localtime()
        time_string = time.strftime("%m-%d-%Y %H:%M:%S", named_tuple)

        loop.create_task(post_mes(text, data, time_string))

        if not printable:
            return

        text_new = (
            f"{data.color}"
            f"[{time_string}][{data.service}]: {text}"
            f"{TextColors.RESET}"
        )
        print(text_new)

    def on_logs(func):
        @staticmethod
        def redirect(text: str):
            data = func(text)
            Logger.callback(text, data)
            return text
        return redirect

    @on_logs
    @staticmethod
    def info(text):
        color = TextColors.GREY
        discord_color = DiscordTextColors.GREY
        service = 'INFO'
        return LogInfo(color, discord_color, service)

    @on_logs
    @staticmethod
    def warn(text):
        color = TextColors.YELLOW
        discord_color = DiscordTextColors.YELLOW
        service = 'WARN'
        return LogInfo(color, discord_color, service)

    @on_logs
    @staticmethod
    def error(text):
        color = TextColors.RED
        discord_color = DiscordTextColors.RED
        service = 'ERROR'
        return LogInfo(color, discord_color, service)

    @on_logs
    @staticmethod
    def critical(text):
        color = TextColors.VIOLET
        discord_color = DiscordTextColors.VIOLET
        service = 'CRITICAL'
        return LogInfo(color, discord_color, service)

    @on_logs
    @staticmethod
    def success(text):
        color = TextColors.GREEN
        discord_color = DiscordTextColors.GREEN
        service = 'SUCCESS'
        return LogInfo(color, discord_color, service)

    @on_logs
    @staticmethod
    def inportent(text):
        color = TextColors.BLUE
        discord_color = DiscordTextColors.BLUE
        service = 'IMPORTENT'
        return LogInfo(color, discord_color, service)

    @on_logs
    @staticmethod
    def core(text):
        color = TextColors.CYAN
        discord_color = DiscordTextColors.CYAN
        service = 'CORE'
        return LogInfo(color, discord_color, service)
