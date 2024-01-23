import nextcord
from nextcord.ext import commands

from bot.misc import (
    utils,
    env
)

import os
from typing import List


async def get_command_prefixs(
    bot: commands.Bot, 
    msg: nextcord.Message
) -> List[str]:
    "Returns a list of prefixes that can be used when using bot commands"
    prefix = utils.get_prefix(msg.guild.id)
    return [prefix, f"<@{bot.user.id}> ", f"<@!{bot.user.id}> "]

bot = commands.Bot(
    command_prefix=get_command_prefixs,
    intents=nextcord.Intents.all(),
    help_command=None
)


def load_dir(dirpath: str) -> None:
    for filename in os.listdir(dirpath):
        if os.path.isfile(f'{dirpath}/{filename}') and filename.endswith(".py"):
            fmp = filename[:-3]
            supath = dirpath[2:].replace("/", ".")
            
            bot.load_extension(f"{supath}.{fmp}")
        elif os.path.isdir(f'{dirpath}/{filename}'):
            load_dir(f'{dirpath}/{filename}')

def start_bot():
    load_dir("./bot/cogs")
    
    bot.run(env.Tokens.token)