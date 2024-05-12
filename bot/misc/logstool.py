import asyncio
from dataclasses import dataclass
import datetime
from enum import IntEnum
import functools
from typing import Dict, List, Optional, Self, Tuple
import nextcord

from bot.databases.handlers.guildHD import GuildDateBases
from bot.misc.time_transformer import display_time
from bot.misc.utils import cut_back


@dataclass
class Message:
    content: Optional[str] = None
    embed: Optional[nextcord.Embed] = None
    files: Optional[List[nextcord.File]] = None


class LogType(IntEnum):
    delete_message = 0
    edit_message = 1
    punishment = 2
    economy = 3
    ideas = 4


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


async def pre_message_delete_log(message: nextcord.Message, moderator: Optional[nextcord.Member] = None):
    if message.id in _message_log:
        return
    loop = asyncio.get_event_loop()
    future = loop.create_future()
    _message_log[(message.channel.id, message.author.id)] = future
    try:
        await asyncio.wait_for(future, timeout=1)
    except asyncio.TimeoutError:
        pass
    else:
        moderator = future.result()
    await Logs(message.guild).delete_message(message, moderator)


async def set_message_delete_audit_log(moderator: nextcord.Member, channel_id: int, author_id: int):
    try:
        _message_log[(channel_id, author_id)].set_result(moderator)
    except KeyError:
        pass


class Logs:
    def __init__(self, guild: nextcord.Guild):
        self.guild = guild
        self.gdb = GuildDateBases(guild.id)
        self.guild_data: Dict[int, List[LogType]] = self.gdb.get('logs')

    @staticmethod
    def on_logs(log_type: int):
        def predicte(coro):
            @functools.wraps(coro)
            async def wrapped(self: Self, *args, **kwargs) -> None:
                for channel_id, logs_types in self.guild_data.items():
                    if log_type not in logs_types:
                        continue

                    channel = self.guild.get_channel(channel_id)
                    mes: Message = await coro(self, *args, **kwargs)
                    if mes is None:
                        return
                    await channel.send(content=mes.content, embed=mes.embed, files=mes.files)

            return wrapped
        return predicte

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
                value=message.content
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
            value=before.content
        )
        embed.add_field(
            name="After",
            value=after.content
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
        economy_settings = gdb.get('economic_settings')
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
    async def remove_currency(self, member: nextcord.Member, amount: int, moderator: Optional[nextcord.Member] = None, reason: Optional[str] = None):
        gdb = GuildDateBases(member.guild.id)
        economy_settings = gdb.get('economic_settings')
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
