import nextcord
from typing import Union
from nextcord.ext import commands



class CallbackCommandError:
    async def __init__(self,ctx: commands.Context, error) -> None:
        self.ctx = ctx
        self.error = error
        for err in self.errors:
            name = err.__name__
            if isinstance(error,getattr(commands,name)):
                await err(ctx,error)
                break
        else:
            await self.OfterError()
    
    
    async def MissingPermissions(self):
        content = "The user does not have enough rights"
    
    async def MissingRole(self):
        content = "You don't have the right role to execute the command"
    
    async def MissingAnyRole(self):
        content = "You don't have the right or the right roles to execute the command"
    
    async def BotMissingPermissions(self):
        content = "The bot doesn't have enough rights"
    
    async def CommandNotFound(self):
        content = "There is no such command"
    
    async def CommandOnCooldown(self):
        error = self.error
        embed = nextcord.Embed(
            title='The command is on hold',
            description=f'Repeat after {error.retry_after :.0f} seconds',
            colour=nextcord.Color.red()
        )
    
    async def NotOwner(self):
        content = "This command is intended for the bot owner"
    
    async def CheckFailure(self):
        content = "You don't fulfill all the conditions"
    
    async def BadArgument(self):
        content = "Incorrect arguments"
    
    async def OfterError(self):
        pass
    
    errors = [
        MissingPermissions,MissingRole,MissingAnyRole,BotMissingPermissions,
        CommandNotFound,CommandOnCooldown,NotOwner,CheckFailure,BadArgument,
    ]


class ErrorTypeChannel(Exception):
    pass

class OnlyTeamError(commands.CommandError):
    def __init__(self, author: Union[nextcord.Member,nextcord.User]) -> None:
        self.author: Union[nextcord.Member,nextcord.User] = author
        super().__init__("This command can only be used by the bot team")

class NotActivateEconomy(commands.CommandError):
    pass