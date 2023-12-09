
class init_embed:
    title = {
        'en':'The Participant Welcome module',
        'ru':'Модуль приветствия участника'
    }
    description = {
        'en':'A module that is equipped with an automatic greeting and roles',
        'ru':'Модуль, оснащенный автоматическим приветствием и ролями'
    }

class init_dropdown:
    welcome_label = {
        'en':'Welcome new members',
        'ru':'Приветствие новых участников'
    }
    roles_label = {
        'en':'Automatic roles',
        'ru':'Автоматические роли'
    }
    placeholder = {
        'en':'Define the greeting setting:',
        'ru':'Определите настройки приветствия:'
    }

class role: 
    install = {
        'en':'Install roles',
        'ru':'Установить роли'
    }
    embed_title = {
        'en':'Automatic roles',
        'ru':'Автоматические роли'
    }
    embed_description = {
        'en':(
            'The control panel for automatic roles.\n'
            'You can install, edit, delete, and view such actions from the panel.\n'
            'If you do not see the auto roles, then they are not selected!'
        ),
        'ru':(
            'Панель управления автоматическими ролями.\n'
            'Вы можете устанавливать, редактировать, удалять и просматривать такие действия с панели.\n'
            'Если вы не видите автоматические правила, значит, они не выбраны!'
        )
    }
    embed_field = {
        'en':'Selected roles:',
        'ru':'Выбранные роли:'
    }

class welcome:
    embed_title = {
        'en':'Message greeting',
        'ru':'Сообщение приветствие'
    }
    embed_description = {
        'en':(
            'Automatic sending of messages when a participant logs on to the server'
            '\n\n'
            'If you want to change the channel, just select it again and set the message'
            '\n\n'
            'To change a message, select the current channel and set a new message for it'
        ),
        'ru':(
            'Автоматическая отправка сообщений при входе участника на сервер'
            '\n\n'
            'Если вы хотите сменить канал, просто выберите его еще раз и установите сообщение'
            '\n\n'
            'Чтобы изменить сообщение, выберите текущий канал и установите для него новое сообщение'
        )
    }
    
    field_successful = {
        'en':'Installed channel',
        'ru':'Установленный канал'
    }
    field_failure = {
        'en':'The channel is not installed',
        'ru':'Канал не установлен'
    }
    
    button_delete = {
        'en':'Delete message',
        'ru':'Удалить сообщение'
    }
    button_view = {
        'en':'View message',
        'ru':'Просмотреть сообщение'
    }
    button_install = {
        'en':'Install message',
        'ru':'Установить сообщение'
    }
    
    dropdown_placeholder = {
        'en':'Select the welcome channel',
        'ru':'Выберите канал приветствия'
    }
    
    modal_title = {
        'en':'Message greeting',
        'ru':'Сообщение приветствие'
    }
    modal_label = {
        'en':'Message',
        'ru':'Сообщение'
    }
    modal_placeholder = {
        'en':'You can also use embed builder',
        'ru':'Вы также можете использовать embed builder'
    }