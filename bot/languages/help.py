from typing import List, Dict, Literal, Union

possible_args = Literal['name','category','aliases','arguments','descriptrion','brief_descriptrion','allowed_disabled']
CommandOption = Dict[
    possible_args,
    Union[dict,list,bool,str]
]   

categories_emoji = {
    'economy':'💎',
    'major':'👑',
    'moderation':'⚠',
}

categories_name = {
    'economy':{
        'ru':'Экономика',
        'en':'Economy'
    },
    'major':{
        'ru':'Главное',
        'en':'Major'
    },
    'moderation':{
        'ru':'Модерационные',
        'en':'Moderation'
    },
}

categories: Dict[str,List[CommandOption]] = {
    'economy':[
        {
            'name':'balance',
            'category':'economy',
            'aliases':['bal'],
            'arguments':['[member]'],
            'descriptrion':{
                'en':(
                    'Displays the participant\'s balance as well as possible rewards that can be collected'
                    '\n\n'
                    'If no participant is specified, the value is taken by the one who started the command'
                ),
                'ru':(
                    'Отображает баланс участника, а также возможные вознаграждения, которые можно получить'
                    '\n\n'
                    'Если участник не указан, значение принимает тот, кто запустил команду'
                )
            },
            'brief_descriptrion':{
                'en':'Participant\'s balance',
                'ru':'Баланс участника'
            },
            'allowed_disabled':True
        },
        {
            'name':'leaderboard',
            'category':'economy',
            'aliases':[],
            'arguments':[],
            'descriptrion':{
                'en':'Shows statistics of the top 10 server participants by balance',
                'ru':'Показывает статистику по 10 лучшим участникам сервера по балансу'
            },
            'brief_descriptrion':{
                'en':'Top server participants by balance',
                'ru':'Лучшие участники сервера по балансу'
            },
            'allowed_disabled':True
        },
        {
            'name':'pay',
            'category':'economy',
            'aliases':[],
            'arguments':['<member>','<amount>'],
            'descriptrion':{
                'en':'Transfers the specified amount to the selected participant',
                'ru':'Переводит указанную сумму выбранному участнику'
            },
            'brief_descriptrion':{
                'en':'Transfers money',
                'ru':'Переводит деньги'
            },
            'allowed_disabled':True
        },
        
        {
            'name':'daily',
            'category':'economy',
            'aliases':[],
            'arguments':[],
            'descriptrion':{
                'en':'Issues a cash reward once a day',
                'ru':'Выдает денежное вознаграждение один раз в день'
            },
            'brief_descriptrion':{
                'en':'Daily cash rewards',
                'ru':'Ежедневные денежные вознаграждения'
            },
            'allowed_disabled':True
        },    
        {
            'name':'weekly',
            'category':'economy',
            'aliases':[],
            'arguments':[],
            'descriptrion':{
                'en':'Issues a cash reward once a week',
                'ru':'Выдает денежное вознаграждение раз в неделю'
            },
            'brief_descriptrion':{
                'en':'Weekly cash rewards',
                'ru':'Еженедельные денежные вознаграждения'
            },
            'allowed_disabled':True
        },    
        {
            'name':'monthly',
            'category':'economy',
            'aliases':[],
            'arguments':[],
            'descriptrion':{
                'en':'Issues a cash reward once a month',
                'ru':'Выдает денежное вознаграждение раз в месяц'
            },
            'brief_descriptrion':{
                'en':'Monthly cash rewards',
                'ru':'Ежемесячное денежное вознаграждение'
            },
            'allowed_disabled':True
        },  
        
        {
            'name':'deposit',
            'category':'economy',
            'aliases':['dep'],
            'arguments':['<amount>'],
            'descriptrion':{
                'en':'Transfers the entered amount of money to the bank protecting your funds from robbery',
                'ru':'Переводит введенную сумму денег в банк, защищая ваши средства от ограбления'
            },
            'brief_descriptrion':{
                'en':'Transfers the entered amount of money to the bank',
                'ru':'Переводит введенную сумму денег в банк'
            },
            'allowed_disabled':True
        },        
        {
            'name':'withdraw',
            'category':'economy',
            'aliases':['wd'],
            'arguments':['<amount>'],
            'descriptrion':{
                'en':(
                    'Redirects your funds from the bank back to your account'
                    '\n\n'
                    'Please note that if you lose your funds, it is not possible to return them'
                ),
                'ru':(
                    'Перенаправляет ваши средства из банка обратно на ваш счет'
                    '\n\n'
                    'Пожалуйста, обратите внимание, что если вы потеряете свои средства, вернуть их будет невозможно'
                ),
            },
            'brief_descriptrion':{
                'en':'Transfers the amount back to the account',
                'ru':'Переводит сумму обратно на счет'
            },
            'allowed_disabled':True
        },   
        
        {
            'name':'gift',
            'category':'economy',
            'aliases':[],
            'arguments':['[member]','<amount>'],
            'descriptrion':{
                'en':(
                    'Adds a certain amount to the selected participant\n'
                    'If the participant is not selected, the team performer acts instead'
                ),
                'ru':(
                    'Добавляет определенную сумму выбранному участнику\n'
                    'Если участник не выбран, вместо него действует исполнитель команды'
                )
            },
            'brief_descriptrion':{
                'en':'Adds the amount to the participant',
                'ru':'Добавляет сумму участнику'
            },
            'allowed_disabled':True
        },   
        {
            'name':'take',
            'category':'economy',
            'aliases':[],
            'arguments':['[member]','<amount>'],
            'descriptrion':{
                'en':(
                    'Takes a certain amount to the selected participant\n'
                    'If the participant is not selected, the team performer acts instead'
                ),
                'ru':(
                    'Выплачивает определенную сумму выбранному участнику\n'
                    'Если участник не выбран, вместо него действует исполнитель команды'
                )
            },
            'brief_descriptrion':{
                'en':'Takes the amount to the participant',
                'ru':'Возвращает сумму участнику'
            },
            'allowed_disabled':True
        },     
    ],
    'major':[
        {
            'name':'help',
            'category':'major',
            'aliases':[],
            'arguments':['[command]'],
            'descriptrion':{
                'en':'A command describing the bot\'s functions',
                'ru':'Команда, описывающая функции бота'
            },
            'brief_descriptrion':{
                'en':'Current command',
                'ru':'Текущая команда'
            },
            'allowed_disabled':False,
        },  
        {
            'name':'ping',
            'category':'major',
            'aliases':[],
            'arguments':[],
            'descriptrion':{
                'en':'Shows the performance and current status of the bot',
                'ru':'Показывает производительность и текущее состояние бота'
            },
            'brief_descriptrion':{
                'en':'Current bot delay',
                'ru':'Текущая задержка бота'
            },
            'allowed_disabled':False,
        },  
        {
            'name':'captcha',
            'category':'major',
            'aliases':[],
            'arguments':[],
            'descriptrion':{
                'en':'Shows a picture on which the text is encrypted within 30 seconds the user must solve the captcha',
                'ru':'Показывает картинку, на которой зашифрован текст, в течение 30 секунд пользователь должен разгадать капчу'
            },
            'brief_descriptrion':{
                'en':'Test command',
                'ru':'Тестовая команда'
            },
            'allowed_disabled':True,
        },  
    ],
    'moderation':[
        {
            'name':'purge',
            'category':'moderation',
            'aliases':[],
            'arguments':[],
            'descriptrion':{
                'en':'Subcommands that help clean the chat',
                'ru':'Подкоманды, которые помогают очистить чат'
            },
            'brief_descriptrion':{
                'en':'Commands to clear the chat',
                'ru':'Команды для очистки чата'
            },
            'allowed_disabled':True,
        },  
        {
            'name':'temp-role',
            'category':'moderation',
            'aliases':[],
            'arguments':['<member>', '<roles>', '[time]'],
            'descriptrion':{
                'en':(
                    'Adds roles to a certain participant for a while or forever\n'
                    'If the role is not specified, the role will be assigned forever\n'
                    'You can summarize the roles\n'
                    'The time is indicated in the format `1d1h1m1s` the values can be combined and also duplicated, for example `1d2h1d`\n\n'
                    'Example: '
                    'l.temp-role **@lordcode** **@role1** **@role2** _12h_'
                ),
                'ru':(
                    'Добавляет роли определенному участнику на некоторое время или навсегда\n'
                    'Если роль не указана, она будет назначена навсегда\n'
                    'Вы можете суммировать роли\n'
                    'Время указано в формате `1d1h1m1s` значения могут комбинироваться, а также дублироваться, например `1d2h1d`\n\n'
                    'Пример: '
                    'l.temp-role **@user** **@role1** **@role2** _12h_'
                )
            },
            'brief_descriptrion':{
                'en':'Adds roles to a certain participant for a while or forever',
                'ru':'Добавляет роли определенному участнику на некоторое время или навсегда'
            },
            'allowed_disabled':True,
        },
        {
            'name':'temp-role list',
            'category':'moderation',
            'aliases':[],
            'arguments':['[member]'],
            'descriptrion':{
                'en':(
                    'Provides a list of temporary roles for the server or member.\n'
                    'If `member` is n2ot specified, it shows a list of all temporary roles on the server.\n'
                    'If specified, it shows only those roles that belong to the participant.\n'
                    'The roles assigned to are always not shown in the list.'
                ),
                'ru':(
                    'Предоставляет список временных ролей для сервера или участника.\n'
                    'Если `member` не указан, то отображается список всех временных ролей на сервере.\n'
                    'Если указано, то отображаются только те роли, которые принадлежат участнику.\n'
                    'Назначенные роли всегда не отображаются в списке.'
                )
            },
            'brief_descriptrion':{
                'en':'Provides a list of temporary roles for the server or member',
                'ru':'Предоставляет список временных ролей для сервера или участника'
            },
            'allowed_disabled':True,
        },
        {
            'name':'say',
            'category':'moderation',
            'aliases':[],
            'arguments':['<text/json>'],
            'descriptrion':{
                'en':(
                    'Sends a message on behalf of the bot using a unique '
                    '[**embed builder**](<https://lordcord.fun/embed-builder>) or plain text'
                ),
                'ru':(
                    'Отправляет сообщение от имени бота, используя уникальный '
                    '[**embed конструктор**](<https://lordcord.fun/embed-builder>) или обычный текст'
                )
            },
            'brief_descriptrion':{
                'en':'Sends a message',
                'ru':'Отправляет сообщение'
            },
            'allowed_disabled':True,
        }, 
        {
            'name':'settings',
            'category':'moderation',
            'aliases':['set','setting'],
            'arguments':[],
            'descriptrion':{
                'en':'Opens special bot management settings as well as its extensions',
                'ru':'Открывает специальные настройки управления ботом, а также его расширения'
            }
            ,
            'brief_descriptrion':{
                'en':'Opens the bot settings',
                'ru':'Открывает настройки бота'
            },
            'allowed_disabled':False,
        }, 
    ],
}


