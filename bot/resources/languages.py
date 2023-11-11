import nextcord
from datetime import datetime
from nextcord.utils import format_dt,escape_markdown


Languages_information = [
    {"discord_language":"da","google_language":"da","english_name":"Danish","native_name":"Dansk","flag":"🇩🇰"},
    {"discord_language":"de","google_language":"de","english_name":"German","native_name":"Deutsch","flag":"🇩🇪"},
    {"discord_language":"en-GB","google_language":"en","english_name":"English, UK","native_name":"English, UK","flag":"🇬🇧"},
    {"discord_language":"es-ES","google_language":"es","english_name":"Spanish","native_name":"Español","flag":"🇪🇸"},
    {"discord_language":"fr","google_language":"fr","english_name":"French","native_name":"Français","flag":"🇫🇷"},
    {"discord_language":"hr","google_language":"hr","english_name":"Croatian","native_name":"Hrvatski","flag":"🇭🇷"},
    {"discord_language":"it","google_language":"it","english_name":"Italian","native_name":"Italiano","flag":"🇮🇹"},
    {"discord_language":"hu","google_language":"hu","english_name":"Hungarian","native_name":"Magyar","flag":"🇭🇺"},
    {"discord_language":"nl","google_language":"nl","english_name":"Dutch","native_name":"Nederlands","flag":"🇳🇱"},
    {"discord_language":"pl","google_language":"pl","english_name":"Polish","native_name":"Polski","flag":"🇵🇱"},
    {"discord_language":"pt-BR","google_language":"pt","english_name":"Portuguese, Brazilian","native_name":"Português do Brasil","flag":"🇵🇹"},
    {"discord_language":"ro","google_language":"ro","english_name":"Romanian, Romania","native_name":"Română","flag":"🇷🇴"},
    {"discord_language":"fi","google_language":"fi","english_name":"Finnish","native_name":" Suomi","flag":"🇫🇮"},
    {"discord_language":"sv-SE","google_language":"sv","english_name":"Swedish","native_name":"Svenska","flag":"🇸🇻"},
    {"discord_language":"vi","google_language":"vi","english_name":"Vietnamese","native_name":"Tiếng Việt","flag":"🇻🇮"},
    {"discord_language":"tr","google_language":"tr","english_name":"Turkish","native_name":"Türkçe","flag":"🇹🇷"},
    {"discord_language":"cs","google_language":"cs","english_name":"Czech","native_name":"Čeština","flag":"🇨🇿"},
    {"discord_language":"el","google_language":"el","english_name":"Greek","native_name":"Ελληνικά","flag":"🇬🇷"},
    {"discord_language":"bg","google_language":"bg","english_name":"Bulgarian","native_name":"български","flag":"🇧🇬"},
    {"discord_language":"ru","google_language":"ru","english_name":"Russian","native_name":"Pусский","flag":"🇷🇺"},
    {"discord_language":"uk","google_language":"uk","english_name":"Ukrainian","native_name":"Українська","flag":"🇺🇦"},
    {"discord_language":"zh-CN","google_language":"zh-cn","english_name":"Chinese, Taiwan","native_name":"繁體中文","flag":"🇨🇳"},
    {"discord_language":"hi","google_language":"hi","english_name":"Hindi","native_name":"हिन्दी","flag":"🇮🇳"},
    {"discord_language":"th","google_language":"th","english_name":"Thai","native_name":"ไทย","flag":"🇹🇭"},
    {"discord_language":"ja","google_language":"ja","english_name":"Japanese","native_name":"日本語","flag":"🇯🇵"},
    
    {"discord_language":"no","google_language":"no","english_name":"Norwegian","native_name":"Norsk","flag":"🇳🇴"},
    {"discord_language":"lt","google_language":"lt","english_name":"Lithuanian","native_name":"Lietuviškai","flag":"🇱🇹"},
    {"discord_language":"en-US","google_language":"en","english_name":"English, US","native_name":"English, US","flag":"🇺🇸"},
    {"discord_language":"zh-TW","google_language":"zh-tw","english_name":"Chinese, China","native_name":"中文","flag":"🇹🇼"},
    {"discord_language":"ko","google_language":"ko","english_name":"Korean","native_name":"한국어","flag":"🇰🇷"}
]

Languages_self = [
    Languages_information[2],
    Languages_information[19],
]

class Emoji:
    congratulation = '<a:congratulation:1165684808844845176>'
    owner = '<:owner:1166002519315599500>'
    verified = '<:verified:1166001046468964406>'
    create = '<:paint:1166001043562307674>'
    channel_text = '<:channel_text:1166001040198484178>'
    channel_voice = '<:channel_voice:1166001038772404284>'
    channel_forum = '<:channel_forum:1166094701020070009>'
    channel_stage = '<:channel_stage:1166092341317226566>'
    category = '<:category:1166001036553621534>'
    text1 = '<:text1:1166001701912846346>'
    text2 = '<:text2:1166001699295592528>'
    member = '<:member:1166001035182080161>'
    channel_announce = '<:channel_announce:1166092338242785370>'
    thread = '<:thread:1166096258511937666>'
    roketa = '<a:rocketa:1165684783754522704>'
    bagmoney = '<:bag_money:1172834872067362818>'
    bank = '<:bank:1165684762279673948>'
    money = '<:money:1165684764775297187>'
    award = '<a:award:1165684769829421209>'
    economy = '<:economy:1172611420454649937>'
    languages = '<:languages:1172611417170526319>'
    prefix = '<:prefix:1172611415392124998>' 
    colour = '<:colour:1172611412519043102>'
    reactions = '<:reactions:1172862660442853497>'
    auto_translate = '<:autotranslate:1172862657586544750>'
    thread_message = '<:threadmessage:1172862656030453770>'


