import orjson


DEFAULT_PREFIX = 'l.'
DEFAULT_COLOR = 1974050
DEFAULT_LANGUAGE = 'en'
DEFAULT_EMOJI = '<:diamond:1183363436780978186>'
DEFAULT_ECONOMY_SETTINGS = orjson.dumps({'emoji': DEFAULT_EMOJI}).decode()

activities_list = [
    {'id': 880218394199220334,
     'label': 'Watch Together',
     'max_user': 'Unlimited'
     },
    {'id': 755827207812677713,
     'label': 'Poker Night',
     'max_user': '25'},
    {'id': 832012774040141894,
     'label': 'Chess In The Park',
     'max_user': 'Unlimited'},
    {'id': 902271654783242291,
     'label': 'Sketch Heads',
     'max_user': '16'},
    {'id': 879863686565621790,
     'label': 'Letter League',
     'max_user': '8'},
    {'id': 832013003968348200,
     'label': 'Checkers In The Park',
     'max_user': 'Unlimited'},
    {'id': 832025144389533716,
     'label': 'Blazing 8s',
     'max_user': '8'},
    {'id': 945737671223947305,
     'label': 'Putt Party',
     'max_user': 'Unlimited'},
    {'id': 903769130790969345,
     'label': 'Land-io',
     'max_user': '16'},
    {'id': 947957217959759964,
     'label': 'Bobble League',
     'max_user': '8'},
    {'id': 1007373802981822582,
     'label': 'Gartic Phone',
     'max_user': '16'},
    {'id': 1039835161136746497,
     'label': 'Color Together',
     'max_user': '100'},
    {'id': 1070087967294631976,
     'label': 'Jamspace Whiteboard',
     'max_user': 'Unlimited'},
    {'id': 1037680572660727838,
     'label': 'Chef Showdown',
     'max_user': '15'},
    {'id': 1107689944685748377,
     'label': 'Bobble Bash',
     'max_user': '8'},
]

invite_link = (
    'https://discord.com/oauth2/authorize'
    '?client_id=1095713975532007434'
    '&scope=bot+applications.commands'
    '&permissions=-1'
    '&response_type=code'
    '&redirect_uri=https%3A%2F%2Flordcord.fun%2Flink-role-callback'
)

site_link = "https://lordcord.fun/link-role-callback"
