import nextcord
import random
import string
from nextcord.ext import commands
from bot.databases.handlers.guildHD import GuildDateBases
from bot.misc.lordbot import LordBot

from bot.misc.ratelimit import Cooldown
from bot.misc.logger import Logger
from bot.resources import errors
from bot.databases import CommandDB
from bot.resources.errors import (CallbackCommandError,
                                  MissingRole,
                                  MissingChannel,
                                  CommandOnCooldown)


class PermissionChecker:
    def __init__(self, ctx: commands.Context) -> None:
        self.ctx = ctx

    async def process(self) -> bool:
        ctx = self.ctx
        command_name = ctx.command.qualified_name
        cdb = CommandDB(ctx.guild.id)
        self.command_permissions = cdb.get(command_name, {})

        enabled = await self.is_enabled()
        allowed = await self.is_allowed()

        answer = enabled & allowed
        return answer

    async def is_enabled(self):
        "Checks whether it is enabled"
        command_permissions = self.command_permissions
        operate = command_permissions.get("operate", 1)

        if operate == 0:
            raise errors.DisabledCommand()
        return True

    async def is_allowed(self):
        "Checks if there are permissions to use the command"
        command_permissions = self.command_permissions
        distribution: dict = command_permissions.get("distribution", {})

        for type, data in distribution.items():
            meaning = self.allowed_types[type]
            value = await meaning(self, data)
            if not value:
                return False
        return True

    async def _is_allowed_role(self, data: dict) -> bool:
        "The `is_allowed` subsection is needed to verify roles"
        ctx = self.ctx
        author = ctx.author
        aut_roles_ids = author._roles

        if not data:
            return True

        common = set(data) & set(aut_roles_ids)
        if not common:
            raise MissingRole()
        return True

    async def _is_allowed_channel(self, data: dict) -> bool:
        "The `is_allowed` subsection is needed to verify channels"
        ctx = self.ctx
        channel = ctx.channel
        channels_ids = data.get("channels", [])
        categories_ids = data.get("categories", [])

        if not (channel.id in channels_ids or
                channel.category_id in categories_ids):
            raise MissingChannel()
        return True

    async def _is_cooldown(self, data: dict) -> bool:
        ctx = self.ctx

        cooldown = Cooldown.from_message(
            ctx.command.qualified_name,
            data,
            ctx.message
        )
        ctx.cooldown = cooldown
        retry = cooldown.get()

        if retry is None:
            return True
        elif isinstance(retry, float):
            raise CommandOnCooldown(retry)
        else:
            raise TypeError(retry)

    allowed_types = {
        'allow-role': _is_allowed_role,
        'allow-channel': _is_allowed_channel,
        'cooldown': _is_cooldown
    }


class CommandEvent(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        super().__init__()

        bot.after_invoke(self.after_invoke)
        bot.set_event(self.on_error)
        bot.set_event(self.on_command_error)
        bot.set_event(self.on_application_error)

        bot.add_check(self.permission_check)

    async def on_application_error(
            self, interaction: nextcord.Interaction, error: Exception):
        if interaction.response.is_done():
            return

        gdb = GuildDateBases(interaction.guild_id)
        color = gdb.get('color')

        random_hex_key = ''.join(
            [random.choice(string.hexdigits) for _ in range(10)])

        embed = nextcord.Embed(
            title="The interaction time has expired",
            description=(
                "A critical error occurred while processing the command\n"
                f"Error key: **{random_hex_key}**"
            ),
            color=color
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

        Logger.error(
            f"[{type(error).__name__}] Application error: {error}\nError key: {random_hex_key}")

    async def on_command_error(self, ctx: commands.Context, error):
        CommandError = CallbackCommandError(ctx, error)
        await CommandError.process()

    async def on_error(self, event, *args, **kwargs):
        Logger.error(event)

    async def permission_check(self,  ctx: commands.Context):
        perch = PermissionChecker(ctx)
        answer = await perch.process()

        return answer

    async def after_invoke(self, ctx: commands.Context) -> None:
        if cooldown := getattr(ctx, 'cooldown', None):
            cooldown.add()


def setup(bot):
    bot.add_cog(CommandEvent(bot))
