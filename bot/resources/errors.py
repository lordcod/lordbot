import nextcord
from nextcord.ext import commands

from bot.misc.logger import Logger
from bot.databases.db import GuildDateBases
from bot.languages import errors

from inspect import Parameter
from typing import Union

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
    def __init__(self,ctx: commands.Context, error) -> None:
        self.ctx = ctx
        self.error = error
        
        self.gdb = GuildDateBases(ctx.guild.id)
        self.locale = self.gdb.get('language')
    
    async def process(self):
        Logger.info(self.error)
        for error in self.errors:
            name = error.__name__
            error_name = self.error.__class__.__name__
            
            if name == error_name:
                await error(self)
                break
        else:
            await self.OfterError()
    
    async def MissingPermissions(self):
        content = errors.MissingPermissions.get(self.locale)
        
        await self.ctx.send(
            content=content
        )
    
    async def MissingRole(self):
        content = "You don't have the right role to execute the command"
        
        await self.ctx.send(
            content=content
        )
    
    async def BotMissingPermissions(self):
        content = "The bot doesn't have enough rights"
        
        await self.ctx.send(
            content=content
        )
    
    
    async def CommandNotFound(self):
        content = "There is no such command"
        
        await self.ctx.send(
            content=content,
            delete_after=5
        )
    
    async def CommandOnCooldown(self):
        embed = nextcord.Embed(
            title='The command is on hold',
            description=f'Repeat after {self.error.retry_after :.0f} seconds',
            colour=nextcord.Color.red()
        )
        
        await self.ctx.send(embed=embed, delete_after=5.0)
    
    async def NotOwner(self):
        content = "This command is intended for the bot owner"
        
        await self.ctx.send(
            content=content
        )
    
    async def CheckFailure(self):
        content = "You don't fulfill all the conditions"
        
        await self.ctx.send(
            content=content
        )
    
    async def BadArgument(self):
        content = "Incorrect arguments"
        
        await self.ctx.send(
            content=content
        )
    
    async def DisabledCommand(self):
        content = f'This command is disabled on the server'
        
        await self.ctx.send(content)
    
    async def MissingRequiredArgument(self):
        param: Parameter = self.error.param
        content = f'You didn\'t enter a required argument - {param.name}'
        
        await self.ctx.send(content)
    
    async def OfterError(self):
        content = f'OfterError, {self.error.__name__}'
        # await self.ctx.send(content)
    
    errors = [
        MissingPermissions,MissingRole,BotMissingPermissions,DisabledCommand,
        CommandNotFound,CommandOnCooldown,NotOwner,CheckFailure,BadArgument,
        MissingRequiredArgument
    ]


