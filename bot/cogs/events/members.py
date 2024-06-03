import functools
import nextcord
from nextcord.ext import commands

from bot.misc import utils
from bot.databases import GuildDateBases

import asyncio
import jmespath
import time
from typing import Optional

from bot.misc.lordbot import LordBot


def disable(func):
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        return None
    return wrapped


class MembersEvent(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        gdb = GuildDateBases(member.guild.id)

        await asyncio.gather(
            self.process_invites(member, gdb),
            self.auto_roles(member, gdb),
            self.auto_message(member, gdb)
        )

    async def auto_roles(self, member: nextcord.Member, gdb: GuildDateBases):
        roles_ids = await gdb.get('auto_roles')

        if not roles_ids:
            return

        roles = filter(lambda item: item is not None,
                       map(member.guild.get_role, roles_ids))

        await member.add_roles(*roles, atomic=False)

    async def auto_message(self, member: nextcord.Member, gdb: GuildDateBases):
        guild = member.guild
        greeting_message: dict = await gdb.get('greeting_message', {})

        if not (channel := guild.get_channel(greeting_message.get("channel_id"))):
            return

        member_payload = utils.MemberPayload(member).to_dict()
        guild_payload = utils.GuildPayload(guild).to_dict()
        data_payload = guild_payload | member_payload

        content: str = greeting_message.get('message')

        message_format = utils.lord_format(content, data_payload)
        message_data = await utils.generate_message(message_format)

        if image_link := greeting_message.get('image'):
            image_bytes = await utils.generate_welcome_image(member, image_link)
            file = nextcord.File(image_bytes, "welcome-image.png")
            message_data["file"] = file

        await channel.send(**message_data)

    @disable
    async def process_invites(self, member: nextcord.Member, gdb: GuildDateBases) -> nextcord.Invite | None:
        old_invites = self.bot.invites_data.get(member.guild.id, [])
        new_invites = await member.guild.invites()
        self.bot.invites_data[member.guild.id] = new_invites

        invite = None

        for oinv in old_invites:
            for ninv in new_invites:
                if ninv.uses >= oinv.uses:
                    invite = ninv
                    break

        if invite is None:
            return

        invites = await gdb.get('invites', [])
        invites.append((member.id, invite.inviter.id,
                       time.time(), invite.code))
        await gdb.set('invites', invites)

        return invite

    @commands.command()
    @disable
    async def invites(self, ctx: commands.Context, member: Optional[nextcord.Member] = None):
        gdb = GuildDateBases(ctx.guild.id)
        color = gdb.get('color')
        invites = gdb.get('invites', [])

        if member is None:
            embed = nextcord.Embed(
                title="Invites",
                description="",
                color=color
            )
            for member_id, invitor_id, _, code in invites:
                member = ctx.guild.get_member(member_id)
                invitor = ctx.guild.get_member(invitor_id)

                embed.description += f"{invitor.mention if invitor else '**'+invitor_id+'**'} → {member.mention if member else '**'+member_id+'**'} | `{code}`"
        else:
            member_invites = jmespath.search(
                f"[?@[1]==`{member.id}`]", invites) or []
            embed = nextcord.Embed(
                title=f"Invites of {member.display_name}",
                description="",
                color=color
            )
            for member_id, _, add_at, code in member_invites:
                member = ctx.guild.get_member(member_id)

                embed.description += f"<t:{add_at :.0f}:f> | {member.mention if member else '**'+member_id+'**'} | `{code}`"

        if not embed.description:
            embed.description = "Information not found!"

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MembersEvent(bot))
