import time
from typing import Optional
import nextcord
import jmespath
from nextcord.ext import commands
from bot.databases import GuildDateBases
from bot.databases.varstructs import IdeasPayload
from bot.misc.lordbot import LordBot
from bot.misc.time_transformer import display_time
from bot.misc.utils import TimeCalculator


class ideas_mod(commands.Cog):
    def __init__(self, bot: LordBot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def ideas(self, ctx: commands.Context) -> None:
        pass

    @staticmethod
    def get_ban(ideas: IdeasPayload, member_id: int) -> list | None:
        ban_users = ideas.get('ban_users', [])
        data_ban = jmespath.search(
            f"[?@[0]==`{member_id}`]|[0]", ban_users)
        return data_ban

    @staticmethod
    def get_mute(ideas: IdeasPayload, member_id: int) -> list | None:
        muted_users = ideas.get('muted_users', [])
        data_mute = jmespath.search(
            f"[?@[0]==`{member_id}`]|[0]", muted_users)
        return data_mute

    @ideas.command()
    async def ban(self, ctx: commands.Context, member: nextcord.Member, *, reason: Optional[str] = None) -> None:
        gdb = GuildDateBases(ctx.guild.id)
        color = await gdb.get('color')
        ideas: IdeasPayload = await gdb.get('ideas')
        ban_users = ideas.get('ban_users', [])

        if data_ban := self.get_ban(ideas, member.id):
            moderator = ctx.guild.get_member(data_ban[1])
            embed = nextcord.Embed(
                title="Ban in ideas",
                description=(
                    f"The {member.mention}({member.id}) user is already banned\n"
                    f"The moderator who issued the ban: {moderator.mention}({moderator.id})\n"
                    f"{f'Reason: `{data_ban[2]}`' if data_ban[2] else ''}"
                ),
                color=color
            )
            await ctx.send(embed=embed)
            return

        ban_users.append([member.id, ctx.author.id, reason])
        ideas['ban_users'] = ban_users
        await gdb.set('ideas', ideas)

        embed = nextcord.Embed(
            title="Ban in ideas",
            description=(
                f"The blocked user: {member.mention}({member.id})\n"
                f"The moderator who issued the ban: {ctx.author.mention}({ctx.author.id})\n"
                f"{f'Reason: `{reason}`' if reason else ''}"
            ),
            color=color
        )
        await ctx.send(embed=embed)

    @ideas.command()
    async def unban(self, ctx: commands.Context, member: nextcord.Member, *, reason: Optional[str] = None) -> None:
        gdb = GuildDateBases(ctx.guild.id)
        color = await gdb.get('color')
        ideas: IdeasPayload = await gdb.get('ideas')
        ban_users = ideas.get('ban_users', [])
        data_ban = self.get_ban(ideas, member.id)

        if not data_ban:
            embed = nextcord.Embed(
                title="Unban in ideas",
                description=f"The {member.mention} user is not blocked!",
                color=color
            )
            await ctx.send(embed=embed)
            return

        ban_users.remove(data_ban)
        ideas['ban_users'] = ban_users
        await gdb.set('ideas', ideas)

        embed = nextcord.Embed(
            title="Unban in ideas",
            description=(
                f"An unblocked user: {member.mention}({member.id})\n"
                f"The moderator who issued the unban: {ctx.author.mention}({ctx.author.id})\n"
                f"{f'Reason: `{reason}`' if reason else ''}"
            ),
            color=color
        )
        await ctx.send(embed=embed)

    @ideas.command()
    async def mute(self, ctx: commands.Context, member: nextcord.Member, timestamp: TimeCalculator, *, reason: Optional[str] = None) -> None:
        gdb = GuildDateBases(ctx.guild.id)
        color = await gdb.get('color')
        ideas: IdeasPayload = await gdb.get('ideas')
        muted_users = ideas.get('muted_users', [])

        if data_mute := self.get_mute(ideas, member.id):
            moderator = ctx.guild.get_member(data_mute[1])
            embed = nextcord.Embed(
                title="Mute in ideas",
                description=(
                    f"The {member.mention}({member.id}) user is already banned\n"
                    f"The moderator who issued the ban: {moderator.mention}({moderator.id})\n"
                    f"Time of action: <t:{data_mute[2] :.0f}:f>({display_time(data_mute[2]-time.time())})\n"
                    f"{f'Reason: `{data_mute[2]}`' if data_mute[3] else ''}"
                ),
                color=color
            )
            await ctx.send(embed=embed)
            return

        muted_users.append(
            [member.id, ctx.author.id, timestamp + time.time(), reason])
        ideas['muted_users'] = muted_users
        await gdb.set('ideas', ideas)

        embed = nextcord.Embed(
            title="Mute in ideas",
            description=(
                f"The muted user: {member.mention}({member.id})\n"
                f"The moderator who issued the mute: {ctx.author.mention}({ctx.author.id})\n"
                f"Time of action: <t:{timestamp + time.time() :.0f}:f>({display_time(timestamp)})\n"
                f"{f'Reason: `{reason}`' if reason else ''}"
            ),
            color=color
        )
        await ctx.send(embed=embed)

    @ideas.command()
    async def unmute(self, ctx: commands.Context, member: nextcord.Member, *, reason: Optional[str] = None) -> None:
        gdb = GuildDateBases(ctx.guild.id)
        color = await gdb.get('color')
        ideas: IdeasPayload = await gdb.get('ideas')
        muted_users = ideas.get('muted_users', [])
        data_mute = self.get_mute(ideas, member.id)

        if not data_mute:
            embed = nextcord.Embed(
                title="Unmute in ideas",
                description=f"The {member.mention} user is not muted!",
                color=color
            )
            await ctx.send(embed=embed)
            return

        muted_users.remove(data_mute)
        ideas['muted_users'] = muted_users
        await gdb.set('ideas', ideas)

        embed = nextcord.Embed(
            title="Unmute in ideas",
            description=(
                f"An unmuted user: {member.mention}({member.id})\n"
                f"The moderator who issued the unmmute: {ctx.author.mention}({ctx.author.id})\n"
                f"{f'Reason: `{reason}`' if reason else ''}"
            ),
            color=color
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ideas_mod(bot))
