import time
import aiohttp
import asyncio


class TextColors:
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


class DiscordTextColors:
    RESET = '[0m'

    GREY = '[2;30m'
    RED = '[2;31m'
    GREEN = '[2;32m'
    YELLOW = '[2;33m'
    BLUE = '[2;34m'
    VIOLET = '[2;35m'
    CYAN = '[2;36m'


async def post_mes(data, time_string):
    url = "https://discord.com/api/webhooks/1202680614772285450/GL1vm6jvvoaNLxb3hXeECOfGH2NuMdjB34h7SBazhDDYK18OMy-x_WV0sIEbRZ0r1BBj"
    data = {
        "content": (
            "```ansi\n"
            f"{data.get('discord_color')}"
            f"[{time_string}][{data.get('service')}]: {data.get('text')}"
            f"{DiscordTextColors.RESET}"
            "```"
        )
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data):
            pass


@lambda cls: cls(True)
class Logger:
    loop = None

    def __init__(self, prints) -> None:
        self.prints = prints
        self.loop = asyncio.get_event_loop()

    def callback(self, text):
        if self.prints:
            print(text)

    def on_logs(func):
        def redirect(self, txt):
            named_tuple = time.localtime()
            time_string = time.strftime("%m-%d-%Y %H:%M:%S", named_tuple)

            data: dict = func(self, txt)
            self.loop.create_task(post_mes(data, time_string))

            text = (
                f"{data.get('color')}"
                f"[{time_string}][{data.get('service')}]: {data.get('text')}"
                f"{TextColors.RESET}"
            )

            self.callback(text)

            return text
        return redirect

    @on_logs
    def info(self, text):
        color = TextColors.GREY
        discord_color = DiscordTextColors.GREY
        service = 'INFO'
        return {
            'text': text,
            'color': color,
            'discord_color': discord_color,
            'service': service
        }

    @on_logs
    def warn(self, text):
        color = TextColors.YELLOW
        discord_color = DiscordTextColors.YELLOW
        service = 'WARN'
        return {
            'text': text,
            'color': color,
            'discord_color': discord_color,
            'service': service
        }

    @on_logs
    def error(self, text):
        color = TextColors.RED
        discord_color = DiscordTextColors.RED
        service = 'ERROR'
        return {
            'text': text,
            'color': color,
            'discord_color': discord_color,
            'service': service
        }

    @on_logs
    def critical(self, text):
        color = TextColors.VIOLET
        discord_color = DiscordTextColors.VIOLET
        service = 'CRITICAL'
        return {
            'text': text,
            'color': color,
            'discord_color': discord_color,
            'service': service
        }

    @on_logs
    def success(self, text):
        color = TextColors.GREEN
        discord_color = DiscordTextColors.GREEN
        service = 'SUCCESS'
        return {
            'text': text,
            'color': color,
            'discord_color': discord_color,
            'service': service
        }

    @on_logs
    def inportent(self, text):
        color = TextColors.BLUE
        discord_color = DiscordTextColors.BLUE
        service = 'IMPORTENT'
        return {
            'text': text,
            'color': color,
            'discord_color': discord_color,
            'service': service
        }

    @on_logs
    def core(self, text):
        color = TextColors.CYAN
        discord_color = DiscordTextColors.CYAN
        service = 'CORE'
        return {
            'text': text,
            'color': color,
            'discord_color': discord_color,
            'service': service
        }
