from typing import Optional
import nextcord
from nextcord.ext import commands

from bot.misc import utils
from bot.misc.logger import Logger
from bot.databases import GuildDateBases

import functools

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

        await self.auto_roles(member, gdb)
        await self.auto_message(member, gdb)

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

        await channel.send(**message_data)


def setup(bot):
    bot.add_cog(members_event(bot))
