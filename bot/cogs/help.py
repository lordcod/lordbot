import math
import re
from typing import Iterable
import nextcord
from nextcord.ext import commands

from bot.languages import help as help_info, i18n
from bot.languages.help import get_command
from bot.databases import GuildDateBases
from bot.misc.lordbot import LordBot
from bot.misc.utils import FissionIterator
from bot.views.help import HelpView


REGEXP_COMMAND_NAME = re.compile(r'([ _\-\.a-zA-Z0-9]+)')


def get_disable_command_value(
    locale: str,
    command: help_info.CommandOption
) -> str:
    return i18n.t(locale,
                  f"help.command-embed.connection_disabled.{int(command.get('allowed_disabled'))}")


def get_using(
    locale: str,
    command: help_info.CommandOption
) -> str:
    _arguments = command.get('arguments')
    arguments = []
    for arg in _arguments:
        if isinstance(arg, dict):
            arguments.append(arg.get(locale))
        else:
            arguments.append(arg)
    return i18n.t(locale, 'help.command-embed.using_command', using=f"{command.get('name')}{' '+' '.join(arguments) if arguments else ''}")


def divise_list(iterable: Iterable, count: int) -> list:
    iterable = list(iterable)
    ret = []
    score = math.ceil(len(iterable)/count)
    for i in range(count):
        ret.append(iterable[score*i:score*(i+1)])
    return ret


class Help(commands.Cog):
    def __init__(self, bot: LordBot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx: commands.Context, *, command_name: str = None):
        self.gdb = GuildDateBases(ctx.guild.id)

        if not command_name:
            await self.generate_message(ctx)
            return

        if not REGEXP_COMMAND_NAME.fullmatch(command_name):
            await self.generate_not_valid(ctx)
            return

        command_data = get_command(command_name)
        if command_data:
            await self.generate_command(ctx, command_data)
            return

        await self.generate_not_found(ctx)

    async def generate_message(self, ctx: commands.Context):
        locale = self.gdb.get('language')
        color = self.gdb.get('color')

        embed = nextcord.Embed(
            title=i18n.t(locale, "help.title"),
            color=color
        )

        for category, coms in help_info.categories.items():
            text = ''
            for cmd in coms:
                text += f"`{cmd.get('name')}` "
            embed.add_field(
                name=f'{help_info.categories_emoji.get(category)}{help_info.categories_name.get(category).get(locale)}',
                value=text,
                inline=False
            )

        view = HelpView(ctx.guild.id)

        await ctx.send(embed=embed, view=view)

    async def generate_command(self, ctx: commands.Context, command_data: help_info.CommandOption):
        locale = self.gdb.get('language')
        color = self.gdb.get('color')
        aliases = command_data.get('aliases')

        embed = nextcord.Embed(
            title=i18n.t(locale, "help.command-embed.title",
                         name=command_data.get('name')),
            description=command_data.get('descriptrion').get(locale),
            color=color
        )
        embed.set_footer(
            text=i18n.t(locale, "help.arguments")
        )
        embed.add_field(
            name=i18n.t(
                locale, 'help.command-embed.info'),
            value=(
                f"{i18n.t(locale, 'help.command-embed.category', category_emoji=help_info.categories_emoji.get(command_data.get('category')), category_name=help_info.categories_name.get(command_data.get('category')).get(locale))}"
                f"{i18n.t(locale, 'help.command-embed.aliases', aliases=', '.join([f'`{al}`' for al in aliases])) if aliases else ''}"
                f"{get_using(locale, command_data)}"
                f"{i18n.t(locale, 'help.command-embed.disable_command', value=get_disable_command_value(locale, command_data))}"
            ),
            inline=False
        )
        if examples := command_data.get('examples'):
            for num, (excmd, descript) in enumerate(examples, start=1):
                embed.add_field(
                    name=i18n.t(
                        locale, 'help.command-embed.example', number=num),
                    value=f"`{excmd}`\n{descript.get(locale)}",
                    inline=False
                )

        if reactions := command_data.get('reactions'):
            react_embed = nextcord.Embed(
                title="Reactions",
                color=color
            )
            for num, reacts in enumerate(divise_list(reactions.items(), count=3), start=1):
                react_embed.add_field(
                    name=num,
                    value='\n'.join([
                        f"{name} - {react.get(locale)}" for name, react in reacts])
                )

            await ctx.send(embeds=[embed, react_embed])
        else:
            await ctx.send(embed=embed)

    async def generate_not_found(self, ctx: commands.Context):
        locale = self.gdb.get('language')
        color = self.gdb.get('color')

        embed = nextcord.Embed(
            title=i18n.t(locale, "help.command-notfound.title"),
            description=i18n.t(locale, "help.command-notfound.description"),
            color=color
        )

        await ctx.send(embed=embed)

    async def generate_not_valid(self, ctx: commands.Context):
        locale = self.gdb.get('language')
        color = self.gdb.get('color')

        embed = nextcord.Embed(
            title=i18n.t(locale, "help.command-invalid.title"),
            description=i18n.t(locale, "help.command-invalid.description"),
            color=color
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
