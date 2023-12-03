
class start:
    description = {
        'ru':'Взаимодействуйте с выпадающим меню выбора, чтобы настроить сервер.',
        'en':'Interact with the selection drop-down menu to configure the server.'
    }
    author = {
        'ru':'Настройка модулей бота.',
        'en':'Configuring the bot modules.'
    }
    request = {
        'ru':'Запрос от',
        'en':'Request from'
    }

class module_name:
    economy = {
        'en':"Economy",
        'ru':"Экономика"
    }
    languages = {
        'en':"Languages",
        'ru':"Языки"
    }
    prefix = {
        'en':"Prefix",
        'ru':"Префикс"
    }
    color = {
        'en':"Color of system messages",
        'ru':"Цвет системных сообщений"
    }
    reactions = {
        'en':"Auto Reactionsⁿᵉʷ",
        'ru':"Автоматические реакцииⁿᵉʷ"
    }
    translate = {
        'en':"Auto Translateⁿᵉʷ",
        'ru':"Автоматический переводⁿᵉʷ"
    }
    thread = {
        'en':"Auto message in a thread/postⁿᵉʷ",
        'ru':"Автоматическое сообщение в ветке/постеⁿᵉʷ"
    }
    disabled_commands = {
        'en':'Command switch',
        'ru':'Командный переключатель'
    }
    greeting = {
        'en':'Greeting',
        'ru':'Приветствие'
    }

class button:
    back = {
        'ru':'Назад',
        'en':'Back'
    }
    edit = {
        'ru':'Изменить',
        'en':'Edit'
    }
    reset = {
        'ru':'Сбросить',
        'en':'Reset'
    }
    add = {
        'ru':'Добавить',
        'en':'Add'
    }


class prefix:
    title = {
        'ru':'Префикс',
        'en':'Prefix'
    }
    description = {
        'ru':'Установка префикса, на который бот будет реагировать при вызове команды.',
        'en':'Setting the prefix to which the bot will respond when calling the command.'
    }
    current = {
        'ru':'Текущий префикс',
        'en':'Current prefix'
    }

class languages:
    title = {
        'ru':'Язык',
        'en':'Language'
    }
    description = {
        'ru':'Эта настройка изменяет язык для работы с ботом. Выберите язык сервера.',
        'en':'This setting changes the language for working with the bot. Select the server language.'
    }
    choose = {
        'ru':'Выберите язык для сервера:',
        'en':'Select the language for the server:'
    }

class color:
    title = {
        'ru':'Цвет системных сообщений',
        'en':'Color of system messages'
    }
    description = {    
        'ru':(
            'Когда вы используете команды, бот отображает вставки, которые по умолчанию имеют невидимый цвет.'
            '\n\n'
            'Вы можете установить свой цвет в соответствии с тематикой вашего сообщества.'
        ),
        'en':(
            'When you use commands, the bot displays inserts that have an invisible color by default.'
            '\n\n'
            'You can set your color according to the theme of your community.'
        )
    }
    current = {
        'ru':'Текущий цвет',
        'en':'Current color'
    }



class economy:
    pass


class disabled_commands:
    title = {
        'en':'Command switch',
        'ru':'Командный переключатель'
    }
    description = {
        'en':'Disables/Enables commands built into the bot',
        'ru':'Отключает/Включает команды, встроенные в бота'
    }
    placeholder = {
        'en':'Select the commands you want to disable on the server',
        'ru':'Выберите команды, которые вы хотите отключить на сервере'
    }
    embed_title = {
        'en':'Disabled commands',
        'ru':'Отключенные команды'
    }
    embed_description_list = {
        'en':'New list of disabled commands:',
        'ru':'Новый список отключенных команд:'
    }
    embed_description_no_disabled = {
        'en':'All commands are enabled',
        'ru':'Все команды включены'
    }
