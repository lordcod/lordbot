DEFAULT_PREFIX = 'l.'
DEFAULT_COLOR = 1974050

activities_list = [
    {'id':880218394199220334,'label':'Watch Together','max_user':'Unlimited'},
    {'id':755827207812677713,'label':'Poker Night','max_user':'25'},
    {'id':832012774040141894,'label':'Chess In The Park','max_user':'Unlimited'},
    {'id':902271654783242291,'label':'Sketch Heads','max_user':'16'},
    {'id':879863686565621790,'label':'Letter League','max_user':'8'},
    {'id':832013003968348200,'label':'Checkers In The Park','max_user':'Unlimited'},
    {'id':832025144389533716,'label':'Blazing 8s','max_user':'8'},
    {'id':945737671223947305,'label':'Putt Party','max_user':'Unlimited'},
    {'id':903769130790969345,'label':'Land-io','max_user':'16'},
    {'id':947957217959759964,'label':'Bobble League','max_user':'8'},
    {'id':1007373802981822582,'label':'Gartic Phone','max_user':'16'},
    {'id':1039835161136746497,'label':'Color Together','max_user':'100'},
    {'id':1070087967294631976,'label':'Jamspace Whiteboard','max_user':'Unlimited'},
    {'id':1037680572660727838,'label':'Chef Showdown','max_user':'15'},
    {'id':1107689944685748377,'label':'Bobble Bash','max_user':'8'},
]

invite_link = (
    'https://discord.com/api/oauth2/authorize'
    '?client_id=1095713975532007434'
    '&permissions=-1'
    '&scope=bot%20applications.commands'
    # '&response_type=code'
    # '&redirect_uri=https://lordbot.ru/link-role-callback'
)

categories = {
    'Economy':[
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
    'Major':[
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
    'Moderation':[
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

footer = '[] = Optional | <> = Required'