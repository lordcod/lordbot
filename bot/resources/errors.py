from asyncio import iscoroutinefunction
import inspect
import logging
import nextcord
from nextcord.ext import commands

from bot.misc.time_transformer import display_time
from bot.databases import GuildDateBases
from bot.languages import i18n
from bot.languages.help import get_command

from typing import TypeVar, Union

_log = logging.getLogger(__name__)


class DisabledCommand(commands.CheckFailure):
    pass


class OnlyTeamError(commands.CheckFailure):
    def __init__(self, author: Union[nextcord.Member, nextcord.User]) -> None:
        self.author: Union[nextcord.Member, nextcord.User] = author
        super().__init__()


class InactiveEconomy(commands.CheckFailure):
    pass


class MissingRole(commands.CheckFailure):
    pass


class MissingChannel(commands.CheckFailure):
    pass


def attach_exception(*errors: BaseException):
    def wrapped(func):
        func.__attachment_errors__ = errors
        return func
    return wrapped


class CommandOnCooldown(commands.CommandError):
    def __init__(self, retry_after: float) -> None:
        self.retry_after: float = retry_after
        super().__init__("Cooldown")


class CallbackCommandError:
    def __init__(self, ctx: commands.Context, error: BaseException) -> None:
        self.ctx = ctx
        self.error: BaseException = error

    async def process(self):
        self.gdb = GuildDateBases(self.ctx.guild.id)
        self.locale = await self.gdb.get('language')

        for name, item in inspect.getmembers(self):
            allow_errors = getattr(item, "__attachment_errors__", None)
            if allow_errors is None or not iscoroutinefunction(item):
                continue

            if isinstance(self.error, allow_errors):
                await item()
                break
        else:
            raise self.error

    @attach_exception(commands.MissingPermissions)
    async def MissingPermissions(self):
        content = i18n.t(self.locale, 'errors.MissingPermissions')

        await self.ctx.send(content)

    @attach_exception(commands.BotMissingPermissions)
    async def BotMissingPermissions(self):
        content = i18n.t(self.locale, 'errors.BotMissingPermissions')

        await self.ctx.send(content)

    @attach_exception(MissingRole)
    async def MissingRole(self):
        content = i18n.t(self.locale, 'errors.MissingRole')

        await self.ctx.send(content)

    @attach_exception(MissingChannel)
    async def MissingChannel(self):
        content = i18n.t(self.locale, 'errors.MissingChannel')

        await self.ctx.send(content)

    @attach_exception(commands.CommandNotFound)
    async def CommandNotFound(self):
        content = i18n.t(self.locale, 'errors.CommandNotFound')

        await self.ctx.send(
            content=content,
            delete_after=5
        )

    @attach_exception(commands.NotOwner)
    async def NotOwner(self):
        content = i18n.t(self.locale, 'errors.NotOwner')

        await self.ctx.send(content=content)

    @attach_exception(OnlyTeamError)
    async def OnlyTeamError(self):
        content = i18n.t(self.locale, 'errors.OnlyTeamError')

        await self.ctx.send(content)

    @attach_exception(commands.BadArgument)
    async def BadArgument(self):
        title = i18n.t(self.locale, 'errors.BadArgument')
        color = await self.gdb.get('color')

        cmd_data = get_command(self.ctx.command.name)
        using = f"`{cmd_data.get('name')}{' '+' '.join(cmd_data.get('arguments')) if cmd_data.get('arguments') else ''}`"

        embed = nextcord.Embed(
            title=title,
            description=i18n.t(
                self.locale, "help.command-embed.using_command", using=using),
            color=color
        )
        embed.set_footer(text=i18n.t(
            self.locale, "help.arguments"))

        if examples := cmd_data.get('examples'):
            for num, (excmd, descript) in enumerate(examples, start=1):
                embed.add_field(
                    name=i18n.t(
                        self.locale, 'help.command-embed.example', number=num),
                    value=f"`{excmd}`\n{descript.get(self.locale)}",
                    inline=False
                )

        await self.ctx.send(embed=embed)

    @attach_exception(commands.MissingRequiredArgument)
    async def MissingRequiredArgument(self):
        title = i18n.t(self.locale, 'errors.MissingRequiredArgument')
        color = await self.gdb.get('color')

        cmd_data = get_command(self.ctx.command.name)
        using = f"`{cmd_data.get('name')}{' '+' '.join([arg.get(self.locale) for arg in cmd_data.get('arguments')]) if cmd_data.get('arguments') else ''}`"

        embed = nextcord.Embed(
            title=title,
            description=i18n.t(
                self.locale, "help.command-embed.using_command", using=using),
            color=color
        )
        embed.set_footer(text=i18n.t(
            self.locale, "help.arguments"))

        if examples := cmd_data.get('examples'):
            for num, (excmd, descript) in enumerate(examples, start=1):
                embed.add_field(
                    name=i18n.t(
                        self.locale, 'help.command-embed.example', number=num),
                    value=f"`{excmd}`\n{descript.get(self.locale)}",
                    inline=False
                )

        await self.ctx.send(embed=embed)

    @attach_exception(CommandOnCooldown)
    async def CommandOnCooldown(self):
        color = await self.gdb.get('color')

        embed = nextcord.Embed(
            title=i18n.t(self.locale, 'errors.CommandOnCooldown.title'),
            description=i18n.t(self.locale, 'errors.CommandOnCooldown.description',
                               delay=display_time(self.error.retry_after,
                                                  self.locale)),
            color=color
        )

        await self.ctx.send(embed=embed, delete_after=5.0)

    @attach_exception(InactiveEconomy)
    async def InactiveEconomy(self):
        content = i18n.t(self.locale, 'errors.InactiveEconomy')

        await self.ctx.send(content)

    @attach_exception(DisabledCommand, commands.DisabledCommand)
    async def DisabledCommand(self):
        content = i18n.t(self.locale, 'errors.DisabledCommand')

        await self.ctx.send(content)

    async def OfterError(self):
        _log.debug(f"[{self.error.__class__.__name__}]: {self.error}")
