import nextcord
from nextcord.ext import commands

from bot.misc.logger import Logger
from bot.databases.db import GuildDateBases
from bot.languages import errors

from inspect import Parameter
from typing import Union

class ErrorTypeChannel(Exception):
    pass

class DisabledCommand(commands.CommandError):
    pass

class OnlyTeamError(commands.CommandError):
    def __init__(self, author: Union[nextcord.Member,nextcord.User]) -> None:
        self.author: Union[nextcord.Member,nextcord.User] = author
        super().__init__()

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
    
    async def BotMissingPermissions(self):
        content = errors.BotMissingPermissions.get(self.locale)
        
        await self.ctx.send(
            content=content
        )
    
    async def MissingRole(self):
        content = errors.MissingRole.get(self.locale)
        
        await self.ctx.send(
            content=content
        )
    
    
    async def CommandNotFound(self):
        content = errors.CommandNotFound.get(self.locale)
        
        await self.ctx.send(
            content=content,
            delete_after=5
        )
    
    async def CommandOnCooldown(self):
        embed = nextcord.Embed(
            title=errors.CommandOnCooldown.title.get(self.locale),
            description=(
                f'{errors.CommandOnCooldown.description.get(self.locale)}'
                f'{self.error.retry_after :.0f}'
                f'{errors.CommandOnCooldown.seconds.get(self.locale)}'
            ),
            colour=nextcord.Color.red()
        )
        
        await self.ctx.send(embed=embed, delete_after=5.0)
    
    async def NotOwner(self):
        content = errors.NotOwner.get(self.locale)
        
        await self.ctx.send(
            content=content
        )
    
    async def CheckFailure(self):
        content = errors.CheckFailure.get(self.locale)
        
        await self.ctx.send(
            content=content
        )
    
    async def BadArgument(self):
        content = errors.BadArgument.get(self.locale)
        
        await self.ctx.send(
            content=content
        )
    
    async def DisabledCommand(self):
        content = errors.DisabledCommand.get(self.locale)
        
        await self.ctx.send(content)
    
    async def MissingRequiredArgument(self):
        param: Parameter = self.error.param
        content = f'{errors.MissingRequiredArgument.get(self.locale)} - {param.name}'
        
        await self.ctx.send(content)
    
    async def NotActivateEconomy(self):
        content = errors.NotActivateEconomy.get(self.locale)
        
        await self.ctx.send(content)
    
    async def OnlyTeamError(self):
        content = errors.OnlyTeamError.get(self.locale)
        
        await self.ctx.send(content)
    
    async def OfterError(self):
        content = f'OfterError, {self.error.__class__.__name__}'
        # await self.ctx.send(content)
    
    errors = [
        MissingPermissions,MissingRole,BotMissingPermissions,DisabledCommand,
        CommandNotFound,CommandOnCooldown,NotOwner,CheckFailure,BadArgument,
        MissingRequiredArgument,OnlyTeamError,NotActivateEconomy
    ]


