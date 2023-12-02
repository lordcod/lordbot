
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

categories = {
    'economy':[
        {
            'name':'balance',
            'aliases':['bal'],
            'arguments':['[member]'],
            'descriptrion':(
                'Displays the participant\'s balance as well as possible rewards that can be collected'
                '\n\n'
                'If no participant is specified, the value is taken by the one who started the command'
            ),
            'brief_descriptrion':'Participant\'s balance',
            'allowed_disabled':True
        },
        
        {
            'name':'daily',
            'aliases':[],
            'arguments':[],
            'descriptrion':'Issues a cash reward once a day',
            'brief_descriptrion':'Daily cash rewards',
            'allowed_disabled':True
        },    
        {
            'name':'weekly',
            'aliases':[],
            'arguments':[],
            'descriptrion':'Issues a cash reward once a week',
            'brief_descriptrion':'Weekly cash rewards',
            'allowed_disabled':True
        },    
        {
            'name':'monthly',
            'aliases':[],
            'arguments':[],
            'descriptrion':'Issues a cash reward once a month',
            'brief_descriptrion':'Monthly cash rewards',
            'allowed_disabled':True
        },  
        
        {
            'name':'deposit',
            'aliases':['dep'],
            'arguments':['<amount>'],
            'descriptrion':'Transfers the entered amount of money to the bank protecting your funds from robbery',
            'brief_descriptrion':'Transfers the entered amount of money to the bank',
            'allowed_disabled':True
        },        
        {
            'name':'withdraw',
            'aliases':['wd'],
            'arguments':['<amount>'],
            'descriptrion':(
                'Redirects your funds from the bank back to your account'
                '\n\n'
                'Please note that if you lose your funds, it is not possible to return them'
            ),
            'brief_descriptrion':'Transfers the amount back to the account',
            'allowed_disabled':True
        },   
        
        {
            'name':'pay' ,
            'aliases':[],
            'arguments':['<member>','<amount>'],
            'descriptrion':'Transfers the specified amount to the selected participant',
            'brief_descriptrion':'Transfers money',
            'allowed_disabled':True
        },
        
        {
            'name':'gift' ,
            'aliases':[],
            'arguments':['[member]','<amount>'],
            'descriptrion':(
            'Adds a certain amount to the selected participant\n'
            'If the participant is not selected, the team performer acts instead'
            ),
            'brief_descriptrion':'Adds the amount to the participant',
            'allowed_disabled':True
        },   
        {
            'name':'take' ,
            'aliases':[],
            'arguments':['[member]','<amount>'],
            'descriptrion':(
            'Takes a certain amount to the selected participant\n'
            'If the participant is not selected, the team performer acts instead'
            ),
            'brief_descriptrion':'Takes the amount to the participant',
            'allowed_disabled':True
        },     
    ],
    'major':[
        {
            'name':'help',
            'aliases':[],
            'arguments':['[command/category]'],
            'descriptrion':'A command describing the bot\'s functions',
            'brief_descriptrion':'Current command',
            'allowed_disabled':False,
        },  
        {
            'name':'ping',
            'aliases':[],
            'arguments':[],
            'descriptrion':'Shows the performance and current status of the bot',
            'brief_descriptrion':'Current bot delay',
            'allowed_disabled':False,
        },  
        {
            'name':'captcha',
            'aliases':[],
            'arguments':[],
            'descriptrion':'Shows a picture on which the text is encrypted within 30 seconds the user must solve the captcha',
            'brief_descriptrion':'Test command',
            'allowed_disabled':True,
        },  
    ],
    'moderation':[
        {
            'name':'purge',
            'aliases':[],
            'arguments':[],
            'descriptrion':'Subcommands that help clean the chat',
            'brief_descriptrion':'Several sub commands',
            'allowed_disabled':True,
        },  
        {
            'name':'say',
            'aliases':[],
            'arguments':['<text/json>'],
            'descriptrion':'Sends a message on behalf of the bot using a unique [**embed builder**](<https://lordbot.ru/embed-builder>) or plain text',
            'brief_descriptrion':'Sends a message',
            'allowed_disabled':True,
        }, 
        {
            'name':'settings',
            'aliases':['set','setting'],
            'arguments':[],
            'descriptrion':'Opens special bot management settings as well as its extensions',
            'brief_descriptrion':'Opens the bot settings',
            'allowed_disabled':False,
        }, 
    ],
}

commands = [com for cat in categories.values() for com in cat]


footer = {
    'ru':'[] = Необязательно | <> = Обязательно',
    'en':'[] = Optional | <> = Required'
}
