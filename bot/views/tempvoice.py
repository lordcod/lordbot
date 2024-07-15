from __future__ import annotations
from enum import IntEnum
from typing import Optional
import nextcord

from bot.databases import GuildDateBases, localdb
from bot.languages import i18n


class VoiceStatus(IntEnum):
    opened = 1
    closed = 2


async def get_voice(interaction: nextcord.Interaction) -> Optional[nextcord.VoiceChannel]:
    channels_tracks_db = await localdb.get_table('channels_track_data')
    channels_data = await localdb.get_table('channels_data')
    channels_track_data = await channels_tracks_db.get(interaction.guild.id, [])

    for cid in channels_track_data:
        voice_data = await channels_data.get(cid)
        owner_id = voice_data['owner_id']
        status = voice_data['status']
        if interaction.user.id == owner_id and status == VoiceStatus.opened:
            return interaction.guild.get_channel(cid)
    return None


class OwnerSettingsDropDown(nextcord.ui.UserSelect):
    def __init__(self, locale: str) -> None:
        super().__init__(placeholder='Select the participant to whom you want to transfer the channel.')

    def get_view(self):
        view = nextcord.ui.View(timeout=300)
        view.add_item(self)
        return view

    async def callback(self, interaction: nextcord.Interaction) -> None:
        user = self.values[0]
        if user == interaction.user:
            await interaction.response.defer()
            return
        channels_data = await localdb.get_table('channels_data')
        voice = await get_voice(interaction)
        voice_data = await channels_data.get(voice.id)
        voice_data['owner_id'] = user.id
        await channels_data.set(voice.id, voice_data)
        await interaction.response.edit_message(content=f'You have successfully transferred the owner to the participant {user.mention}',
                                                view=None)


class UserPermissionSettingsDropDown(nextcord.ui.UserSelect):
    def __init__(self, locale: str) -> None:
        super().__init__(placeholder='Select the user from whom you want to grant/take away access to the channel')

    def get_view(self):
        view = nextcord.ui.View(timeout=300)
        view.add_item(self)
        return view

    async def callback(self, interaction: nextcord.Interaction) -> None:
        user = self.values[0]
        if user == interaction.user:
            await interaction.response.defer()
            return

        voice = await get_voice(interaction)
        perm = voice.overwrites.get(user)

        if not perm or not (perm.view_channel or perm.connect or perm.speak):
            await voice.set_permissions(
                target=user,
                view_channel=True,
                connect=True,
                speak=perm.speak,
            )
            await interaction.response.edit_message(content=f'You have granted access to the channel to a participant {user.mention}',
                                                    view=None)
        else:
            await voice.set_permissions(target=user,
                                        view_channel=False,
                                        connect=False,
                                        speak=perm.speak,)
            await interaction.response.edit_message(content=f'You have taken away access to the participant\'s {user.mention} channel',
                                                    view=None)


class UserKickSettingsDropDown(nextcord.ui.UserSelect):
    def __init__(self, locale: str) -> None:
        super().__init__(placeholder='Select the participant you want to kick')

    def get_view(self):
        view = nextcord.ui.View(timeout=300)
        view.add_item(self)
        return view

    async def callback(self, interaction: nextcord.Interaction) -> None:
        user = self.values[0]
        if user == interaction.user:
            await interaction.response.defer()
            return

        voice = await get_voice(interaction)
        if user not in voice.members:
            return

        await user.disconnect()

        await interaction.response.edit_message(f'You have successfully bailed out a participant {user.mention}')


class UserMuteSettingsDropDown(nextcord.ui.UserSelect):
    def __init__(self, locale: str) -> None:
        super().__init__(placeholder='Select the participant you want to turn off the microphone for')

    def get_view(self):
        view = nextcord.ui.View(timeout=300)
        view.add_item(self)
        return view

    async def callback(self, interaction: nextcord.Interaction) -> None:
        user = self.values[0]
        if user == interaction.user:
            await interaction.response.defer()
            return

        voice = await get_voice(interaction)
        perm = voice.overwrites.get(user)

        if not perm or not perm.speak:
            await voice.set_permissions(
                target=user,
                speak=True,
                view_channel=perm.view_channel,
                connect=perm.connect,
            )
            await interaction.response.edit_message(content=f'You have successfully turned on the microphone to the participant {user.mention}',
                                                    view=None)
        else:
            await voice.set_permissions(
                target=user,
                speak=False,
                view_channel=perm.view_channel,
                connect=perm.connect,
            )
            await interaction.response.edit_message(content=f'You have successfully turned off the microphone to the participant {user.mention}',
                                                    view=None)


class LimitSettingsModal(nextcord.ui.Modal):
    def __init__(self, locale: str) -> None:
        super().__init__('Channel limit')
        self.limit = nextcord.ui.TextInput(
            label='Limit',
            placeholder='Set the channel limit from 0 to 99. 0 is no limit.',
            max_length=2,
        )
        self.add_item(self.limit)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        limit = self.limit.value
        if not limit.isdigit() or int(limit) >= 100 or 0 > int(limit):
            await interaction.response.send_message('The limit format is incorrect.',
                                                    ephemeral=True)
            return

        if int(limit) == 0:
            limit = None
        else:
            limit = int(limit)

        voice = await get_voice(interaction)
        await voice.edit(user_limit=limit)
        await interaction.response.send_message('You have successfully set the channel limit.',
                                                ephemeral=True)


