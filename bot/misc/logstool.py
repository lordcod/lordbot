import asyncio
from dataclasses import dataclass
import datetime
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


def embed_to_text(embed: nextcord.Embed) -> str:
    return '\n'.join([
        cut_back(embed.title, 200),
        cut_back(embed.author.name, 100),
        cut_back(embed.description, 1000),
        cut_back(embed.footer.text, 200)
    ])


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
        self.guild_data = {0: 1229044270996918272,
                           1: 1229044270996918272,
                           2: 1229044270996918272,
                           3: 1229044270996918272}

    @staticmethod
    def on_logs(log_type: int):
        def predicte(coro):
            @functools.wraps(coro,
                             assigned=("__module__", "__name__",
                                       "__qualname__", "__doc__"),
                             updated=("__dict__", "__annotations__"))
            async def wrapped(self: Self, *args, **kwargs) -> None:
                if log_type not in self.guild_data:
                    return
                channel_id = self.guild_data[log_type]
                channel = self.guild.get_channel(channel_id)
                mes: Message = await coro(self, *args, **kwargs)
                await channel.send(content=mes.content, embed=mes.embed, files=mes.files)

            return wrapped
        return predicte

    @on_logs(0)
    async def delete_message(self, message: nextcord.Message, moderator: Optional[nextcord.Member] = None):
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
        if message.embeds:
            for num, emb in enumerate(message.embeds):
                embed.add_field(
                    name=f"Embed #{num}",
                    value=embed_to_text(emb)
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

    @on_logs(100)
    async def edit_message(self, before: nextcord.Message, after: nextcord.Message):
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
        before_content = f'{before.content}\n' if before.content else ''
        if before.embeds:
            before_content += embed_to_text(before.embeds[0])
        after_content = f'{after.content}\n' if after.content else ''
        if after.embeds:
            after_content += embed_to_text(after.embeds[0])
        embed.add_field(
            name="Before",
            value=before_content
        )
        embed.add_field(
            name="After",
            value=after_content
        )
        return Message(embed=embed)

    @on_logs(2)
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

    @on_logs(2)
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

    @on_logs(2)
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

    @on_logs(2)
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

    @on_logs(2)
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

    @on_logs(3)
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

    @on_logs(3)
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

    @on_logs()
    async def create_idea():
        pass

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
