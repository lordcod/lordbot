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
        
        bot.event(self.on_error)
        bot.event(self.on_command_error)
        bot.event(self.on_application_error)
        
        bot.add_check(self.main_check)
    
    async def on_application_error(self, interaction, error):
        pass
    
    async def on_command_error(self, ctx: commands.Context, error):
        CommandError = CallbackCommandError(ctx,error)
        await CommandError.process()
    
    async def on_error(self, event,*args,**kwargs):
        pass
    
    async def main_check(self, ctx: commands.Context):
        gdb = GuildDateBases(ctx.guild.id)
        com_name = ctx.command.qualified_name
        dis_coms = gdb.get('disabled_commands')
        if com_name in dis_coms:
            raise errors.DisabledCommand()
        return True




def setup(bot: commands.Bot):
    event = command_event(bot)
    
    bot.add_cog(event)