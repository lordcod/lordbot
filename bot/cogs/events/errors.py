import nextcord
from nextcord.ext import commands

from bot.databases.db import GuildDateBases
from bot.resources import errors
from bot.resources.errors import CallbackCommandError



class command_event(commands.Cog):
    bot: commands.Bot
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()
    
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        CommandError = CallbackCommandError(ctx,error)
        await CommandError.process()

    @commands.Cog.listener()
    async def on_error(event,*args,**kwargs):
        pass
    
    @commands.Cog.bot_check()
    async def main_check(ctx: commands.Context):
        gdb = GuildDateBases(ctx.guild.id)
        com_name = ctx.command.name
        dis_coms = gdb.get('disabled_commands')
        if com_name in dis_coms:
            raise errors.DisabledCommand('This command is disabled on the server')
        return True




def setup(bot: commands.Bot):
    event = command_event(bot)
    
    bot.add_cog(event)