class NameSettingsModal(nextcord.ui.Modal):
    def __init__(self, locale: str) -> None:
        super().__init__('Channel name')
        self.name = nextcord.ui.TextInput(
            label='Name',
            placeholder='Set the channel name.',
            max_length=100,
        )
        self.add_item(self.name)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        name = self.name.value

        voice = await get_voice(interaction)
        await voice.edit(name=name)
        await interaction.response.send_message('You have successfully set the channel name.',
                                                ephemeral=True)


class TempVoiceFunctioins:
    def get_module(self, module_name: str):
        return getattr(self, 'process_'+module_name, None)

    async def run_interaction(self, interaction: nextcord.Interaction) -> None:
        custom_id = interaction.data['custom_id']
        module = self.get_module(custom_id.removeprefix('tempvoice:'))
        await module(interaction)

    async def process_change_owner(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        locale = await gdb.get('language')
        view = OwnerSettingsDropDown(locale).get_view()
        await interaction.response.send_message(view=view, ephemeral=True)

    async def process_give_access(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        locale = await gdb.get('language')
        view = UserPermissionSettingsDropDown(locale).get_view()
        await interaction.response.send_message(view=view, ephemeral=True)

    async def process_kick_member(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        locale = await gdb.get('language')
        view = UserKickSettingsDropDown(locale).get_view()
        await interaction.response.send_message(view=view, ephemeral=True)

    async def process_mute_member(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        locale = await gdb.get('language')
        view = UserMuteSettingsDropDown(locale).get_view()
        await interaction.response.send_message(view=view, ephemeral=True)

    async def process_set_limit(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        locale = await gdb.get('language')
        modal = LimitSettingsModal(locale)
        await interaction.response.send_modal(modal)

    async def process_change_name(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        locale = await gdb.get('language')
        modal = NameSettingsModal(locale)
        await interaction.response.send_modal(modal)

    async def process_change_ghost(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        locale = await gdb.get('language')
        voice = await get_voice(interaction)
        perm = voice.overwrites[interaction.guild.default_role]
        perm_dict = dict([*perm])
        res = perm_dict.pop('view_channel', None)
        if res:
            await voice.set_permissions(interaction.guild.default_role, view_channel=False, **perm_dict)
            await interaction.response.send_message('The channel has been successfully hide to everyone.',
                                                    ephemeral=True)
        else:
            await voice.set_permissions(interaction.guild.default_role, view_channel=True, **perm_dict)
            await interaction.response.send_message('The channel has been successfully shown to everyone.',
                                                    ephemeral=True)

    async def process_change_locked(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        locale = await gdb.get('language')
        voice = await get_voice(interaction)
        perm = voice.overwrites[interaction.guild.default_role]
        perm_dict = dict([*perm])
        res = perm_dict.pop('connect', None)
        if res:
            await voice.set_permissions(interaction.guild.default_role, connect=False, **perm_dict)
            await interaction.response.send_message('The channel has been successfully lock to everyone.',
                                                    ephemeral=True)
        else:

            await voice.set_permissions(interaction.guild.default_role, connect=True, **perm_dict)
            await interaction.response.send_message('The channel has been successfully unlock to everyone.',
                                                    ephemeral=True)


# 'Invite'
# 'Permit' 'Reject' 'Permit'
# 'Lock' 'Unlock' 'Lock'
# 'Ghost' 'Unghost' 'Ghost'
# 'Bitrate' 'Activity' 'NSFW'

voice_items = [
    {
        'value': 'change_owner',
        'label': 'Ownership',
        'description': 'Transfer ownership of the channel.',
        'emoji': '👑',
        'row': 1
    },
    {
        'value': 'set_limit',
        'label': 'Limit',
        'description': 'Set a channel limit.',
        'emoji': '👑',
        'row': 1
    },
    {
        'value': 'change_name',
        'label': 'Name',
        'description': 'Change the channel name.',
        'emoji': '👑',
        'row': 1
    },
    {
        'value': 'give_access',
        'label': 'Permit',
        'description': 'Grant/withdraw access rights to the channel.',
        'emoji': '👑',
        'row': 1
    },
    {
        'value': 'change_ghost',
        'label': 'Ghost',
        'description': 'Hide/open the channel.',
        'emoji': '👑',
        'row': 2
    },
    {
        'value': 'change_locked',
        'label': 'Lock',
        'description': 'Lock/unlock the channel.',
        'emoji': '👑',
        'row': 2
    },
    {
        'value': 'kick_member',
        'label': 'Kick',
        'description': 'Expel a participant from the voice.',
        'emoji': '👑',
        'row': 2
    },
    {
        'value': 'mute_member',
        'label': 'Mute',
        'description': 'Enable/disable the microphone for the participant..',
        'emoji': '👑',
        'row': 2
    },
]


class TempVoiceView(nextcord.ui.View):
    embed: nextcord.Embed

    def __init__(self) -> None:
        super().__init__(timeout=None)
        for data in voice_items:
            but = nextcord.ui.Button(
                custom_id='tempvoice:'+data['value'],
                emoji=data['emoji'],
                row=data['row']
            )
            but.callback = TempVoiceFunctioins().run_interaction
            self.add_item(but)

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        voice = await get_voice(interaction)
        if voice is None:
            await interaction.response.send_message("I didn't find the private room you opened.",
                                                    ephemeral=True)
            return False
        return True
