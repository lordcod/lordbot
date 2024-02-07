from typing import List, Dict, TypedDict


class CommandOption(TypedDict):
    name: str
    category: str
    aliases: List[str]
    arguments: List[str]
    descriptrion: Dict[str, str]
    brief_descriptrion: Dict[str, str]
    allowed_disabled: bool


categories_emoji: Dict[str, str] = {
    'economy': '💎',
    'major': '👑',
    'voice': '🎤',
    'moderation': '⚠',
}

categories_name:  Dict[str, Dict[str, str]] = {
    'economy': {
        'ru': 'Экономика',
        'en': 'Economy',
        'id': 'Ekonomi',
        'da': 'Økonomi',
        'de': 'Wirtschaft',
        'es': 'Economía',
        'fr': 'Économie',
        'pl': 'Gospodarka',
        'tr': 'Ekonomi'
    },
    'major': {
        'ru': 'Главное',
        'en': 'Major',
        'id': 'Mayor',
        'da': 'Stor',
        'de': 'Wichtigsten',
        'es': 'Mayor',
        'fr': 'Majeur',
        'pl': 'Major',
        'tr': 'Büyük'
    },
    'voice': {
        'ru': 'Голос',
        'en': 'Voice',
        'id': 'Suara',
        'da': 'Stemme',
        'de': 'Stimme',
        'es': 'Voz',
        'fr': 'Voix',
        'pl': 'Głos',
        'tr': 'Ses'
    },
    'moderation': {
        'ru': 'Модерационные',
        'en': 'Moderation',
        'id': 'Moderasi',
        'da': 'Moderation',
        'de': 'Moderation',
        'es': 'Moderación',
        'fr': 'Modération',
        'pl': 'Moderacja',
        'tr': 'Ilımlılık'
    },
}

