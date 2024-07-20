
import asyncio
import nextcord
from nextcord.ext import commands, application_checks

from bot.languages import i18n
from bot.misc import utils
from bot.misc.utils import TimeCalculator
from bot.misc.lordbot import LordBot
from bot.misc.time_transformer import display_time
from bot.views.settings_menu import SettingsView
from bot.views.delcat import DelCatView
from bot.databases import RoleDateBases, BanDateBases, GuildDateBases

import time
from typing import List, Optional


timenow = None
timestamp = None


async def _single_delete(messages: List[nextcord.Message]):
    return
    for msg in messages:
        await msg.delete()


class Moderations(commands.Cog):
    def __init__(self, bot: LordBot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(send_messages=True)
    async def say(self, ctx: commands.Context, *, message: str):
        files = await asyncio.gather(*[attach.to_file(spoiler=attach.is_spoiler())
                                       for attach in ctx.message.attachments])

        res = await utils.generate_message(message)

        await ctx.send(**res, files=files)

        await ctx.message.delete()

    @commands.command(aliases=["set", "setting"])
    @commands.has_permissions(manage_guild=True)
    async def settings(self, ctx: commands.Context):
        view = await SettingsView(ctx.author)

        await ctx.send(embed=view.embed, view=view)

    @nextcord.slash_command(name="delete-category", default_member_permissions=48)
    @application_checks.has_permissions(manage_channels=True)
    async def deletecategory(self, interaction: nextcord.Interaction, category: nextcord.CategoryChannel):
        view = await DelCatView(interaction.user, category)

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
        locale = await gdb.get('language')
        color = await gdb.get('color')

        self.bot.lord_handler_timer.close(
            f"ban:{ctx.guild.id}:{member.id}")

        embed = nextcord.Embed(
            title=i18n.t(locale, 'tempban.title'),
            description=i18n.t(locale, 'tempban.description', member=member.name, member_id=member.id, author=ctx.author, author_id=ctx.author.id),
            color=color
        )
        if ftime is not None:
            embed.add_field(
                name=i18n.t(locale, 'tempban.description.field.time'),
                value=f"<t:{ftime+time.time() :.0f}:f> ({display_time(ftime, locale)})",
                inline=False
            )
        if reason is not None:
            embed.add_field(
                name=i18n.t(locale, 'tempban.description.field.reason'),
                value=reason,
                inline=False
            )
        if ftime is not None:
            self.bot.lord_handler_timer.create(
                ftime, bsdb.remove_ban(ctx.guild._state), f"ban:{ctx.guild.id}:{member.id}")

            bsdb.insert(ftime+time.time())

        await member.ban(reason=reason)

        await ctx.send(embed=embed)

    @temp_ban.command(name='list')
    async def temp_ban_list(self, ctx: commands.Context):
        gdb = GuildDateBases(ctx.guild.id)
        color = await gdb.get('color')
        locale = await gdb.get('language')

        rsdb = BanDateBases(ctx.guild.id)
        datas = await rsdb.get_as_guild()

        message = ""

        for quantity, (member_id, ban_time) in enumerate(datas):
            message += f"{quantity}. <@{member_id}> (<t:{ban_time}:R>)\n"

        message = message or i18n.t(locale, 'tempban.list.nf')
        embed = nextcord.Embed(
            title=i18n.t(locale, 'tempban.list.title'),
            description=message,
            color=color
        )

        await ctx.send(embed=embed)

    @commands.group(name='temp-role', aliases=['temprole'], invoke_without_command=True)
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
        locale = await gdb.get('language')
        color = await gdb.get('color')
        _role_time = await rsdb.get_as_role(role.id)

        if _role_time is not None:
            self.bot.lord_handler_timer.close(
                f"role:{ctx.guild.id}:{member.id}:{role.id}")
            embed = nextcord.Embed(
                title=i18n.t(locale, 'temprole.change.title'),
                color=color)
            embed.add_field(
                name=i18n.t(locale, 'temprole.change.role'),
                value=f'{member.mention} → {role.mention} (ROLE ID: {role.id})',
                inline=False
            )
            embed.add_field(
                name=i18n.t(locale, 'temprole.global.action'),
                value=f'<t:{_role_time[0]}:f> → <t:{ftime+time.time() :.0f}:f> ({display_time(ftime, locale)})',
                inline=False
            )
        else:
            embed = nextcord.Embed(
                title=i18n.t(locale, 'temprole.created.title'),
                color=color)
            embed.add_field(
                name="Role",
                value=f'{member.mention} → {role.mention} (ROLE ID: {role.id})',
                inline=False
            )
            embed.add_field(
                name=i18n.t(locale, 'temprole.global.action'),
                value=f"<t:{ftime+time.time() :.0f}:f> ({display_time(ftime)})",
                inline=False
            )

        await rsdb.set_role(role.id, ftime+time.time())

        self.bot.lord_handler_timer.create(
            ftime, rsdb.remove_role(member, role), f"role:{ctx.guild.id}:{member.id}:{role.id}")

        await member.add_roles(role)

        await ctx.send(embed=embed)

    @temp_role.command(name='list')
    async def temp_role_list(self, ctx: commands.Context, member: Optional[nextcord.Member] = None):
        gdb = GuildDateBases(ctx.guild.id)
        color = await gdb.get('color')
        locale = await gdb.get('language')

        if member is not None:
            rsdb = RoleDateBases(ctx.guild.id, member.id)
            datas = await rsdb.get_as_member()
        else:
            rsdb = RoleDateBases(ctx.guild.id)
            datas = await rsdb.get_as_guild()

        message = ""

        for quantity, (member_id, role_id, role_time) in enumerate(datas):
            member = ctx.guild.get_member(member_id)
            role = ctx.guild.get_role(role_id)

            if not (role and member):
                continue

            message += f"{quantity}. {member.mention} → {role.mention} (<t:{role_time}:R>)\n"

        message = message or i18n.t(locale, 'temprole.list.nf')
        embed = nextcord.Embed(
            title=i18n.t(locale, 'temprole.list.title'),
            description=message,
            color=color
        )

        await ctx.send(embed=embed)

    @nextcord.slash_command(
        name='clone',
        default_member_permissions=268435456
    )
    async def cmd_clone(
        self,
        interaction: nextcord.Interaction
    ) -> None:
        pass

    @cmd_clone.subcommand(
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
        gdb = GuildDateBases(interaction.guild_id)
        locale = await gdb.get('language')

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

        await interaction.response.send_message(i18n.t(locale, 'clone-role.success', role=new_role.mention), ephemeral=True)

    @commands.group(invoke_without_command=True, aliases=["clear", "clean"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, limit: int):
        gdb = GuildDateBases(ctx.guild.id)
        locale = await gdb.get('language')
        if limit > 250:
            await ctx.send(i18n.t(locale, 'purge.error.limit'))
            return

        iterator = ctx.channel.history(limit=limit)
        deleted = []
        count = 0
        strategy = ctx.channel.delete_messages
        minimum_time = int((time.time() - 14 * 24 * 60 * 60) * 1000.0 - 1420070400000) << 22
        ctx.channel.purge
        async for message in iterator:
            if count == 100:
                to_delete = deleted[-100:]
                await strategy(to_delete)
                count = 0
                await asyncio.sleep(1)

            if message.id < minimum_time:
                to_delete = deleted[-count:]
                await strategy(to_delete)
                count = 0
                strategy = _single_delete

            count += 1
            deleted.append(message)

        to_delete = deleted[-count:]
        await strategy(to_delete)

        await ctx.send(i18n.t(locale, 'purge.success', lenght=len(deleted)), delete_after=5.0)

    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def user(self, ctx: commands.Context, member: nextcord.Member, limit: int):
        gdb = GuildDateBases(ctx.guild.id)
        locale = await gdb.get('language')
        if limit > 250:
            await ctx.send(i18n.t(locale, 'purge.error.limit'))
            return

        iterator = ctx.channel.history(limit=1000)
        count = 0
        deleted = []
        strategy = ctx.channel.delete_messages
        minimum_time = int((time.time() - 14 * 24 * 60 * 60)
                           * 1000.0 - 1420070400000) << 22

        async for message in iterator:
            if len(deleted) >= limit:
                break
            if count == 100:
                to_delete = deleted[-100:]
                await strategy(to_delete)
                count = 0
                await asyncio.sleep(1)
            if message.id < minimum_time:
                to_delete = deleted[-count:]
                await strategy(to_delete)
                count = 0
                strategy = _single_delete
            if message.author == member:
                count += 1
                deleted.append(message)

        to_delete = deleted[-count:]
        await strategy(to_delete)

        await ctx.send(i18n.t(locale, 'purge.success', lenght=len(deleted)), delete_after=5.0)

    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def between(self, ctx: commands.Context,
                      message_start: nextcord.Message,
                      message_finish: nextcord.Message):
        gdb = GuildDateBases(ctx.guild.id)
        locale = await gdb.get('language')
        if message_start.channel != message_finish.channel:
            await ctx.send(i18n.t(locale, 'purge.error.channel'))
            return

        iterator = message_start.channel.history(limit=1000)
        count = 0
        deleted = []
        strategy = message_start.channel.delete_messages
        minimum_time = int((time.time() - 14 * 24 * 60 * 60)
                           * 1000.0 - 1420070400000) << 22

        async for message in iterator:
            if count == 100:
                to_delete = deleted[-100:]
                await strategy(to_delete)
                count = 0
                await asyncio.sleep(1)
            if message.id < minimum_time:
                to_delete = deleted[-count:]
                await strategy(to_delete)
                count = 0
                strategy = _single_delete
            if message_finish.created_at > message.created_at:
                count += 1
                deleted.append(message)
            if message_start.created_at >= message.created_at or len(deleted) >= 250:
                break

        to_delete = deleted[-count:]
        await strategy(to_delete)

        await ctx.send(i18n.t(locale, 'purge.success', lenght=len(deleted)), delete_after=5.0)

    @purge.command()
    @commands.has_permissions(manage_messages=True)
    async def until(self, ctx: commands.Context,
                    message_start: nextcord.Message):
        gdb = GuildDateBases(ctx.guild.id)
        locale = await gdb.get('language')

        iterator = message_start.channel.history(limit=1000)
        count = 0
        deleted = []
        strategy = message_start.channel.delete_messages
        minimum_time = int((time.time() - 14 * 24 * 60 * 60)
                           * 1000.0 - 1420070400000) << 22

        async for message in iterator:
            if count == 100:
                to_delete = deleted[-100:]
                await strategy(to_delete)
                count = 0
                await asyncio.sleep(1)
            if message.id < minimum_time:
                to_delete = deleted[-count:]
                await strategy(to_delete)
                count = 0
                strategy = _single_delete

            count += 1
            deleted.append(message)

            if message_start.created_at >= message.created_at or len(deleted) >= 250:
                break

        to_delete = deleted[-count:]
        await strategy(to_delete)

        await ctx.send(i18n.t(locale, 'purge.success', lenght=len(deleted)), delete_after=5.0)


def setup(bot):
    bot.add_cog(Moderations(bot))
