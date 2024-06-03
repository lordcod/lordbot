
import logging
import os
import aiohttp
import asyncio
from datetime import datetime
from pytz import timezone

log_webhook = os.environ.get('log_webhook')
loop = asyncio.get_event_loop()


TRACE = logging.DEBUG - 5
CORE = logging.INFO + 5

DEFAULT_LOG = TRACE
DEFAULT_DISCORD_LOG = logging.INFO

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

RESET_SEQD = '[0m'
COLOR_SEQD = '[2;%dm'
BOLD_SEQD = '[2;1m'

COLORS = {
    'WARNING': YELLOW,
    'INFO': GREEN,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED,
    'TRACE': CYAN,
    'CORE': MAGENTA
}


tasks = []


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


def formatter_discord_message(message, use_color=True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQD).replace("$BOLD", BOLD_SEQD)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


async def post_mes(webhook_url: str, text: str) -> None:
    from nextcord import Webhook

    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, session=session)
        await webhook.send('```ansi\n' + text + '```')


tz = timezone('Europe/Moscow')
logging.Formatter.convert = lambda *args: datetime.now(tz).timetuple()


class DiscordColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg, datefmt='%m-%d-%Y %H:%M:%S')
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQD % (30 + COLORS[levelname]) + levelname + RESET_SEQD
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg, datefmt='%m-%d-%Y %H:%M:%S')
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


class DiscordHandler(logging.Handler):
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url
        super().__init__()

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            task = loop.create_task(post_mes(self.webhook_url, msg))
            tasks.append(task)
            self.flush()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)


class LordLogger(logging.Logger):
    FORMAT = "[$BOLD%(asctime)s$RESET][$BOLD%(name)s$RESET][%(levelname)s]  %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
    COLOR_FORMAT = formatter_message(FORMAT, True)

    def __init__(self, name: str, level: int = DEFAULT_LOG):
        logging.Logger.__init__(self, name, level)

        color_formatter = ColoredFormatter(self.COLOR_FORMAT)
        self.console = logging.StreamHandler()
        self.console.setFormatter(color_formatter)
        self.addHandler(self.console)

        color_formatter = DiscordColoredFormatter(self.COLOR_FORMAT)
        self.discord_handler = DiscordHandler(log_webhook)
        self.discord_handler.setFormatter(color_formatter)
        self.discord_handler.setLevel(DEFAULT_DISCORD_LOG)
        self.addHandler(self.discord_handler)

    def trace(self, msg, *args, **kwargs):
        if self.isEnabledFor(TRACE):
            self._log(TRACE, msg, args, **kwargs)

    def core(self, msg, *args, **kwargs):
        if self.isEnabledFor(CORE):
            self._log(CORE, msg, args, **kwargs)


logging.setLoggerClass(LordLogger)

logging.addLevelName(TRACE, 'TRACE')
logging.addLevelName(CORE, 'CORE')
