from typing import Optional, NamedTuple
import nextcord
import jmespath


class _TempChannelData(NamedTuple):
    guild_id: int
    owner_id: int


nextcord.Permissions
_db_data = []
_guild_data = {
    'category_id': 1216365743671873678,
    'trigger_channel_id': 0,  # 1216365803042246756,
    'owner_permission': nextcord.PermissionOverwrite(
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
    'everyone_permission': nextcord.PermissionOverwrite(
        create_instant_invite=True,
        view_channel=True,
        connect=True,
        speak=True,
        stream=True,
        use_voice_activation=True,
        priority_speaker=True
    ),
    'channel_name': '{count}-{name}'
}


class TempChannelsDataBases:
    @staticmethod
    def create(guild_id: int, owner_id: int, channel_id: int):
        _db_data.append({
            'guild_id': guild_id,
            'owner_id': owner_id,
            'channel_id': channel_id
        })

    @staticmethod
    def get(guild_id: int, owner_id: int) -> Optional[int]:
        return jmespath.search(f"[?guild_id==`{guild_id}`&&owner_id==`{owner_id}`]|[0].channel_id", _db_data)

    @staticmethod
    def get_as_channel(channel_id: int) -> Optional[_TempChannelData]:
        data = jmespath.search(
            f"[?channel_id==`{channel_id}`]|[0].[guild_id, owner_id]", _db_data)
        if data is None:
            return None
        return _TempChannelData(*data)

    @staticmethod
    def get_count(guild_id: int) -> int:
        return jmespath.search(f"length([?guild_id==`{guild_id}`])", _db_data)+1

    @staticmethod
    def delete(guild_id: int, owner_id: int):
        data = jmespath.search(
            f"[?guild_id==`{guild_id}`&&owner_id==`{owner_id}`]|[0]", _db_data)
        if data is None:
            return
        _db_data.remove(data)

    @staticmethod
    def delete_as_channel(channel_id: int):
        data = jmespath.search(
            f"[?channel_id==`{channel_id}`]|[0]", _db_data)
        if data is None:
            return
        _db_data.remove(data)


class TempChannels:
    def __init__(self, channel: nextcord.VoiceChannel) -> None:
        self.channel = channel

    @classmethod
    async def create(cls, guild: nextcord.Guild, member: nextcord.Member) -> 'TempChannels':
        channel = await guild.create_voice_channel(
            name=_guild_data.get('channel_name').format(
                count=TempChannelsDataBases.get_count(guild.id),
                name=member.display_name
            ),
            category=guild.get_channel(_guild_data.get('category_id')),
            overwrites={
                member: _guild_data.get('owner_permission'),
                guild.default_role: _guild_data.get('everyone_permission')
            }
        )
        await member.move_to(channel)
        TempChannelsDataBases.create(guild.id, member.id, channel.id)
        return cls(channel)

    async def delete(self) -> None:
        tcdb = TempChannelsDataBases.get_as_channel(self.channel.id)
        if tcdb is None:
            return
        TempChannelsDataBases.delete_as_channel(self.channel.id)
        await self.channel.delete()
