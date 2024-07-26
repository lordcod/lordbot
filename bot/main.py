import getopt
import sys

import nextcord
from bot.misc import env
from bot.misc.lordbot import LordBot

import os


bot = LordBot(rollout_functions=False)


def load_dir(dirpath: str) -> None:
    for filename in os.listdir(dirpath):
        if (os.path.isfile(f'{dirpath}/{filename}')
                and filename.endswith(".py")):
            fmp = filename[:-3]
            supath = dirpath[2:].replace("/", ".")

            bot.load_extension(f"{supath}.{fmp}")
        elif os.path.isdir(f'{dirpath}/{filename}'):
            load_dir(f'{dirpath}/{filename}')


def start_bot():
    flags = dict(map(lambda item: (item[0].removeprefix(
        '--'), item[1]), getopt.getopt(sys.argv[1:], '', ['token=', 'shards='])[0]))

    load_dir("./bot/cogs")

    try:
        if token_name := flags.get('token'):
            token = getattr(env.Tokens, 'token_'+token_name)
        else:
            token = env.Tokens.token
        bot.run(token)
    except nextcord.HTTPException:
        return
