from os import environ
import re
import nextcord
from nextcord.ext import commands
from bot.misc.lordbot import LordBot

from bot.misc.utils import clamp
from dotenv import load_dotenv

load_dotenv()


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

FFMPEG_OPTIONS = {'options': '-vn'}
YOUTUBE_LINK_SEARCH = re.compile(
    r'https://www.youtube.com/watch?v=([a-zA-Z0-9_]+)')
YANDEX_MUSIC_SEARCH = re.compile(
    r'https://music.yandex.ru/album/(\d+)/track/(\d+)(.*)')


def setup(bot):
    return
