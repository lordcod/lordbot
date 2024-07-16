import contextlib
from datetime import datetime
from enum import IntEnum
import logging
import time
from typing import Optional
import nextcord
from nextcord.utils import snowflake_time

from bot.databases import localdb
from bot.databases.handlers.guildHD import GuildDateBases
from bot.databases.varstructs import TempChannelsItemPayload, TempChannelsPayload
from bot.languages import i18n
from bot.misc.utils import GuildPayload, MemberPayload, get_emoji_wrap, lord_format
from bot.resources.info import DEFAULT_BOT_COLOR
from bot.resources.ether import temp_voice_emojis
from bot.views.tempvoice.view import TempVoiceView
from bot.views.tempvoice.dropdown import AdvancedTempVoiceView


_log = logging.getLogger(__name__)

TIMEOUT_VOICE = 5


class VoiceStatus(IntEnum):
    opened = 1
    closed = 2


def get_payload(member: nextcord.Member, count: int):
    payload = {'voice.count': count}
    payload.update(MemberPayload(member)._to_dict())
    payload.update(GuildPayload(member.guild)._to_dict())
    return payload


class TempVoiceModule:
    async def process(
        self,
        member: nextcord.Member,
        before: Optional[nextcord.VoiceChannel],
        after: Optional[nextcord.VoiceChannel]
    ) -> None:
        self.member = member

        gdb = GuildDateBases(member.guild.id)
        data = await gdb.get('tempvoice')
        channels_data = await localdb.get_table('channels_data')

        if not (data and data.get('enabled')):
            return

        if before:
            voice_data = await channels_data.get(before.id)
            if voice_data and voice_data.get('mutes', {}).get(member.id):
                if after is None:
                    mutes = data.get('mutes', [])
                    mutes.append(member.id)
                    await gdb.set_on_json('tempvoice', 'mutes', mutes)
                else:
                    await member.edit(mute=False)
        if after:
            mutes = data.get('mutes', [])
            voice_data = await channels_data.get(after.id)
            if voice_data and voice_data.get('mutes', {}).get(member.id):
                await member.edit(mute=True)
            elif member.id in mutes:
                mutes.remove(member.id)
                await member.edit(mute=False)
                await gdb.set_on_json('tempvoice', 'mutes', mutes)

        if after and after.id == data['channel_id']:
            await self.create(after)
        if before and await channels_data.exists(before.id):
            await self.delete(before)

    async def get_embed(self) -> nextcord.Embed:
        gdb = GuildDateBases(self.member.guild.id)
        locale = await gdb.get('language')
        color = await gdb.get('color')
        get_emoji = await get_emoji_wrap(gdb)
        emoji = get_emoji('assets')

        embed = nextcord.Embed(
            title=i18n.t(locale, 'tempvoice.panel.message.title', emoji=emoji),
            description=i18n.t(locale, 'tempvoice.panel.message.description', emoji=emoji),
            color=color,
            timestamp=datetime.today()
        )
        return embed

    async def check_user(self, channel: nextcord.VoiceChannel):
        gdb = GuildDateBases(self.member.guild.id)
        locale = await gdb.get('language')
        channels_tracks_db = await localdb.get_table('channels_track_data')
        channels_data = await localdb.get_table('channels_data')
        channels_track_data = await channels_tracks_db.get(self.member.guild.id, [])

        for cid in channels_track_data:
            voice_data = await channels_data.get(cid)
            owner_id = voice_data['owner_id']

            if self.member.id != owner_id:
                continue

            if voice_data['status'] == VoiceStatus.closed:
                limited_time = snowflake_time(cid).timestamp()+TIMEOUT_VOICE
                if limited_time > time.time():
                    with contextlib.suppress(nextcord.Forbidden):
                        await channel.send(i18n.t(locale, 'tempvoice.errors.room_limit',
                                                  mention=self.member.mention, limited_time=limited_time))
                    await self.member.disconnect()
                    return False
            if voice_data['status'] == VoiceStatus.opened:
                channel = self.member.guild.get_channel(
                    voice_data['channel_id'])
                if channel is None:
                    voice_data['status'] = VoiceStatus.closed
                    voice_data['closed_time'] = time.time()
                    await channels_data.set(cid, voice_data)
                    continue
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

        type_panel = data.get('type_panel', 2)
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
                    read_message_history=True,
                    connect=True,
                    speak=True,
                    stream=True,
                    use_voice_activation=True,
                    priority_speaker=True,
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

        if data.get('type_message_panel', 2) in {2, 3}:
            if type_panel == 1:
                view = await TempVoiceView(self.member.guild.id)
            elif type_panel == 2:
                view = await AdvancedTempVoiceView(self.member.guild.id)
            else:
                view = None
            if view is not None:
                embed = await self.get_embed()
                await channel.send(embed=embed, view=view)

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
