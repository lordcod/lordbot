import nextcord
from nextcord.ext import commands

from bot.misc.logger import Logger
from bot.misc.time_transformer import display_time
from bot.databases.db import GuildDateBases
from bot.languages import i18n

from inspect import Parameter
from typing import Union


class ErrorTypeChannel(Exception):
    pass


class DisabledCommand(commands.CommandError):
    pass


class OnlyTeamError(commands.CommandError):
    def __init__(self, author: Union[nextcord.Member, nextcord.User]) -> None:
        self.author: Union[nextcord.Member, nextcord.User] = author
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
    def __init__(self, ctx: commands.Context, error) -> None:
        self.ctx = ctx
        self.error = error

        self.gdb = GuildDateBases(ctx.guild.id)
        self.locale = self.gdb.get('language')

    async def process(self):
        Logger.info(f'[{self.error.__class__.__name__}] {self.error}')
        error_name = self.error.__class__.__name__
        if error_coro := getattr(self, error_name, None):
            await error_coro()
        else:
            await self.OfterError()

    async def MissingPermissions(self):
        content = i18n.t(self.locale, 'errors.MissingPermissions')

        await self.ctx.send(content)

    async def BotMissingPermissions(self):
        content = i18n.t(self.locale, 'errors.BotMissingPermissions')

        await self.ctx.send(content)

    async def MissingRole(self):
        content = i18n.t(self.locale, 'errors.MissingRole')

        await self.ctx.send(content)

    async def MissingChannel(self):
        content = i18n.t(self.locale, 'errors.MissingChannel')

        await self.ctx.send(content)

    async def CommandNotFound(self):
        content = i18n.t(self.locale, 'errors.CommandNotFound')

        await self.ctx.send(
            content=content,
            delete_after=5
        )

    async def CommandOnCooldown(self):
        color = self.gdb.get('color')

        embed = nextcord.Embed(
            title=i18n.t(self.locale, 'errors.CommandOnCooldown.title'),
            description=i18n.t(self.locale, 'errors.CommandOnCooldown.description',
                               delay=display_time(self.error.retry_after,
                                                  self.locale)),
            color=color
        )

        await self.ctx.send(embed=embed, delete_after=5.0)

    async def NotOwner(self):
        content = i18n.t(self.locale, 'errors.NotOwner')

        await self.ctx.send(content=content)

    async def BadArgument(self):
        content = i18n.t(self.locale, 'errors.BadArgument')

        await self.ctx.send(content)

    async def DisabledCommand(self):
        content = i18n.t(self.locale, 'errors.DisabledCommand')

        await self.ctx.send(content)

    async def MissingRequiredArgument(self):
        content = i18n.t(self.locale, 'errors.MissingRequiredArgument')

        await self.ctx.send(content)

    async def NotActivateEconomy(self):
        content = i18n.t(self.locale, 'errors.NotActivateEconomy')

        await self.ctx.send(content)

    async def OnlyTeamError(self):
        content = i18n.t(self.locale, 'errors.OnlyTeamError')

        await self.ctx.send(content)

    async def MemberNotFound(self):
        content = i18n.t(self.locale, 'errors.MemberNotFound')

        await self.ctx.send(content)

    async def BadUnionArgument(self):
        await self.BadArgument()

    async def OfterError(self):
        pass
