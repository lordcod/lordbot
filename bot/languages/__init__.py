import nextcord
from datetime import datetime
from nextcord.utils import format_dt,escape_markdown


data = [
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

current = [
    {"locale":"en","english_name":"English","native_name":"English","flag":"🇬🇧"},
    {"locale":"ru","english_name":"Russian","native_name":"Pусский","flag":"🇷🇺"},
]

class BotInfo:
    title = {
        'en':'This is a multifunctional bot',
        'ru':'это многофункциональный бот'
    }
    description = {
        'en':'The bot is designed to facilitate server management and is equipped with various automation tools',
        'ru':'Бот предназначен для облегчения управления сервером и оснащен различными средствами автоматизации'
    }
    
    info_server = {
        'en':'Information about the server',
        'ru':'Информация о сервере'
    }
    prefix_server = {
        'en':'Server prefix',
        'ru':'Префикс сервера'
    }

class translate:
    placeholder = {
        'ru':'Выберете подходящий язык:',
        'en':'Will choose the appropriate language:'
    }

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

class errors:
    MissingPermissions = {
        'en':'You don\'t have enough rights',
        'ru':'У вас недостаточно прав'
    }
    BotMissingPermissions = {
        'en':'The bot does not have enough rights to perform this action, most likely you took it away when adding the bot to the server',
        'ru':'У бота недостаточно прав для выполнения этого действия, скорее всего, вы убрали их при добавлении бота на сервер'
    }
    MissingRole = {
        'en':'You don\'t have a suitable role to execute the command',
        'ru':'У вас нет нужной роли для выполнения команды'
    }
    
    NotOwner = {
        'en':'This command is intended for the bot owner',
        'ru':'Эта команда предназначена для владельца бота'
    }
    CommandNotFound = {
        'en':'There is no such command',
        'ru':'Такой команды нет'
    }
    CheckFailure = {
        'en':'You don\'t fulfill all the conditions',
        'ru':'Вы не выполняете всех условий'
    }
    BadArgument = {
        'en':'Invalid argument entered',
        'ru':'Введен недопустимый аргумент'
    }
    DisabledCommand = {
        'en':'This command is disabled on the server',
        'ru':'Эта команда отключена на сервере'
    }
    MissingRequiredArgument = {
        'en':'You didn\'t enter a required argument',
        'ru':'Вы не ввели обязательный аргумент'
    }
    NotActivateEconomy = {
        'en':'The economy system is disabled on the server',
        'ru':'Система экономики отключена на сервере'
    }
    OnlyTeamError = {
        'en':'This command can only be used by the bot team',
        'ru':'Эта команда может быть использована только командой бота'
    }
    
    class CommandOnCooldown:
        title = {
            'en':'The command is on hold',
            'ru':'Команда находится в режиме ожидания'
        }
        description = {
            'en':'Try again after',
            'ru':'Повторите попытку через'
        }
        seconds = {
            'en':'seconds',
            'ru':'секунд'
        }
