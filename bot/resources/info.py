import nextcord
import orjson
from bot.resources.ether import Emoji


DEFAULT_PREFIX = 'l.'
DEFAULT_COLOR = 2829617
DEFAULT_LANGUAGE = 'en'
DEFAULT_EMOJI = Emoji.diamod
DEFAULT_ECONOMY_THEFT = {
    'cooldown': 86400,
    'jail': True,
    'time_prison': {
        'min': 86400,
        'max': 259200,
        'adaptive': 86400
    }
}
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
    },
    'theft': DEFAULT_ECONOMY_THEFT
}
DEFAULT_ECONOMY_SETTINGS_JSON = orjson.dumps(DEFAULT_ECONOMY_SETTINGS).decode()
DEFAULT_GUILD_DATA = {
    'language': 'en',
    'prefix': 'l.',
    'color': 1974050,
    'economic_settings': {},
    'greeting_message': {},
    'auto_roles': {},
    'ideas': {},
    'music_settings': {},
    'auto_translate': {},
    'command_permissions': {},
    'tickettool': {},
    'invites': {},
    'giveaways': {},
    'polls': {},
    'logs': {},
    'role_reactions': {},
    'delete_task': 0
}

COUNT_ROLES_PAGE = 5

DEFAULT_TICKET_PAYLOAD = {
    'names': {
        'open': '{ticket.count}-ticket',
        'close': '{ticket.count}-closed'
    },
    'messages': {
        'panel': orjson.dumps({
            "title": "Tickets",
            "description": "If you have a question about the operation of the server, click on interaction to create a request.",
            "color": "{guild.color}",
            "footer": {
                "text": "{bot.displayName}",
                "timestamp": "{today_dt}",
                'icon_url': '{bot.avatar}'
            }, "thumbnail": ""
        }).decode(),
        'controller': orjson.dumps({
            "title": "Support team ticket controls",
            "color": "{guild.color}",
            "footer": {
                "timestamp": "{today_dt}"
            },
        }).decode(),
        'close': orjson.dumps({
            "title": "Action",
            "description": "The ticket is closed by {member.mention}",
            "color": 16765743,
            "footer": {
                "timestamp": "{today_dt}"
            },
        }).decode(),
        'reopen': orjson.dumps({
            "title": "Action",
            "description": "The ticket is opened by {member.mention}",
            "color": 53380,
            "footer": {
                "timestamp": "{today_dt}"
            },
        }).decode(),
        'delete': orjson.dumps({
            "title": "Action",
            "description": 'Ticket will be deleted in a few seconds',
            "color": 16718362,
            "footer": {
                "timestamp": "{today_dt}"
            },
        }).decode(),
        'open': '{member} Welcome!',
    },
    'buttons': {
        'category_placeholder': 'Select the category of the request',
        'modal_placeholder': 'Ticket Forms',
        'faq_placeholder': 'FAQ',
        'faq_option': {
            'label': 'Didn\'t find the answer?',
            'emoji': Emoji.tickets,
            'description': 'Click to create a request',
        },
        'faq_button_open': {
            'label': 'FAQ',
            'emoji': Emoji.faq,
            'style': nextcord.ButtonStyle.blurple,
        },
        'faq_button_create': {
            'label': 'Create appeal',
            'emoji': Emoji.tickets,
            'style': nextcord.ButtonStyle.secondary,
        },
        'close_button': {
            'label': "Close ticket",
            'emoji': "🔒",
            'style': nextcord.ButtonStyle.red,
        },
        'reopen_button': {
            'label': 'Reopen ticket',
            'emoji': '🔓',
            'style': nextcord.ButtonStyle.secondary,
        },
        'delete_button': {
            'label': 'Delete ticket',
            'emoji': '⛔',
            'style': nextcord.ButtonStyle.red,
        },

    }
}


DEFAULT_TICKET_PERMISSIONS_PERM = {
    'moderator': nextcord.PermissionOverwrite(
        view_channel=True,
        send_messages=True,
        embed_links=True,
        attach_files=True,
        add_reactions=True,
        use_external_emojis=True,
        use_external_stickers=True,
        manage_messages=True,
        manage_threads=True,
        read_message_history=True
    ).pair(),
    'owner': nextcord.PermissionOverwrite(
        view_channel=True,
        send_messages=True,
        embed_links=True,
        attach_files=True,
        add_reactions=True,
        use_external_emojis=True,
        use_external_stickers=True,
        read_message_history=True
    ).pair(),
    'addtional': nextcord.PermissionOverwrite(
        view_channel=True,
        send_messages=True
    ).pair(),
    'everyone': nextcord.PermissionOverwrite(view_channel=False).pair()
}
DEFAULT_TICKET_PERMISSIONS = {k: (v[0].value, v[1].value) for k, v in DEFAULT_TICKET_PERMISSIONS_PERM.items()}

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