categories: Dict[str, List[CommandOption]] = {
    'economy': [
        {
            'name': 'balance',
            'category': 'economy',
            'aliases': ['bal'],
            'arguments': ['[member]'],
            'descriptrion': {
                'en': (
                    'Displays the participant\'s balance as well as possible rewards that can be collected\n\n'
                    'If no participant is specified, the value is taken by the one who started the command'
                ),
                'ru': (
                    'Отображает баланс участника, а также возможные вознаграждения, которые можно получить\n\n'
                    'Если участник не указан, значение принимает тот, кто запустил команду'
                ),
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Participant\'s balance',
                'ru': 'Баланс участника',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True
        },
        {
            'name': 'leaderboard',
            'category': 'economy',
            'aliases': [],
            'arguments': [],
            'descriptrion': {
                'en': 'Shows statistics of the top 10 server participants by balance',
                'ru': 'Показывает статистику по 10 лучшим участникам сервера по балансу',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Top server participants by balance',
                'ru': 'Лучшие участники сервера по балансу',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True
        },
        {
            'name': 'pay',
            'category': 'economy',
            'aliases': [],
            'arguments': ['<member>', '<amount>'],
            'descriptrion': {
                'en': 'Transfers the specified amount to the selected participant',
                'ru': 'Переводит указанную сумму выбранному участнику',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Transfers money',
                'ru': 'Переводит деньги',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True
        },

        {
            'name': 'daily',
            'category': 'economy',
            'aliases': [],
            'arguments': [],
            'descriptrion': {
                'en': 'Issues a cash reward once a day',
                'ru': 'Выдает денежное вознаграждение один раз в день',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Daily cash rewards',
                'ru': 'Ежедневные денежные вознаграждения',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True
        },
        {
            'name': 'weekly',
            'category': 'economy',
            'aliases': [],
            'arguments': [],
            'descriptrion': {
                'en': 'Issues a cash reward once a week',
                'ru': 'Выдает денежное вознаграждение раз в неделю',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Weekly cash rewards',
                'ru': 'Еженедельные денежные вознаграждения',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True
        },
        {
            'name': 'monthly',
            'category': 'economy',
            'aliases': [],
            'arguments': [],
            'descriptrion': {
                'en': 'Issues a cash reward once a month',
                'ru': 'Выдает денежное вознаграждение раз в месяц',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Monthly cash rewards',
                'ru': 'Ежемесячное денежное вознаграждение',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True
        },

        {
            'name': 'deposit',
            'category': 'economy',
            'aliases': ['dep'],
            'arguments': ['<amount>'],
            'descriptrion': {
                'en': 'Transfers the entered amount of money to the bank protecting your funds from robbery',
                'ru': 'Переводит введенную сумму денег в банк, защищая ваши средства от ограбления',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Transfers the entered amount of money to the bank',
                'ru': 'Переводит введенную сумму денег в банк',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True
        },
        {
            'name': 'withdraw',
            'category': 'economy',
            'aliases': ['wd'],
            'arguments': ['<amount>'],
            'descriptrion': {
                'en': (
                    'Redirects your funds from the bank back to your account\n\n'
                    'Please note that if you lose your funds, it is not possible to return them'
                ),
                'ru': (
                    'Перенаправляет ваши средства из банка обратно на ваш счет\n\n'
                    'Пожалуйста, обратите внимание, что если вы потеряете свои средства, вернуть их будет невозможно'
                ),
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Transfers the amount back to the account',
                'ru': 'Переводит сумму обратно на счет',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True
        },

        {
            'name': 'gift',
            'category': 'economy',
            'aliases': [],
            'arguments': ['[member]', '<amount>'],
            'descriptrion': {
                'en': (
                    'Adds a certain amount to the selected participant\n'
                    'If the participant is not selected, the team performer acts instead'
                ),
                'ru': (
                    'Добавляет определенную сумму выбранному участнику\n'
                    'Если участник не выбран, вместо него действует исполнитель команды'
                ),
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Adds the amount to the participant',
                'ru': 'Добавляет сумму участнику',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True
        },
        {
            'name': 'take',
            'category': 'economy',
            'aliases': [],
            'arguments': ['[member]', '<amount>'],
            'descriptrion': {
                'en': (
                    'Takes a certain amount to the selected participant\n'
                    'If the participant is not selected, the team performer acts instead'
                ),
                'ru': (
                    'Выплачивает определенную сумму выбранному участнику\n'
                    'Если участник не выбран, вместо него действует исполнитель команды'
                ),
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Takes the amount to the participant',
                'ru': 'Возвращает сумму участнику',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True
        },
    ],
    'major': [
        {
            'name': 'help',
            'category': 'major',
            'aliases': [],
            'arguments': ['[command]'],
            'descriptrion': {
                'en': 'A command describing the bot\'s functions',
                'ru': 'Команда, описывающая функции бота',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Current command',
                'ru': 'Текущая команда',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': False,
        },
        {
            'name': 'ping',
            'category': 'major',
            'aliases': [],
            'arguments': [],
            'descriptrion': {
                'en': 'Shows the performance and current status of the bot',
                'ru': 'Показывает производительность и текущее состояние бота',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Current bot delay',
                'ru': 'Текущая задержка бота',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': False,
        },
        {
            'name': 'invite',
            'category': 'major',
            'aliases': [],
            'arguments': [],
            'descriptrion': {
                'en': 'Issues a link inviting the bot to the server',
                'ru': 'Выдает ссылку, приглашающую бота на сервер',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Bot invitation link',
                'ru': 'Ссылка на приглашение бота',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': False,
        },
        {
            'name': 'captcha',
            'category': 'major',
            'aliases': [],
            'arguments': [],
            'descriptrion': {
                'en': 'Shows a picture on which the text is encrypted within 30 seconds the user must solve the captcha',
                'ru': 'Показывает картинку, на которой зашифрован текст, в течение 30 секунд пользователь должен разгадать капчу',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Test command',
                'ru': 'Тестовая команда',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True,
        },
    ],
    'voice': [
        {
            'name': 'join',
            'category': 'voice',
            'aliases': [],
            'arguments': [],
            'descriptrion': {
                'en': 'Enters the channel with the user who called the command',
                'ru': '',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Enters the channel'
            },
            'allowed_disabled': True,
        },
        {
            'name': 'leave',
            'category': 'voice',
            'aliases': [],
            'arguments': [],
            'descriptrion': {
                'en': 'Comes out the channel with the user who called the command',
                'ru': '',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Comes out the channel',
                'ru': '',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True,
        },
        {
            'name': 'play',
            'category': 'voice',
            'aliases': [],
            'arguments': ['<title/url>'],
            'descriptrion': {
                'en': (
                    'Starts playing the music set by the user\n'
                    'As a cloud with music is **Yandex Music**'
                ),
                'ru': '',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Starts playing music',
                'ru': '',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True,
        },
        {
            'name': 'stop',
            'category': 'voice',
            'aliases': [],
            'arguments': [],
            'descriptrion': {
                'en': 'Stops the current music stream',
                'ru': '',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Stops the music',
                'ru': '',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True,
        },
        {
            'name': 'pause',
            'category': 'voice',
            'aliases': [],
            'arguments': [],
            'descriptrion': {
                'en': 'Stops the current music stream in the future which can be continued',
                'ru': '',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Assigns a pause for music',
                'ru': '',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True,
        },
        {
            'name': 'resume',
            'category': 'voice',
            'aliases': [],
            'arguments': [],
            'descriptrion': {
                'en': 'Resumes the music stream that was completed by the necessary means in order to continue in the future',
                'ru': '',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Resumes music',
                'ru': '',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True,
        },
        {
            'name': 'volume',
            'category': 'voice',
            'aliases': [],
            'arguments': ['<volume>'],
            'descriptrion': {
                'en': 'Set the volume to the current music stream from 1 to 100',
                'ru': '',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Sets the volume',
                'ru': '',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True,
        },
    ],
    'moderation': [
        {
            'name': 'purge',
            'category': 'moderation',
            'aliases': [],
            'arguments': [],
            'descriptrion': {
                'en': 'Subcommands that help clean the chat',
                'ru': 'Подкоманды, которые помогают очистить чат',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Commands to clear the chat',
                'ru': 'Команды для очистки чата',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True,
        },
        {
            'name': 'temp-role',
            'category': 'moderation',
            'aliases': [],
            'arguments': ['<member>', '<roles>', '[time]'],
            'descriptrion': {
                'en': (
                    'Adds roles to a certain participant for a while or forever\n'
                    'If the role is not specified, the role will be assigned forever\n'
                    'You can summarize the roles\n'
                    'The time is indicated in the format `1d1h1m1s` the values can be combined and also duplicated, for example `1d2h1d`\n\n'
                    'Example: '
                    'l.temp-role **@lordcode** **@role1** **@role2** _12h_'
                ),
                'ru': (
                    'Добавляет роли определенному участнику на некоторое время или навсегда\n'
                    'Если роль не указана, она будет назначена навсегда\n'
                    'Вы можете суммировать роли\n'
                    'Время указано в формате `1d1h1m1s` значения могут комбинироваться, а также дублироваться, например `1d2h1d`\n\n'
                    'Пример: '
                    'l.temp-role **@lordcode** **@role1** **@role2** _12h_'
                ),
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Adds roles to a certain participant for a while or forever',
                'ru': 'Добавляет роли определенному участнику на некоторое время или навсегда',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True,
        },
        {
            'name': 'temp-role list',
            'category': 'moderation',
            'aliases': [],
            'arguments': ['[member]'],
            'descriptrion': {
                'en': (
                    'Provides a list of temporary roles for the server or member.\n'
                    'If `member` is n2ot specified, it shows a list of all temporary roles on the server.\n'
                    'If specified, it shows only those roles that belong to the participant.\n'
                    'The roles assigned to are always not shown in the list.'
                ),
                'ru': (
                    'Предоставляет список временных ролей для сервера или участника.\n'
                    'Если `member` не указан, то отображается список всех временных ролей на сервере.\n'
                    'Если указано, то отображаются только те роли, которые принадлежат участнику.\n'
                    'Роли назначенные на всегда не отображаются в списке.'
                ),
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Provides a list of temporary roles for the server or member',
                'ru': 'Предоставляет список временных ролей для сервера или участника',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True,
        },
        {
            'name': 'say',
            'category': 'moderation',
            'aliases': [],
            'arguments': ['<text/json>'],
            'descriptrion': {
                'en': (
                    'Sends a message on behalf of the bot using a unique '
                    '[**embed builder**](<https://lordcord.fun/embed-builder>) or plain text'
                ),
                'ru': (
                    'Отправляет сообщение от имени бота, используя уникальный '
                    '[**embed конструктор**](<https://lordcord.fun/embed-builder>) или обычный текст'
                ),
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Sends a message',
                'ru': 'Отправляет сообщение',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': True,
        },
        {
            'name': 'settings',
            'category': 'moderation',
            'aliases': ['set', 'setting'],
            'arguments': [],
            'descriptrion': {
                'en': 'Opens special bot management settings as well as its extensions',
                'ru': 'Открывает специальные настройки управления ботом, а также его расширения',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'brief_descriptrion': {
                'en': 'Opens the bot settings',
                'ru': 'Открывает настройки бота',
                'id': '',
                'da': '',
                'de': '',
                'es': '',
                'fr': '',
                'pl': '',
                'tr': ''
            },
            'allowed_disabled': False,
        },
    ],
}


commands: List[CommandOption] = [com for cat in categories.values()
                                 for com in cat]


class Embed:
    title = {
        'ru': 'Справочник',
        'en': 'Help Book',
        'id': '',
        'da': '',
        'de': '',
        'es': '',
        'fr': '',
        'pl': '',
        'tr': ''
    }

    description = {
        'ru': 'Справка по командам бота',
        'en': 'Help on bot commands',
        'id': '',
        'da': '',
        'de': '',
        'es': '',
        'fr': '',
        'pl': '',
        'tr': ''
    }

    footer = {
        'ru': '[] = Необязательно | <> = Обязательно',
        'en': '[] = Optional | <> = Required',
        'id': '',
        'da': '',
        'de': '',
        'es': '',
        'fr': '',
        'pl': '',
        'tr': ''
    }


class CommandEmbed:
    name = {
        'ru': 'Имя команды',
        'en': 'Command name',
        'id': '',
        'da': '',
        'de': '',
        'es': '',
        'fr': '',
        'pl': '',
        'tr': ''
    }
    category = {
        'ru': 'Категория',
        'en': 'Category',
        'id': '',
        'da': '',
        'de': '',
        'es': '',
        'fr': '',
        'pl': '',
        'tr': ''
    }
    aliases = {
        'ru': 'Псевдонимы',
        'en': 'Aliases',
        'id': '',
        'da': '',
        'de': '',
        'es': '',
        'fr': '',
        'pl': '',
        'tr': ''
    }
    arguments = {
        'ru': 'Аргументы',
        'en': 'Arguments',
        'id': '',
        'da': '',
        'de': '',
        'es': '',
        'fr': '',
        'pl': '',
        'tr': ''
    }
    disable_command = {
        'ru': 'Можно отключить?',
        'en': 'Can I turn it off?',
        'id': '',
        'da': '',
        'de': '',
        'es': '',
        'fr': '',
        'pl': '',
        'tr': ''
    }
    connection_disabled = {
        0: {
            'ru': 'Да',
            'en': 'Yeah',
            'id': '',
            'da': '',
            'de': '',
            'es': '',
            'fr': '',
            'pl': '',
            'tr': ''
        },
        1: {
            'ru': 'Нет',
            'en': 'Nope',
            'id': '',
            'da': '',
            'de': '',
            'es': '',
            'fr': '',
            'pl': '',
            'tr': ''
        }
    }
    description = {
        'ru': 'Описание',
        'en': 'Descriptrion',
        'id': '',
        'da': '',
        'de': '',
        'es': '',
        'fr': '',
        'pl': '',
        'tr': ''
    }


class CommandNotFound:
    title = {
        'en': 'Command Not Found',
        'ru': 'Команда не найдена',
        'id': '',
        'da': '',
        'de': '',
        'es': '',
        'fr': '',
        'pl': '',
        'tr': ''
    }
    description = {
        'en': 'When searching for command, we did not find it, look at it again in the general list of commands',
        'ru': 'При поиске команды мы ее не нашли, посмотрите на нее еще раз в общем списке команд',
        'id': '',
        'da': '',
        'de': '',
        'es': '',
        'fr': '',
        'pl': '',
        'tr': ''
    }


class CommandNotValid:
    title = {
        'en': 'The command is invalid',
        'ru': 'Команда недействительна',
        'id': '',
        'da': '',
        'de': '',
        'es': '',
        'fr': '',
        'pl': '',
        'tr': ''
    }
    description = {
        'en': 'Most likely you entered the name of the team incorrectly, perhaps it contains some strange characters',
        'ru': 'Скорее всего, вы неправильно ввели название команды, возможно, оно содержит какие-то странные символы',
        'id': '',
        'da': '',
        'de': '',
        'es': '',
        'fr': '',
        'pl': '',
        'tr': ''
    }
