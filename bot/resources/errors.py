import nextcord
from typing import Union
from nextcord.ext import commands


class DisabledCommand(commands.CommandError):
    pass

class ErrorTypeChannel(Exception):
    pass

class OnlyTeamError(commands.CommandError):
    def __init__(self, author: Union[nextcord.Member,nextcord.User]) -> None:
        self.author: Union[nextcord.Member,nextcord.User] = author
        super().__init__("This command can only be used by the bot team")

class NotActivateEconomy(commands.CommandError):
    pass


class CallbackCommandError:
    def __init__(self,ctx: commands.Context,error) -> None:
        self.ctx = ctx
        self.error = error
    
    async def process(self):
        for error in self.errors:
            name = error.__name__
            error_name = self.error.__class__.__name__
            
            if name == error_name:
                await error(self)
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
        await self.ctx.send(content)
    
    async def CommandOnCooldown(self):
        embed = nextcord.Embed(
            title='The command is on hold',
            description=f'Repeat after {self.error.retry_after :.0f} seconds',
            colour=nextcord.Color.red()
        )
        await self.ctx.send(embed=embed, delete_after=5.0)
    
    async def NotOwner(self):
        content = "This command is intended for the bot owner"
    
    async def CheckFailure(self):
        content = "You don't fulfill all the conditions"
    
    async def BadArgument(self):
        content = "Incorrect arguments"
    
    async def DisabledCommand(self):
        content = f'This command is disabled on the server'
        await self.ctx.send(content)
    
    async def OfterError(self):
        pass
    
    errors = [
        MissingPermissions,MissingRole,MissingAnyRole,BotMissingPermissions,
        CommandNotFound,CommandOnCooldown,NotOwner,CheckFailure,BadArgument,
        DisabledCommand
    ]


