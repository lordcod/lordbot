import nextcord
from nextcord.ext import (commands,application_checks,tasks)
from nextcord.utils import (get,find,escape_markdown)
import os

from bot.databases.db import GuildDateBases
from bot.misc import (utils,env)
from bot.resources import (info,errors)
from bot import languages
from bot.views import views
from bot.resources.errors import CallbackCommandError




def get_command_prefixs(bot: commands.Bot, msg: nextcord.Message):
    prefix = utils.get_prefix(msg.guild.id)
    return [prefix, f"<@{bot.user.id}> ", f"<@!{bot.user.id}> "]

bot = commands.Bot(command_prefix=get_command_prefixs,intents=nextcord.Intents.all())

@bot.check
async def main_check(ctx: commands.Context):
    gdb = GuildDateBases(ctx.guild.id)
    com_name = ctx.command.name
    dis_coms = gdb.get('disabled_commands')
    if com_name in dis_coms:
        raise errors.DisabledCommand('This command is disabled on the server')
    return True


def load_dir(dirpath: str):
    for filename in os.listdir(dirpath):
        if os.path.isfile(f'{dirpath}/{filename}') and filename.endswith(".py") and not filename.startswith("__"):
            fmp = filename[:-3]
            supdirpath = dirpath[2:].split("/")
            findirpatch = '.'.join(supdirpath)
            bot.load_extension(f"{findirpatch}.{fmp}")
        elif os.path.isdir(f'{dirpath}/{filename}'):
            load_dir(f'{dirpath}/{filename}')


def start_bot():
    load_dir("./bot/cogs")
    
    bot.run(env.token_lord_the_tester)