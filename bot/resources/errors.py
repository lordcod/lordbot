import nextcord
from nextcord.ext import commands

from bot.misc.logger import Logger
from bot.misc.time_transformer import display_time
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

class MissingRole(commands.CommandError):
    pass

class MissingChannel(commands.CommandError):
    pass

class CommandOnCooldown(commands.CommandError):
    def __init__(self, retry_after: float) -> None:
        self.retry_after: float = retry_after
        super().__init__("Cooldown")


class CallbackCommandError:
    def __init__(self,ctx: commands.Context, error) -> None:
        self.ctx = ctx
        self.error = error
        
        self.gdb = GuildDateBases(ctx.guild.id)
        self.locale = self.gdb.get('language')
    
    async def process(self):
        Logger.info(f'[{self.error.__class__.__name__}] {self.error}')
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
        
        await self.ctx.send(content)
    
    async def BotMissingPermissions(self):
        content = errors.BotMissingPermissions.get(self.locale)
        
        await self.ctx.send(content)
    
    async def MissingRole(self):
        content = errors.MissingRole.get(self.locale)
        
        await self.ctx.send(content)
    
    async def MissingChannel(self):
        content = errors.MissingChannel.get(self.locale)
        
        await self.ctx.send(content)
    
    
    async def CommandNotFound(self):
        content = errors.CommandNotFound.get(self.locale)
        
        await self.ctx.send(
            content=content,
            delete_after=5
        )
    
    async def CommandOnCooldown(self):
        color = self.gdb.get('color')
        
        embed = nextcord.Embed(
            title=errors.CommandOnCooldown.title.get(self.locale),
            description=f'{errors.CommandOnCooldown.description.get(self.locale)} {display_time(self.error.retry_after, self.locale)}',
            color=color
        )
        
        await self.ctx.send(embed=embed, delete_after=5.0)
    
    async def NotOwner(self):
        content = errors.NotOwner.get(self.locale)
        
        await self.ctx.send(content=content)
    
    async def CheckFailure(self):
        content = errors.CheckFailure.get(self.locale)
        
        await self.ctx.send(content)
    
    async def BadArgument(self):
        content = errors.BadArgument.get(self.locale)
        
        await self.ctx.send(content)
    
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
    
    async def MemberNotFound(self):
        content = errors.MemberNotFound.get(self.locale)
        
        await self.ctx.send(content)
    
    async def BadUnionArgument(self):
        await self.BadArgument()
    
    async def OfterError(self):
        content = f'OfterError, {self.error.__class__.__name__}'
        # await self.ctx.send(content)
    
    errors = [
        MissingPermissions,MissingRole,MissingChannel,BotMissingPermissions,
        DisabledCommand,CommandNotFound,CommandOnCooldown,NotOwner,CheckFailure,
        BadArgument,MissingRequiredArgument,OnlyTeamError,NotActivateEconomy,
        MemberNotFound,BadUnionArgument
    ]


