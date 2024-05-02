from typing import Optional, NamedTuple
import nextcord
import jmespath



_db_data = {}
_guild_data = {
    'category_id': 1216365743671873678,
    'trigger_channel_id': 0,  # 1216365803042246756,
    'owner_permission': (305137425, 0),
    'everyone_permission': (36701953, 0),
    'channel_name': '{count}-{name}'
}



class TempChannels:
    def __init__(self, channel: nextcord.VoiceChannel) -> None:
        self.channel = channel
        self.owner_id = _db_data[channel.id]
        self.owner = channel.guild.get_member(self.owner_id)

    @classmethod
    async def create(cls, guild: nextcord.Guild, member: nextcord.Member) -> 'TempChannels':
        owner_permission_allow, owner_permission_deny = _guild_data.get(
            'owner_permission')
        everyone_permission_allow, everyone_permission_deny = _guild_data.get(
            'everyone_permission')
        channel = await guild.create_voice_channel(
            name=_guild_data.get('channel_name').format(
                count=1,
                name=member.display_name
            ),
            category=guild.get_channel(_guild_data.get('category_id')),
            overwrites={
                member: nextcord.PermissionOverwrite.from_pair(nextcord.Permissions(
                    owner_permission_allow), nextcord.Permissions(owner_permission_deny)),
                guild.default_role: nextcord.PermissionOverwrite.from_pair(nextcord.Permissions(
                    everyone_permission_allow), nextcord.Permissions(everyone_permission_deny))
            }
        )
        _db_data[channel.id] = (guild.id, member.id)
        await member.move_to(channel)
        return cls(channel)

    async def delete(self) -> None:
        tcdb = _db_data.get(self.channel.id)
        if tcdb is None:
            return
        _db_data.pop(self.channel.id)
        await self.channel.delete()
    
    async def edit_name(self, member: nextcord.Member, name: str) -> None:
        if member != self.owner:
            return
        await self.channel.edit(name=name)
    
    async def edit_limit(self, member: nextcord.Member, limit: int) -> None:
        if member != self.owner:
            return
        await self.channel.edit(user_limit=limit)
    
    async def edit_region(self, member: nextcord.Member, region: nextcord.VoiceRegion) -> None:
        if member != self.owner:
            return
        self.channel.edit(rtc_region=region)
    
    async def edit_privacy_hiden(self, member: nextcord.Member) -> None:
        if member != self.owner:
            return
        await self.channel.edit(overwrites={
            member.guild.default_role: nextcord.PermissionOverwrite(view_channel=False, connect=False)
        })

    async def edit_privacy_shown(self, member: nextcord.Member) -> None:
        if member != self.owner:
            return
        await self.channel.edit(overwrites={
            member.guild.default_role: nextcord.PermissionOverwrite(view_channel=True, connect=True)
        })
    
    async def add_trust(self, member: nextcord.Member, trust: nextcord.Member) -> None:
        if member != self.owner:
            return
        await self.channel.edit(overwrites={
            trust: nextcord.PermissionOverwrite(view_channel=True, connect=True)
        })

    async def remove_trust(self, member: nextcord.Member, trust: nextcord.Member) -> None:
        if member != self.owner:
            return
        await self.channel.edit(overwrites={
            trust: nextcord.PermissionOverwrite(view_channel=False, connect=False)
        })
    
    async def invite(self, member: nextcord.Member, trust: nextcord.Member) -> None:
        if member != self.owner:
            return
        invite = await self.channel.create_invite(max_uses=1)
        await trust.send(invite.url)

    async def kick(self, member: nextcord.Member, trust: nextcord.Member) -> None:
        if member != self.owner:
            return
        if trust not in self.channel.members:
            return
        await trust.disconnect()
    
    async def block(self, member: nextcord.Member, trust: nextcord.Member) -> None:
        if member != self.owner:
            return
        if trust not in self.channel.members:
            await trust.disconnect()
        await self.channel.edit(overwrites={
            trust: nextcord.PermissionOverwrite(speak=False, view_channel=False, connect=False)
        })
    
    async def unblock(self, member: nextcord.Member, trust: nextcord.Member) -> None:
        if member != self.owner:
            return
        if trust not in self.channel.members:
            await trust.disconnect()
        await self.channel.edit(overwrites={
            trust: nextcord.PermissionOverwrite(speak=True, view_channel=True, connect=True)
        })
    
    async def transfer(self, member: nextcord.Member, new_owner: nextcord.Member) -> None:
        if member != self.owner:
            return
        owner_permission_allow, owner_permission_deny = _guild_data.get(
            'owner_permission')
        await self.channel.edit(overwrites={
                new_owner: nextcord.PermissionOverwrite.from_pair(nextcord.Permissions(
                    owner_permission_allow), nextcord.Permissions(owner_permission_deny)),
                member: None
            })