
class start:
    description = {
        'ru': 'Взаимодействуйте с выпадающим меню выбора, чтобы настроить сервер.',
        'en': 'Interact with the selection drop-down menu to configure the server.'
    }
    author = {
        'ru': 'Настройка модулей бота.',
        'en': 'Configuring the bot modules.'
    }
    request = {
        'ru': 'Запрос от',
        'en': 'Request from'
    }
    choose = {
        'en': 'Choose settings...',
        'ru': 'Выберите настройки...'
    }


class module_name:
    economy = {
        'en': "Economy",
        'ru': "Экономика"
    }
    languages = {
        'en': "Languages",
        'ru': "Языки"
    }
    prefix = {
        'en': "Prefix",
        'ru': "Префикс"
    }
    color = {
        'en': "Color of system messages",
        'ru': "Цвет системных сообщений"
    }
    reactions = {
        'en': "Auto Reactionsⁿᵉʷ",
        'ru': "Автоматические реакцииⁿᵉʷ"
    }
    translate = {
        'en': "Auto Translateⁿᵉʷ",
        'ru': "Автоматический переводⁿᵉʷ"
    }
    thread = {
        'en': "Auto message in a thread/postⁿᵉʷ",
        'ru': "Автоматическое сообщение в ветке/постеⁿᵉʷ"
    }
    disabled_commands = {
        'en': 'Command switch',
        'ru': 'Командный переключатель'
    }
    command_permission = {
        'en': 'Command Settings',
        'ru': 'Настройки команды'
    }
    ideas = {
        'en': 'Ideas',
        'ru': 'Идеи'
    }

    welcomer = {
        'en': 'Welcome new members',
        'ru': 'Приветствие новых участников'
    }
    auto_roles = {
        'en': 'Automatic roles',
        'ru': 'Автоматические роли'
    }


class button:
    back = {
        'ru': 'Назад',
        'en': 'Back'
    }
    edit = {
        'ru': 'Изменить',
        'en': 'Edit'
    }
    reset = {
        'ru': 'Сбросить',
        'en': 'Reset'
    }
    add = {
        'ru': 'Добавить',
        'en': 'Add'
    }


class prefix:
    title = {
        'ru': 'Префикс',
        'en': 'Prefix'
    }
    description = {
        'ru': 'Установка префикса, на который бот будет реагировать при вызове команды.',
        'en': 'Setting the prefix to which the bot will respond when calling the command.'
    }
    current = {
        'ru': 'Текущий префикс',
        'en': 'Current prefix'
    }


class languages:
    title = {
        'ru': 'Язык',
        'en': 'Language'
    }
    description = {
        'ru': 'Эта настройка изменяет язык для работы с ботом. Выберите язык сервера.',
        'en': 'This setting changes the language for working with the bot. Select the server language.'
    }
    choose = {
        'ru': 'Выберите язык для сервера:',
        'en': 'Select the language for the server:'
    }


class color:
    title = {
        'ru': 'Цвет системных сообщений',
        'en': 'Color of system messages'
    }
    description = {
        'ru': (
            'Когда вы используете команды, бот отображает вставки, которые по умолчанию имеют невидимый цвет.'
            '\n\n'
            'Вы можете установить свой цвет в соответствии с тематикой вашего сообщества.'
        ),
        'en': (
            'When you use commands, the bot displays inserts that have an invisible color by default.'
            '\n\n'
            'You can set your color according to the theme of your community.'
        )
    }
    current = {
        'ru': 'Текущий цвет',
        'en': 'Current color'
    }


class auto_role:
    install = {
        'en': 'Install roles',
        'ru': 'Установить роли'
    }
    embed_title = {
        'en': 'Automatic roles',
        'ru': 'Автоматические роли'
    }
    embed_description = {
        'en': (
            'The control panel for automatic roles.\n'
            'You can install, edit, delete, and view such actions from the panel.\n'
            'If you do not see the auto roles, then they are not selected!'
        ),
        'ru': (
            'Панель управления автоматическими ролями.\n'
            'Вы можете устанавливать, редактировать, удалять и просматривать такие действия с панели.\n'
            'Если вы не видите автоматические правила, значит, они не выбраны!'
        )
    }
    embed_field = {
        'en': 'Selected roles:',
        'ru': 'Выбранные роли:'
    }


class welcome:
    embed_title = {
        'en': 'Message greeting',
        'ru': 'Сообщение приветствие'
    }
    embed_description = {
        'en': (
            'Automatic sending of messages when a participant logs on to the server'
            '\n\n'
            'If you want to change the channel, just select it again and set the message'
            '\n\n'
            'To change a message, select the current channel and set a new message for it'
        ),
        'ru': (
            'Автоматическая отправка сообщений при входе участника на сервер'
            '\n\n'
            'Если вы хотите сменить канал, просто выберите его еще раз и установите сообщение'
            '\n\n'
            'Чтобы изменить сообщение, выберите текущий канал и установите для него новое сообщение'
        )
    }

    field_successful = {
        'en': 'Installed channel',
        'ru': 'Установленный канал'
    }
    field_failure = {
        'en': 'The channel is not installed',
        'ru': 'Канал не установлен'
    }

    button_delete = {
        'en': 'Delete message',
        'ru': 'Удалить сообщение'
    }
    button_view = {
        'en': 'View message',
        'ru': 'Просмотреть сообщение'
    }
    button_install = {
        'en': 'Install message',
        'ru': 'Установить сообщение'
    }

    dropdown_placeholder = {
        'en': 'Select the welcome channel',
        'ru': 'Выберите канал приветствия'
    }

    modal_title = {
        'en': 'Message greeting',
        'ru': 'Сообщение приветствие'
    }
    modal_label = {
        'en': 'Message',
        'ru': 'Сообщение'
    }
    modal_placeholder = {
        'en': 'You can also use embed builder',
        'ru': 'Вы также можете использовать embed builder'
    }


class economy:
    pass


class disabled_commands:
    title = {
        'en': 'Command switch',
        'ru': 'Командный переключатель'
    }
    description = {
        'en': 'Disables/Enables commands built into the bot',
        'ru': 'Отключает/Включает команды, встроенные в бота'
    }
    placeholder = {
        'en': 'Select the commands you want to disable on the server',
        'ru': 'Выберите команды, которые вы хотите отключить на сервере'
    }
    embed_title = {
        'en': 'Disabled commands',
        'ru': 'Отключенные команды'
    }
    embed_description_list = {
        'en': 'New list of disabled commands:',
        'ru': 'Новый список отключенных команд:'
    }
    embed_description_no_disabled = {
        'en': 'All commands are enabled',
        'ru': 'Все команды включены'
    }
