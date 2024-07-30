from __future__ import annotations

import asyncio
from dataclasses import dataclass
import datetime
from enum import IntEnum
import functools
import logging
from typing import Dict, List, Optional,  Tuple
import nextcord

from bot.databases import GuildDateBases
from bot.misc.time_transformer import display_time
from bot.misc.utils import cut_back

_log = logging.getLogger(__name__)


@dataclass
class Message:
    content: Optional[str] = None
    embed: Optional[nextcord.Embed] = None
    embeds: Optional[List[nextcord.Embed]] = None
    file: Optional[nextcord.File] = None
    files: Optional[List[nextcord.File]] = None


class LogType(IntEnum):
    # TODO: Create logs: voice state, tickets and tempvoice
    delete_message = 0
    edit_message = 1
    punishment = 2
    economy = 3
    ideas = 4
    voice_state = 5
    ticket = 6
    tempvoice = 7


def embed_to_text(embed: nextcord.Embed) -> str:
    return '\n'.join([
        cut_back(embed.title, 200),
        cut_back(embed.author.name, 100),
        cut_back(embed.description, 1000),
        cut_back(embed.footer.text, 200)
    ])


def filter_bool(texts: list) -> list:
    return list(filter(
        lambda item: item,
        texts
    ))


_message_log: Dict[Tuple[int, int], asyncio.Future] = {}


async def pre_message_delete_log(message: nextcord.Message):
    moderator: Optional[nextcord.Member] = None
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    _message_log[(message.channel.id, message.author.id)] = future

    try:
        await asyncio.wait_for(future, timeout=1)
    except asyncio.TimeoutError:
        pass
    else:
        moderator = future.result()
    finally:
        _message_log.pop((message.channel.id, message.author.id), None)

    await Logs(message.guild).delete_message(message, moderator)


async def set_message_delete_audit_log(moderator: nextcord.Member, channel_id: int, author_id: int) -> None:
    try:
        _message_log[(channel_id, author_id)].set_result(moderator)
    except KeyError:
        pass


def on_logs(log_type: int):
    def predicte(coro):
        @functools.wraps(coro)
        async def wrapped(self: Logs, *args, **kwargs) -> None:
            if self.guild is None or self.gdb is None:
                return

            mes: Optional[Message] = await coro(self, *args, **kwargs)
            guild_data: Dict[int, List[LogType]] = await self.gdb.get('logs')

            if mes is None or guild_data is None:
                return

            for channel_id, logs_types in guild_data.items():
                if log_type not in logs_types:
                    continue

                channel = self.guild.get_channel(channel_id)
                if not channel:
                    continue

                bot = self.guild.me
                perms = channel.permissions_for(bot)
                if not (perms.send_messages and perms.embed_links and perms.read_messages):
                    continue

                await channel.send(
                    content=mes.content,
                    embed=mes.embed,
                    embeds=mes.embeds,
                    file=mes.file,
                    files=mes.files
                )

        return wrapped
    return predicte


