import nextcord
from nextcord.ext import commands

from bot.misc import utils
from bot.misc.logger import Logger
from bot.databases import GuildDateBases

import functools
from typing import Dict, List, Optional

from bot.misc.lordbot import LordBot


def on_error(func):
    @functools.wraps(func)
    async def wrapped(self, member, gdb):
        try:
            result = await func(self, member, gdb)
            return result
        except Exception as err:
            Logger.error(err)
    return wrapped


class members_event(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        gdb = GuildDateBases(member.guild.id)

        self.bot.loop.create_task(self.auto_roles(member, gdb))
        self.bot.loop.create_task(self.auto_message(member, gdb))
        self.bot.loop.create_task(self.process_invites(member, gdb))

    @on_error
    async def auto_roles(self, member: nextcord.Member, gdb: GuildDateBases):
        roles_ids = gdb.get('auto_roles')

        if not roles_ids:
            return

        roles = filter(lambda item: item is not None,
                       [member.guild.get_role(role_id) for role_id in roles_ids])

        await member.add_roles(*roles, atomic=False)

    @on_error
    async def auto_message(self, member: nextcord.Member, gdb: GuildDateBases):
        guild = member.guild
        greeting_message: dict = gdb.get('greeting_message', {})

        channel_id: int = greeting_message.get("channel_id")
        channel = guild.get_channel(channel_id)

        if not channel:
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

        invites = gdb.get('invites', [])
        invites.append((member.id, invite.inviter.id, invite.code))
        gdb.set('invites', invites)

    @commands.command()
    async def getinvite(self, ctx: commands.Context, member: Optional[nextcord.Member] = None):
        gdb = GuildDateBases(ctx.guild.id)
        invites = gdb.get('invites', [])

        if member is None:
            await ctx.send(invites)
            return

        meminvites = []

        for inv in invites:
            if inv[1] == member.id:
                meminvites.append(inv)

        await ctx.send(meminvites)


def setup(bot):
    bot.add_cog(members_event(bot))
