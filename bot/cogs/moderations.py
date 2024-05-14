
import nextcord
from nextcord.ext import commands, application_checks

from bot.misc import utils
from bot.misc.utils import TimeCalculator
from bot.misc.lordbot import LordBot
from bot.misc.time_transformer import display_time
from bot.views.settings_menu import SettingsView
from bot.views.delcat import DelCatView
from bot.databases import RoleDateBases, BanDateBases, GuildDateBases

import io
import time
from typing import Optional
time_now = None
time_stamp = None


class Moderations(commands.Cog):
    def __init__(self, bot: LordBot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def say(self, ctx: commands.Context, *, message: str):
        files = []
        for attach in ctx.message.attachments:
            data = io.BytesIO(await attach.read())
            files.append(nextcord.File(data, attach.filename))

        res = await utils.generate_message(message)

        await ctx.send(**res, files=files)

        await ctx.message.delete()

    @commands.command(aliases=["set", "setting"])
    @commands.has_permissions(manage_guild=True)
    async def settings(self, ctx: commands.Context):
        view = SettingsView(ctx.author)

        await ctx.send(embed=view.embed, view=view)

    @nextcord.slash_command(name="delete-category", default_member_permissions=48)
    @application_checks.has_permissions(manage_channels=True)
    async def deletecategory(self, interaction: nextcord.Interaction, category: nextcord.CategoryChannel):
        view = DelCatView(interaction.user, category)

        await interaction.response.send_message(embed=view.embed, view=view)

    @commands.group(name='ban', aliases=["tempban"], invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    async def temp_ban(
        self,
        ctx: commands.Context,
        member: nextcord.Member,
        ftime: Optional[TimeCalculator] = None,
        *,
        reason: Optional[str] = None
    ):
        gdb = GuildDateBases(ctx.guild.id)
        bsdb = BanDateBases(ctx.guild.id, member.id)
        locale = gdb.get('language')
        color = gdb.get('color')

        self.bot.lord_handler_timer.close_as_key(
            f"ban:{ctx.guild.id}:{member.id}")

        embed = nextcord.Embed(
            title="Temporary ban granted!",
            description=(
                f"Banned: {member.name}({member.id})\n"
                f"Moderator: {ctx.author.name}({ctx.author.id})"
            ),
            color=color
        )
        if ftime is not None:
            embed.add_field(
                name="Time of action",
                value=f"<t:{ftime+time.time() :.0f}:f> ({display_time(ftime, locale)})",
                inline=False
            )
        if reason is not None:
            embed.add_field(
                name='Reason',
                value=reason,
                inline=False
            )
        if ftime is not None:
            self.bot.lord_handler_timer.create_timer_handler(
                ftime, bsdb.remove_ban(ctx.guild._state), f"ban:{ctx.guild.id}:{member.id}")

            bsdb.insert(ftime+time.time())

        await member.ban(reason=reason)

        await ctx.send(embed=embed)

    @temp_ban.command(name='list')
    async def temp_ban_list(self, ctx: commands.Context):
        gdb = GuildDateBases(ctx.guild.id)
        color = gdb.get('color')

        rsdb = BanDateBases(ctx.guild.id)
        datas = rsdb.get_as_guild()

        message = ""

        for quantity, (member_id, ban_time) in enumerate(datas):
            message += f"{quantity}. <@{member_id}>(<t:{ban_time}:R>)\n"

        message = message or "There are no registered temporary roles on this server"
        embed = nextcord.Embed(
            title="Temp Bans",
            description=message,
            color=color
        )

        await ctx.send(embed=embed)

    @commands.group(name='temp-role', invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    async def temp_role(
        self,
        ctx: commands.Context,
        member: nextcord.Member,
        role: nextcord.Role,
        ftime: TimeCalculator
    ):
        gdb = GuildDateBases(ctx.guild.id)
        rsdb = RoleDateBases(ctx.guild.id, member.id)
        locale = gdb.get('language')
        color = gdb.get('color')
        _role_time = rsdb.get_as_role(role.id)

        if _role_time is not None:
            self.bot.lord_handler_timer.close_as_key(
                f"role:{ctx.guild.id}:{member.id}:{role.id}")
            embed = nextcord.Embed(
                title="The duration of the role has been changed",
                color=color)
            embed.add_field(
                name='Role',
                value=f'{member.mention} → {role.mention} (ROLE ID: {role.id})',
                inline=False
            )
            embed.add_field(
                name='New time of action',
                value=f'<t:{_role_time[0]}:f> → <t:{ftime+time.time() :.0f}:f> ({display_time(ftime, locale)})',
                inline=False
            )
        else:
            embed = nextcord.Embed(
                title="Temporary role granted!",
                color=color)
            embed.add_field(
                name="Role",
                value=f'{member.mention} → {role.mention} (ROLE ID: {role.id})',
                inline=False
            )
            embed.add_field(
                name="Time of action",
                value=f"<t:{ftime+time.time() :.0f}:f> ({display_time(ftime)})",
                inline=False
            )

        rsdb.set_role(role.id, ftime+time.time())

        self.bot.lord_handler_timer.create_timer_handler(
            ftime, rsdb.remove_role(member, role), f"role:{ctx.guild.id}:{member.id}:{role.id}")

        await member.add_roles(role)

        await ctx.send(embed=embed)

    @temp_role.command(name='list')
    async def temp_role_list(self, ctx: commands.Context, member: Optional[nextcord.Member] = None):
        gdb = GuildDateBases(ctx.guild.id)
        color = gdb.get('color')

        if member is not None:
            rsdb = RoleDateBases(ctx.guild.id, member.id)
            datas = rsdb.get_as_member()
        else:
            rsdb = RoleDateBases(ctx.guild.id)
            datas = rsdb.get_as_guild()

        message = ""

        for quantity, (member_id, role_id, role_time) in enumerate(datas):
            member = ctx.guild.get_member(member_id)
            role = ctx.guild.get_role(role_id)

            if not (role and member):
                continue

            message += f"{quantity}. {member.mention} → {role.mention} (<t:{role_time}:R>)\n"

        message = message or "There are no registered temporary roles on this server"
        embed = nextcord.Embed(
            title="Temp Roles",
            description=message,
            color=color
        )

        await ctx.send(embed=embed)

    @nextcord.slash_command(
        name='clone',
        default_member_permissions=268435456
    )
    async def clone(
        self,
        interaction: nextcord.Interaction
    ) -> None:
        pass

    @clone.subcommand(
        name='role',
        description='If you want to copy the role but still keep the rights, then this is the command for you'
    )
    async def clone_role(
        self,
        interaction: nextcord.Interaction,
        role: nextcord.Role = nextcord.SlashOption(
            name='role',
            description='Select the role you want to copy',
            required=True
        ),
        name: str = nextcord.SlashOption(
            name='name',
            description='When creating a new role, this name will be specified',
            required=False
        )
    ) -> None:
        role_name = name or role.name

        new_role = await interaction.guild.create_role(
            reason="Copying a role with rights",
            name=role_name,
            permissions=role.permissions,
            color=role.color,
            hoist=role.hoist,
            mentionable=role.mentionable,
            icon=role.icon
        )

        await interaction.response.send_message(f'Successfully created a new role - {new_role.mention}', ephemeral=True)

    @commands.group(invoke_without_command=True, aliases=["clear", "clean"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, limit: int):
        if limit > 250:
            raise commands.CommandError(
                "The maximum number of messages to delete is `250`")

        deleted = await ctx.channel.purge(limit=limit)
        await ctx.send(f'Deleted {len(deleted)} message(s)', delete_after=5.0)

    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def user(self, ctx: commands.Context, member: nextcord.Member, limit: int):
        if limit > 100:
            raise commands.CommandError(
                "The maximum number of messages to delete is `100`")

        messages = []

        minimum_time = int((time.time() - 14 * 24 * 60 * 60)
                           * 1000.0 - 1420070400000) << 22

        async for message in ctx.channel.history(limit=250):
            if len(messages) >= limit:
                break
            if message.author == member:
                messages.append(message)

            if message.id < minimum_time:
                break

        await ctx.channel.delete_messages(messages)

        await ctx.send(f'Deleted {len(messages)} message(s)', delete_after=5.0)

    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def between(self, ctx: commands.Context,
                      message_start: nextcord.Message,
                      messsage_finish: nextcord.Message):
        if message_start.channel != messsage_finish.channel:
            raise commands.CommandError("Channel error")

        messages = []
        finder = False
        minimum_time = int((time.time() - 14 * 24 * 60 * 60)
                           * 1000.0 - 1420070400000) << 22

        async for message in message_start.channel.history(limit=100):
            if message == messsage_finish:
                finder = True

            if finder:
                messages.append(message)

            if message == message_start or len(messages) >= 50 or message.id < minimum_time:
                break

        await ctx.channel.delete_messages(messages)

        await ctx.send(f'Deleted {len(messages)} message(s)', delete_after=5.0)

    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def until(self, ctx: commands.Context,
                    message_start: nextcord.Message):
        messages = []
        finder = False
        messsage_finish = None
        minimum_time = int((time.time() - 14 * 24 * 60 * 60)
                           * 1000.0 - 1420070400000) << 22

        async for message in message_start.channel.history(limit=250):
            if not messsage_finish:
                messsage_finish = message

            if message == messsage_finish:
                finder = True

            if finder:
                messages.append(message)

            if message == message_start or message.id < minimum_time:
                break

        await ctx.channel.delete_messages(messages)

        await ctx.send(f'Deleted {len(messages)} message(s)', delete_after=5.0)


def setup(bot):
    bot.add_cog(Moderations(bot))
