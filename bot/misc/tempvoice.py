import contextlib
from enum import IntEnum
import logging
import time
import nextcord

from bot.cogs.events import voice_state
from bot.databases import localdb
from bot.databases.handlers.guildHD import GuildDateBases
from bot.databases.varstructs import TempChannelsItemPayload, TempChannelsPayload
from bot.misc.utils import GuildPayload, MemberPayload, lord_format


_log = logging.getLogger(__name__)

TIMEOUT_VOICE = 300


def get_payload(member: nextcord.Member, count: int):
    payload = {'voice.count': count}
    payload.update(MemberPayload(member)._to_dict())
    payload.update(GuildPayload(member.guild)._to_dict())
    return payload


class VoiceStatus(IntEnum):
    opened = 1
    closed = 2


class TempVoiceModule:
    async def process(self, member: nextcord.Member, before: nextcord.VoiceChannel, after: nextcord.VoiceChannel) -> None:
        gdb = GuildDateBases(member.guild.id)
        data = await gdb.get('tempvoice')
        channels_data = await localdb.get_table('channels_data')
        self.member = member

        if not (data and data.get('enabled')):
            return
        if after and after.id == data['channel_id']:
            await self.create(after)
        if before and await channels_data.exists(before.id):
            await self.delete(before)

    async def check_user(self, channel: nextcord.VoiceChannel):
        channels_tracks_db = await localdb.get_table('channels_track_data')
        channels_data = await localdb.get_table('channels_data')
        channels_track_data = await channels_tracks_db.get(self.member.guild.id, [])

        for cid in channels_track_data:
            voice_data = await channels_data.get(cid)
            owner_id = voice_data['owner_id']

            if self.member.id != owner_id:
                continue

            if voice_data['status'] == VoiceStatus.closed:
                limited_time = voice_data['closed_time']+TIMEOUT_VOICE
                if limited_time > time.time():
                    with contextlib.suppress(nextcord.Forbidden):
                        await channel.send(f'{self.member.mention} You will be able to create a new temporary room only after <t:{limited_time:.0f}:R>')
                    await self.member.disconnect()
                    return False
            if voice_data['status'] == VoiceStatus.opened:
                channel = self.member.guild.get_channel(
                    voice_data['channel_id'])
                await self.member.move_to(channel)
                return False
        return True

    async def get_activity_count(self):
        channels_tracks_db = await localdb.get_table('channels_track_data')
        channels_data = await localdb.get_table('channels_data')
        channels_track_data = await channels_tracks_db.get(self.member.guild.id, [])

        count = 1
        for cid in channels_track_data:
            voice_data = await channels_data.get(cid)
            if voice_data['status'] == VoiceStatus.opened:
                count += 1
        return count

    async def create(self, channel: nextcord.VoiceChannel):
        if not await self.check_user(channel):
            return

        gdb = GuildDateBases(self.member.guild.id)
        data = await gdb.get('tempvoice')
        channels_tracks_db = await localdb.get_table('channels_track_data')
        channels_data = await localdb.get_table('channels_data')
        channels_track_data = await channels_tracks_db.get(self.member.guild.id, [])

        name = lord_format(data['channel_name'], get_payload(self.member, await self.get_activity_count()))
        category = self.member.guild.get_channel(data['category_id'])
        channel = await self.member.guild.create_voice_channel(
            name=name,
            category=category,
            user_limit=data.get('channel_limit', 4),
            overwrites={
                self.member: nextcord.PermissionOverwrite(
                    manage_channels=True,
                    manage_permissions=True,
                    create_instant_invite=True,
                    view_channel=True,
                    connect=True,
                    speak=True,
                    stream=True,
                    use_voice_activation=True,
                    priority_speaker=True
                ),
                self.member.guild.default_role: nextcord.PermissionOverwrite(
                    create_instant_invite=True,
                    view_channel=True,
                    connect=True,
                    speak=True,
                    stream=True,
                    use_voice_activation=True,
                    priority_speaker=True
                )
            })
        await self.member.move_to(channel)

        channels_track_data.append(channel.id)
        await channels_tracks_db.set(self.member.guild.id, channels_track_data)
        await channels_data.set(channel.id, {
            'owner_id': self.member.id,
            'channel_id': channel.id,
            'status': VoiceStatus.opened
        })

    async def delete(self, channel: nextcord.VoiceChannel):
        if len(channel.members) > 0:
            return

        channels_data = await localdb.get_table('channels_data')
        voice_data = await channels_data.get(channel.id)
        voice_data['status'] = VoiceStatus.closed
        voice_data['closed_time'] = time.time()
        await channels_data.set(channel.id, voice_data)

        await channel.delete()
