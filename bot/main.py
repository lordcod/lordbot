import nextcord
from nextcord.ext import commands

from bot.misc import (utils,env)
from bot.misc.logger import Logger

from typing import List
import os



def get_command_prefixs(
bot: commands.Bot, 
msg: nextcord.Message
) -> List[str]:
    prefix = utils.get_prefix(msg.guild.id)
    return [prefix, f"<@{bot.user.id}> ", f"<@!{bot.user.id}> "]

bot = commands.Bot(
    command_prefix=get_command_prefixs,
    intents=nextcord.Intents.all(),
    help_command=None
)




def load_dir(dirpath: str) -> None:
    for filename in os.listdir(dirpath):
        if os.path.isfile(f'{dirpath}/{filename}') and filename.endswith(".py") and not filename.startswith("__"):
            fmp = filename[:-3]
            supdirpath = dirpath[2:].split("/")
            findirpatch = '.'.join(supdirpath)
            Logger.info(f'Load Extension: {dirpath}/{filename}')
            bot.load_extension(f"{findirpatch}.{fmp}")
        elif os.path.isdir(f'{dirpath}/{filename}'):
            load_dir(f'{dirpath}/{filename}')

def start_bot():
    load_dir("./bot/cogs")
    
    bot.run(env.token_lord_the_tester)