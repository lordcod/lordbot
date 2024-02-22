import nextcord
from nextcord.ext import commands

from bot.languages import help as help_info
from bot.languages.help import get_command
from bot.databases.db import GuildDateBases
from bot.misc.lordbot import LordBot
from bot.views.help import HelpView

import re


def is_valid_command(name: str) -> bool:
    pattern = r'([ _\-\.a-zA-Z]+)'
    result = re.fullmatch(pattern, name)
    if result:
        return True
    return False


class help(commands.Cog):
    def __init__(self, bot: LordBot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx: commands.Context, *, command_name: str = None):
        self.gdb = GuildDateBases(ctx.guild.id)

        if not command_name:
            await self.generate_message(ctx)
            return

        if not is_valid_command(command_name):
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
            title=help_info.Embed.title.get(locale),
            description=help_info.Embed.description.get(locale),
            color=color
        )

        for category, coms in help_info.categories.items():
            text = ''
            for cmd in coms:
                text = (
                    f"{text}"
                    f"`{cmd.get('name')}` "
                )
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
        arguments = command_data.get('arguments')

        embed = nextcord.Embed(
            title=help_info.Embed.title.get(locale),
            description=help_info.Embed.description.get(locale),
            color=color
        )

        embed.add_field(
            name=help_info.CommandEmbed.name.get(locale),
            value=command_data.get('name')
        )

        embed.add_field(
            name=help_info.CommandEmbed.category.get(locale),
            value=f"{help_info.categories_emoji.get(command_data.get('category'))}{help_info.categories_name.get(command_data.get('category')).get(locale)}"
        )

        embed.add_field(
            name='',
            value='',
            inline=False
        )

        if aliases:
            embed.add_field(
                name=help_info.CommandEmbed.aliases.get(locale),
                value=', '.join(aliases)
            )

        if arguments:
            embed.add_field(
                name=help_info.CommandEmbed.arguments.get(locale),
                value=' '.join(arguments)
            )
            embed.set_footer(
                text=help_info.Embed.footer.get(locale)
            )

        embed.add_field(
            name=help_info.CommandEmbed.disable_command.get(locale),
            value=help_info.CommandEmbed.connection_disabled.get(
                command_data.get('allowed_disabled')).get(locale),
            inline=False
        )

        embed.add_field(
            name=help_info.CommandEmbed.description.get(locale),
            value=command_data.get('descriptrion').get(locale),
            inline=False
        )

        await ctx.send(embed=embed)

    async def generate_not_found(self, ctx: commands.Context):
        locale = self.gdb.get('language')
        color = self.gdb.get('color')

        embed = nextcord.Embed(
            title=help_info.CommandNotFound.title.get(locale),
            description=help_info.CommandNotFound.description.get(locale),
            color=color
        )

        await ctx.send(embed=embed)

    async def generate_not_valid(self, ctx: commands.Context):
        locale = self.gdb.get('language')
        color = self.gdb.get('color')

        embed = nextcord.Embed(
            title=help_info.CommandNotValid.title.get(locale),
            description=help_info.CommandNotValid.description.get(locale),
            color=color
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(help(bot))
