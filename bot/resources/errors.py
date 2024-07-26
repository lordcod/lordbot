from __future__ import annotations

from asyncio import iscoroutinefunction
import functools
import inspect
import logging
import nextcord
from nextcord.ext import commands

from bot.misc.time_transformer import display_time
from bot.databases import GuildDateBases
from bot.languages import i18n
from bot.languages.help import CommandOption, get_command

from typing import TypeVar, Union

from bot.resources.info import DISCORD_SUPPORT_SERVER

_log = logging.getLogger(__name__)
ExceptionT = TypeVar("ExceptionT", bound=BaseException)


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


def attach_exception(*errors: type[ExceptionT]):
    def inner(func):
        func.__attachment_errors__ = errors

        @functools.wraps(func)
        def wrapped(self: CallbackCommandError, error: ExceptionT):
            return func(self, error)
        return func
    return inner


class CommandOnCooldown(commands.CommandError):
    def __init__(self, retry_after: float) -> None:
        self.retry_after: float = retry_after
        super().__init__("Cooldown")


class CallbackCommandError:
    def __init__(self, ctx: commands.Context) -> None:
        self.ctx = ctx
        self.gdb = GuildDateBases(ctx.guild.id)
        self.locale = None

    @classmethod
    async def process(cls, ctx: commands.Context, error):
        self = cls(ctx)
        self.locale = await self.gdb.get('language')

        for name, item in inspect.getmembers(self):
            allow_errors = getattr(item, "__attachment_errors__", None)
            if allow_errors is None or not iscoroutinefunction(item):
                continue

            if isinstance(error, allow_errors):
                await item(error)
                break
        else:
            await self.OfterError(error)

    @attach_exception(commands.MissingPermissions)
    async def MissingPermissions(self, error):
        content = i18n.t(self.locale, 'errors.MissingPermissions')

        await self.ctx.send(content)

    @attach_exception(commands.BotMissingPermissions)
    async def BotMissingPermissions(self, error):

        content = i18n.t(self.locale, 'errors.BotMissingPermissions')

        await self.ctx.send(content)

    @attach_exception(MissingRole)
    async def MissingRole(self, error):
        content = i18n.t(self.locale, 'errors.MissingRole')

        await self.ctx.send(content)

    @attach_exception(MissingChannel)
    async def MissingChannel(self, error):
        content = i18n.t(self.locale, 'errors.MissingChannel')

        await self.ctx.send(content)

    @attach_exception(commands.CommandNotFound)
    async def CommandNotFound(self, error):
        pass

    @attach_exception(commands.NotOwner)
    async def NotOwner(self, error):
        content = i18n.t(self.locale, 'errors.NotOwner')

        await self.ctx.send(content=content)

    @attach_exception(OnlyTeamError)
    async def OnlyTeamError(self, error):
        content = i18n.t(self.locale, 'errors.OnlyTeamError')

        await self.ctx.send(content)

    @attach_exception(commands.BadArgument)
    async def BadArgument(self, error):
        title = i18n.t(self.locale, 'errors.BadArgument')
        color = await self.gdb.get('color')

        cmd_data = get_command(self.ctx.command.qualified_name)

        if cmd_data is None:
            return

        using = f"`{cmd_data.get('name')}{' '+' '.join(CommandOption.get_arguments(cmd_data ,self.locale)) if cmd_data.get('arguments') else ''}`"

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
    async def MissingRequiredArgument(self, error):
        title = i18n.t(self.locale, 'errors.MissingRequiredArgument')
        color = await self.gdb.get('color')

        cmd_data = get_command(self.ctx.command.name)

        if cmd_data is None:
            return

        using = f"`{cmd_data.get('name')}{' '+' '.join(CommandOption.get_arguments(cmd_data ,self.locale)) if cmd_data.get('arguments') else ''}`"

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
    async def CommandOnCooldown(self, error):
        color = await self.gdb.get('color')

        embed = nextcord.Embed(
            title=i18n.t(self.locale, 'errors.CommandOnCooldown.title'),
            description=i18n.t(self.locale, 'errors.CommandOnCooldown.description',
                               delay=display_time(error.retry_after,
                                                  self.locale)),
            color=color
        )

        await self.ctx.send(embed=embed, delete_after=5.0)

    @attach_exception(InactiveEconomy)
    async def InactiveEconomy(self, error):
        content = i18n.t(self.locale, 'errors.InactiveEconomy')

        await self.ctx.send(content)

    @attach_exception(DisabledCommand, commands.DisabledCommand)
    async def DisabledCommand(self, error):
        content = i18n.t(self.locale, 'errors.DisabledCommand')

        await self.ctx.send(content)

    async def OfterError(self, error):
        _log.error(
            "Ignoring exception in command %s", self.ctx.command, exc_info=error)

        await self.ctx.author.send(
            "There's been some kind of mistake!\n"
            "Check if the bot has the necessary permissions to execute this command!\n"
            f"Error ID (required for support): specify the name of the commands\n"
            f"If you couldn't figure out what's going on, contact the [support server]({DISCORD_SUPPORT_SERVER})!",
            flags=nextcord.MessageFlags(suppress_embeds=True, suppress_notifications=True)
        )