commands: List[CommandOption] = [com for cat in categories.values() for com in cat]

class Embed:
    title = {
        'ru':'Справочник',
        'en':'Help Book'
    }
    
    description = {
        'ru':'Справка по командам бота',
        'en':'Help on bot commands'
    }
    
    footer = {
        'ru':'[] = Необязательно | <> = Обязательно',
        'en':'[] = Optional | <> = Required'
    }

class CommandEmbed:
    name = {
        'ru':'Имя команды',
        'en':'Command name'
    }
    category  = {
        'ru':'Категория',
        'en':'Category'
    }
    aliases = {
        'ru':'Псевдонимы',
        'en':'Aliases'
    }
    arguments = {
        'ru':'Аргументы',
        'en':'Arguments'
    }
    disable_command = {
        'ru':'Можно отключить?',
        'en':'Can I turn it off?'
    }
    connection_disabled = {
        True:{
            'ru':'Да',
            'en':'Yeah'
        },
        False:{
            'ru':'Нет',
            'en':'Nope'
        }
    }
    description = {
        'ru':'Описание',
        'en':'Descriptrion'
    }

class CommandNotFound:
    title = {
        'en':'Command Not Found',
        'ru':'Команда не найдена'
    }
    description = {
        'en':'When searching for command, we did not find it, look at it again in the general list of commands',
        'ru':'При поиске команды мы ее не нашли, посмотрите на нее еще раз в общем списке команд'
    }

class CommandNotValid:
    title = {
        'en':'The command is invalid',
        'ru':'Команда недействительна'
    }
    description = {
        'en':'Most likely you entered the name of the team incorrectly, perhaps it contains some strange characters',
        'ru':'Скорее всего, вы неправильно ввели название команды, возможно, оно содержит какие-то странные символы'
    }
