description = {
    'change_ghost': {'description': 'Hide/open the channel.', 'label': 'Ghost'},
    'change_locked': {'description': 'Lock/unlock the channel.', 'label': 'Lock'},
    'change_name': {'description': 'Change the channel name.', 'label': 'Name'},
    'change_owner': {'description': 'Transfer ownership of the channel.',
                     'label': 'Ownership'},
    'ghost': {'description': 'Hide the channel.', 'label': 'Ghost'},
    'give_access': {'description': 'Grant/withdraw access rights to the channel.',
                    'label': 'Permit'},
    'invite': {'description': 'Invite a participant to your voice.',
               'label': 'Invite'},
    'kick_member': {'description': 'Expel a participant from the voice.',
                    'label': 'Kick'},
    'lock': {'description': 'Lock the channel.', 'label': 'Lock'},
    'mute_member': {'description': 'Enable/disable the microphone for the '
                    'participant..',
                    'label': 'Mute'},
    'mute_member_fd': {'description': 'Disable the microphone for the '
                       'participant..',
                       'label': 'Mute'},
    'permit': {'description': 'Grant access rights to the channel.',
               'label': 'Permit'},
    'reject': {'description': 'Withdraw access rights to the channel.',
               'label': 'Reject'},
    'set_bitrate': {'description': 'Change the channel bitrate.',
                    'label': 'Bitrate'},
    'set_limit': {'description': 'Set a channel limit.', 'label': 'Limit'},
    'unghost': {'description': 'Open the channel.', 'label': 'Unghost'},
    'unlock': {'description': 'Unlock the channel.', 'label': 'Unlock'},
    'unmute_member_fd': {'description': 'Enable the microphone for the '
                         'participant..',
                         'label': 'Unmute'}
}

simple_dd_voice_items = [
    [
        {'emoji': 'owner', 'value': 'change_owner'},
        {'emoji': 'limit',  'value': 'set_limit'},
        {'emoji': 'name', 'value': 'change_name'},
        {'emoji': 'permit', 'value': 'give_access'}
    ],
    [
        {'emoji': 'hide', 'row': 2, 'value': 'change_ghost'},
        {'emoji': 'lock', 'row': 2, 'value': 'change_locked'},
        {'emoji': 'kick', 'row': 2, 'value': 'kick_member'},
        {'emoji': 'micoff', 'row': 2, 'value': 'mute_member'}
    ]
]


simple_but_voice_items = [
    {'emoji': 'owner', 'row': 1, 'value': 'change_owner'},
    {'emoji': 'limit', 'row': 1, 'value': 'set_limit'},
    {'emoji': 'name', 'row': 1, 'value': 'change_name'},
    {'emoji': 'permit', 'row': 1, 'value': 'give_access'},
    {'emoji': 'hide', 'row': 2, 'value': 'change_ghost'},
    {'emoji': 'lock', 'row': 2, 'value': 'change_locked'},
    {'emoji': 'kick', 'row': 2, 'value': 'kick_member'},
    {'emoji': 'micoff', 'row': 2, 'value': 'mute_member'}
]


advance_dd_voice_items = [
    [
        {'emoji': 'owner', 'value': 'change_owner'},
        {'emoji': 'invite', 'value': 'invite'},
        {'emoji': 'limit', 'value': 'set_limit'},
        {'emoji': 'name', 'value': 'change_name'},
        {'emoji': 'bitrate', 'value': 'set_bitrate'}
    ],
    [
        {'emoji': 'kick', 'value': 'kick_member'},
        {'emoji': 'mic', 'value': 'unmute_member_fd'},
        {'emoji': 'micoff', 'value': 'mute_member_fd'},
        {'emoji': 'permit', 'value': 'permit'},
        {'emoji': 'reject', 'value': 'reject'},
        {'emoji': 'show', 'value': 'ghost'},
        {'emoji': 'hide', 'value': 'unghost'},
        {'emoji': 'lock', 'value': 'lock'},
        {'emoji': 'open', 'value': 'unlock'}
    ]
]


advance_but_voice_items = [
    {'emoji': 'owner', 'row': 1, 'value': 'change_owner'},
    {'emoji': 'limit', 'row': 1, 'value': 'set_limit'},
    {'emoji': 'name', 'row': 1, 'value': 'change_name'},
    {'emoji': 'bitrate', 'row': 1, 'value': 'set_bitrate'},
    {'emoji': 'invite', 'row': 1, 'value': 'invite'},
    {'emoji': 'kick', 'row': 2, 'value': 'kick_member'},
    {'emoji': 'mic', 'row': 2, 'value': 'unmute_member_fd'},
    {'emoji': 'micoff', 'row': 2, 'value': 'mute_member_fd'},
    {'emoji': 'permit', 'row': 2, 'value': 'permit'},
    {'emoji': 'reject', 'row': 2, 'value': 'reject'},
    {'emoji': 'hide', 'row': 3, 'value': 'ghost'},
    {'emoji': 'show', 'row': 3, 'value': 'unghost'},
    {'emoji': 'lock', 'row': 3, 'value': 'lock'},
    {'emoji': 'open', 'row': 3, 'value': 'unlock'},
]