class Logs:
    def __init__(self, guild: Optional[nextcord.Guild]):
        if guild is not None:
            self.guild = guild
            self.gdb = GuildDateBases(guild.id)
        else:
            self.guild = None
            self.gdb = None

    @on_logs(LogType.delete_message)
    async def delete_message(self, message: nextcord.Message, moderator: Optional[nextcord.Member] = None):
        if message.author.bot:
            return

        embed = nextcord.Embed(
            title="Message deleted",
            color=nextcord.Colour.red(),
            description=(
                f"> Channel: {message.channel.name} ({message.channel.mention})\n"
                f"> Message id: {message.id}\n"
                f"> Message author: {str(message.author)} ({message.author.mention})\n"
                f"> Message created: <t:{message.created_at.timestamp() :.0f}:f> (<t:{message.created_at.timestamp() :.0f}:R>)"
            ),
            timestamp=datetime.datetime.today()
        )
        if message.content:
            embed.add_field(
                name="Message",
                value=message.content[:1024]
            )
        if moderator:
            embed.set_footer(text=moderator,
                             icon_url=moderator.display_avatar)
        if message.attachments:
            files = await asyncio.gather(*[
                attach.to_file()
                for attach in message.attachments
            ])
        else:
            files = None
        return Message(embed=embed, files=files)

    @on_logs(LogType.edit_message)
    async def edit_message(self, before: nextcord.Message, after: nextcord.Message):
        if after.author.bot:
            return

        if before.content == after.content:
            editted = {}
            for slot in nextcord.Message.__slots__:
                if getattr(before, slot, None) != getattr(after, slot, None):
                    editted[slot] = (getattr(before, slot, None),
                                     getattr(after, slot, None))
            _log.trace('[%d] Eddited data: %s', after.id, editted)

            if len(before.attachments) > 0 and len(after.attachments) == 0:
                embed = nextcord.Embed(
                    title="Message edited",
                    color=nextcord.Colour.orange(),
                    description=(
                        f"> Channel: {before.channel.name} ({before.channel.mention})\n"
                        f"> Message id: {before.id}\n"
                        f"> Message author: {str(before.author)} ({before.author.mention})\n"
                        f"> Message created: <t:{before.created_at.timestamp() :.0f}:f> (<t:{before.created_at.timestamp() :.0f}:R>)"
                    ),
                    timestamp=datetime.datetime.today()
                )
                embed.add_field(
                    name='Action',
                    value='Remove all attachments'
                )
                return Message(embed=embed)
            return

        embed = nextcord.Embed(
            title="Message edited",
            color=nextcord.Colour.orange(),
            description=(
                f"> Channel: {before.channel.name} ({before.channel.mention})\n"
                f"> Message id: {before.id}\n"
                f"> Message author: {str(before.author)} ({before.author.mention})\n"
                f"> Message created: <t:{before.created_at.timestamp() :.0f}:f> (<t:{before.created_at.timestamp() :.0f}:R>)"
            ),
            timestamp=datetime.datetime.today()
        )
        embed.add_field(
            name="Before",
            value=before.content[:1024]
        )
        embed.add_field(
            name="After",
            value=after.content[:1024]
        )
        return Message(embed=embed)

    @on_logs(LogType.punishment)
    async def timeout(
            self,
            member: nextcord.Member,
            duration: int,
            moderator: nextcord.Member,
            reason: Optional[str] = None):
        embed = nextcord.Embed(
            title='Timeout',
            color=nextcord.Colour.red(),
            description=(
                f'Member: {member} ({member.id})\n'
                f'Disabled on: {display_time(duration)}\n'
                f'Moderator: {moderator} ({moderator.id})\n'
                f"{f'Reason: {reason}' if reason else ''}"
            )
        )
        embed.set_thumbnail(member.display_avatar)
        return Message(embed=embed)

    @on_logs(LogType.punishment)
    async def untimeout(self,
                        member: nextcord.Member,
                        duration: Optional[int] = None,
                        moderator: Optional[nextcord.Member] = None,
                        reason: Optional[str] = None):
        embed = nextcord.Embed(
            title='Untimeout',
            color=nextcord.Colour.red(),
            description=f"Member: {member} ({member.id})"
        )
        if duration:
            embed.description += f'\nSpent in the mute: {display_time(duration)}'
        if moderator:
            embed.description += f'\nModerator: {moderator} ({moderator.id})'
        if reason:
            embed.description += f'\nReason: {reason}'
        embed.set_thumbnail(member.display_avatar)
        return Message(embed=embed)

    @on_logs(LogType.punishment)
    async def kick(self, guild: nextcord.Guild, user: nextcord.User,
                   moderator: nextcord.Member, reason: Optional[str]):
        embed = nextcord.Embed(
            title='Kick',
            color=nextcord.Colour.red(),
            description=(
                f'Member: {user} ({user.id})\n'
                f'Moderator: {moderator} ({moderator.id})\n'
                f"{f'Reason: {reason}' if reason else ''}"
            )
        )
        embed.set_thumbnail(user.display_avatar)
        return Message(embed=embed)

    @on_logs(LogType.punishment)
    async def ban(self, guild: nextcord.Guild, user: nextcord.User,
                  moderator: nextcord.Member, reason: Optional[str]):
        embed = nextcord.Embed(
            title='Ban',
            color=nextcord.Colour.red(),
            description=(
                f'Member: {user} ({user.id})\n'
                f'Moderator: {moderator} ({moderator.id})\n'
                f"{f'Reason: {reason}' if reason else ''}"
            )
        )
        embed.set_thumbnail(user.display_avatar)
        return Message(embed=embed)

    @on_logs(LogType.punishment)
    async def unban(self, guild: nextcord.Guild, user: nextcord.User,
                    moderator: nextcord.Member, reason: Optional[str]):
        embed = nextcord.Embed(
            title='Unbam',
            color=nextcord.Colour.red(),
            description=(
                f'Member: {user} ({user.id})\n'
                f'Moderator: {moderator} ({moderator.id})\n'
                f"{f'Reason: {reason}' if reason else ''}"
            )
        )
        embed.set_thumbnail(user.display_avatar)
        return Message(embed=embed)

    @on_logs(LogType.economy)
    async def add_currency(self, member: nextcord.Member, amount: int, moderator: Optional[nextcord.Member] = None, reason: Optional[str] = None):
        gdb = GuildDateBases(member.guild.id)
        economy_settings = await gdb.get('economic_settings')
        currency_emoji = economy_settings.get('emoji')
        embed = nextcord.Embed(
            title='Currency received',
            color=nextcord.Colour.brand_green(),
            description=(
                f'Member: {member} ({member.id})\n'
                f'Amount: {amount :,}{currency_emoji}'
            )
        )
        if moderator:
            embed.description += f'\nModerator: {moderator} ({moderator.id})'
        if reason:
            embed.description += f'\nReason: {reason}'
        embed.set_thumbnail(member.display_avatar)
        return Message(embed=embed)

    @on_logs(LogType.economy)
    async def add_currency_for_ids(self, role: nextcord.Role, amount: int, moderator: Optional[nextcord.Member] = None, reason: Optional[str] = None):
        gdb = GuildDateBases(role.guild.id)
        economy_settings = await gdb.get('economic_settings')
        currency_emoji = economy_settings.get('emoji')
        embed = nextcord.Embed(
            title='Currency received',
            color=nextcord.Colour.brand_green(),
            description=(
                f'Role: {role.mention} ({role.id})\n'
                f'Amount: {amount :,}{currency_emoji}'
            )
        )
        if moderator:
            embed.description += f'\nModerator: {moderator} ({moderator.id})'
        if reason:
            embed.description += f'\nReason: {reason}'
        embed.set_thumbnail(role.icon)
        return Message(embed=embed)

    @on_logs(LogType.economy)
    async def remove_currency(self, member: nextcord.Member, amount: int, moderator: Optional[nextcord.Member] = None, reason: Optional[str] = None):
        gdb = GuildDateBases(member.guild.id)
        economy_settings = await gdb.get('economic_settings')
        currency_emoji = economy_settings.get('emoji')
        embed = nextcord.Embed(
            title='Currency was taken',
            color=nextcord.Colour.red(),
            description=(
                f'Member: {member} ({member.id})\n'
                f'Amount: {amount :,}{currency_emoji}'
            )
        )
        if moderator:
            embed.description += f'\nModerator: {moderator} ({moderator.id})'
        if reason:
            embed.description += f'\nReason: {reason}'
        embed.set_thumbnail(member.display_avatar)
        return Message(embed=embed)

    @on_logs(LogType.ideas)
    async def create_idea(self, member: nextcord.Member, idea: str, image: Optional[str] = None):
        embed = nextcord.Embed(
            title='Created new idea',
            description=(
                f'Member: {member} ({member.id})\n'
                f'Idea: {idea}'
            ),
            color=nextcord.Colour.orange()
        )
        embed.set_thumbnail(member.display_avatar)
        embed.set_image(image)
        return Message(embed=embed)

    @on_logs(LogType.ideas)
    async def approve_idea(self, moderator: nextcord.Member, member: nextcord.Member, idea: str, reason: Optional[str] = None, image: Optional[str] = None):
        embed = nextcord.Embed(
            title='Approved idea',
            description='\n'.join(filter_bool([
                f'Member: {member} ({member.id})',
                f'Moderator: {moderator} ({moderator.id})',
                'Reason: '+reason if reason else '',
                f'Idea: {idea}'
            ])),
            color=nextcord.Colour.brand_green()
        )
        embed.set_thumbnail(member.display_avatar)
        if image:
            embed.set_image(image)
        embed.set_footer(text=str(moderator),
                         icon_url=moderator.display_avatar)
        return Message(embed=embed)

    @on_logs(LogType.ideas)
    async def deny_idea(self, moderator: nextcord.Member, member: nextcord.Member, idea: str, image: Optional[str] = None):
        embed = nextcord.Embed(
            title='Denied idea',
            description=(
                f'Member: {member} ({member.id})\n'
                f'Moderator: {moderator} ({moderator.id})'
                f'Idea: {idea}'
            ),
            color=nextcord.Colour.red()
        )
        embed.set_thumbnail(member.display_avatar)
        if image:
            embed.set_image(image)
        embed.set_footer(text=str(moderator),
                         icon_url=moderator.display_avatar)
        return Message(embed=embed)

    @on_logs
    async def add_role(self, member: nextcord.Member, role: nextcord.Role): ...

    @on_logs
    async def remove_role(self, member: nextcord.Member,
                          role: nextcord.Role): ...

    @on_logs
    async def change_role(self, *args): ...

    @on_logs
    async def delete_role(self, role: nextcord.Role): ...

    @on_logs
    async def add_channel(
        self, channel: nextcord.abc.GuildChannel): ...

    @on_logs
    async def change_channel(
        self, channel: nextcord.abc.GuildChannel): ...

    @on_logs
    async def delete_channel(
        self, channel: nextcord.abc.GuildChannel): ...

    @on_logs
    async def change_bot_settings(
        self, user: nextcord.User, *args): ...
