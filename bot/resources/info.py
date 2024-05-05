import orjson
from bot.resources.ether import Emoji


DEFAULT_PREFIX = 'l.'
DEFAULT_COLOR = 2829617
DEFAULT_LANGUAGE = 'en'
DEFAULT_EMOJI = Emoji.diamod
DEFAULT_ECONOMY_SETTINGS = {
    'emoji': DEFAULT_EMOJI,
    "daily": 10,
    "weekly": 50,
    "monthly": 200,
    'work': {
        'min': 5,
        'max': 30,
        'cooldown': 60 * 60 * 6
    },
    'bet': {
        'min': 10,
        'max': 1000
    }
}
DEFAULT_ECONOMY_SETTINGS_JSON = orjson.dumps(DEFAULT_ECONOMY_SETTINGS).decode()


COUNT_ROLES_PAGE = 5

activities_list = [
    {
        'id': 880218394199220334,
        'label': 'Watch Together',
        'max_user': 'Unlimited'
    },
    {
        'id': 1037680572660727838,
        'label': 'Chef Showdown',
        'max_user': '15'
    },
    {
        'id': 1011683823555199066,
        'label': 'Krunker Strike FRVR',
        'max_user': '12'
    },
    {
        'id': 947957217959759964,
        'label': 'Bobble League',
        'max_user': '8'
    },
    {
        'id': 1106787098452832296,
        'label': 'Colonist',
        'max_user': '8'
    },
    {
        'id': 1007373802981822582,
        'label': 'Gartic Phone',
        'max_user': '16'
    },
    {
        'id': 945737671223947305,
        'label': 'Putt Party',
        'max_user': 'Unlimited'
    },
    {
        'id': 832025144389533716,
        'label': 'Blazing 8s',
        'max_user': '8'
    },
    {
        'id': 1070087967294631976,
        'label': 'Whiteboard',
        'max_user': 'Unlimited'
    },
    {
        'id': 1078728822972764312,
        'label': 'Know What I Meme',
        'max_user': '9'
    },
    {
        'id': 902271654783242291,
        'label': 'Sketch Heads',
        'max_user': '16'
    },
    {
        'id': 903769130790969345,
        'label': 'Land-io',
        'max_user': '16'
    },
    {
        'id': 1039835161136746497,
        'label': 'Color Together',
        'max_user': '100'
    },
    {
        'id': 852509694341283871,
        'label': 'SpellCast',
        'max_user': '6'
    },
    {
        'id': 879863686565621790,
        'label': 'Letter League',
        'max_user': '8'
    },
    {
        'id': 832013003968348200,
        'label': 'Checkers In The Park',
        'max_user': 'Unlimited'
    },
    {
        'id': 1107689944685748377,
        'label': 'Bobble Bash',
        'max_user': '8'
    },
    {
        'id': 755827207812677713,
        'label': 'Poker Night',
        'max_user': '25'
    }
]

site_link = "https://lordcord.fun/link-role-callback"