class invites:
    verification_level = {
        'ru':[
                "нет",
                "низкий",
                "средний",
                "высокий",
                "высочайший"
            ],
        'en':[
            'none',
            'low',
            'medium',
            'high',
            'highest'
        ]
    }
    
    channel_type = {
        0:Emoji.channel_text,
        1:Emoji.channel_text,
        2:Emoji.channel_voice,
        3:Emoji.category,
        4:Emoji.category,
        5:Emoji.channel_announce,
        10:Emoji.thread,
        11:Emoji.thread,
        12:Emoji.thread,
        13:Emoji.channel_stage,
        14:Emoji.category,
        15:Emoji.channel_forum,
        16:Emoji.channel_forum,
    }

    title = {
            'ru':f'Приглашение на',
            'en':f'Invitation to'
        }
    
    footer = {
            'ru':'Приглашающий:',
            'en':'Inviter:'
        }
    
    custom_invite = {
        'en':'Custom Invite Link',
        'ru':'Пользовательская ссылка для приглашения'
    }
    
    @property
    def field_guild(self):
        invite = self.invite 
        guild = invite.guild
        return {
            'ru':(
                f'{Emoji.owner} Владелец: {guild.owner.mention}\n'
                f'{Emoji.verified} Уровень проверки: {self.verification_level["ru"][guild.verification_level.value]}\n'
                f'{Emoji.create} Создан: {format_dt(guild.created_at,"f")} ({format_dt(guild.created_at,"R")})\n'
                f'{Emoji.channel_text} Всего {len(guild.channels)} каналов\n'
                f'{Emoji.text1}{Emoji.channel_text} Текстовые каналы: {len(guild.text_channels)}\n'
                f'{Emoji.text1}{Emoji.channel_voice}  Голосовые каналы: {len(guild.voice_channels)}\n'
                f'{Emoji.text1}{Emoji.channel_forum}  Форум: {len(guild.forum_channels)}\n'
                f'{Emoji.text1}{Emoji.channel_stage}  Трибуны: {len(guild.stage_channels)}\n'
                f'{Emoji.text2}{Emoji.category}  Категории: {len(guild.categories)}\n'
                f'{Emoji.member} Всего {guild.member_count} пользователя\n'
                f'{Emoji.text1} Ботов: {len(guild.bots)}\n'
                f'{Emoji.text2} Участников: {len(guild.humans)}'
            ),
            'en':(
                f'{Emoji.owner} Owner: {guild.owner.mention}\n'
                f'{Emoji.verified} Verification level: {self.verification_level["en"][guild.verification_level.value]}\n'
                f'{Emoji.create} Generated: {format_dt(guild.created_at,"f")} ({format_dt(guild.created_at,"R")})\n'
                f'{Emoji.channel_text} Total {len(guild.channels)} channels\n'
                f'{Emoji.text1}{Emoji.channel_text} Text channels: {len(guild.text_channels)}\n'
                f'{Emoji.text1}{Emoji.channel_voice}  Voice channels: {len(guild.voice_channels)}\n'
                f'{Emoji.text1}{Emoji.channel_forum}  Forums: {len(guild.forum_channels)}\n'
                f'{Emoji.text1}{Emoji.channel_stage}  Stands: {len(guild.stage_channels)}\n'
                f'{Emoji.text2}{Emoji.category} Categories: {len(guild.categories)}\n'
                f'{Emoji.member} Total {guild.member_count} user\n'
                f'{Emoji.text1} Bots: {len(guild.bots)}\n'
                f'{Emoji.text2} Participants: {len(guild.humans)}'
            )
        }

class captcha:
    congratulation = {
        'ru':'Поздравляю, вы ввели капчу!',
        'en':'Congratulations you have passed the captcha!'
    }
    enter = {
        'ru':'У вас есть 30 секунд чтобы решить капчу!',
        'en':'You have 30 seconds to solve the captcha!'
    }
    failed = {
        'ru':'Капча не пройдена',
        'en':'Captcha failed'
    }

class activiti:
    failed = {
        'ru':'Это действие недоступно или не работает',
        'en':'This activity is unavailable or does not work'
    }
    embed_title = {
        'ru':'Активность успешно создана!',
        'en':'The activity has been successfully created!'
    }
    embed_description = {
        'ru':'Однако некоторые виды активностей могут быть недоступны для вашего сервера, если уровень бустов не соответствует требованиям активности.',
        'en':'However, some types of activities may not be available for your server if the boost level does not meet the activity requirements.'
    }
    fields_label = {
        'ru':'Название активности',
        'en':'Activity name'
    }
    fields_max_user = {
        'ru':'Максимальное кол-во пользователей',
        'en':'Maximum number of users'
    }

class auto_translate:
    title = {
        'ru':'Авто перевод',
        'en':'Automatic translation'
    }
    field_name_from = {
        'ru':'Переведено c',
        'en':'Translated from'
    }
    field_name_to = {
        'ru':'Переведено на',
        'en':'Translated to'
    }