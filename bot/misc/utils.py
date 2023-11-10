import nextcord,string,random,re,orjson
from captcha.image import ImageCaptcha
from bot.resources import errors
from io import BytesIO
from PIL import Image

async def get_webhook(channel: nextcord.TextChannel, user) -> nextcord.Webhook:
    if channel.type.value not in [0,2,5,13]:
        raise  errors.ErrorTypeChannel("Channel error")
    
    webhooks = await channel.webhooks()
    for wh in webhooks:
        if wh.user==user:
            return wh
    else:
        wh = await channel.create_webhook(name=user.name)
        return wh

def is_builtin_class_instance(obj):
    return obj in (str, int, float, bool)

def clord(value,cls,default=None):
        print('MISC',1)
        if type(value) == cls:
            return value
        print('MISC',2)
        print(is_builtin_class_instance(cls))
        if not is_builtin_class_instance(cls):
            return default
        print('MISC',3)
        try:
            print('MISC',4)
            return cls(value)
        except:
            print('MISC',5)
            return default

async def generate_message(content):
    message = {}
    try:
        content = orjson.loads(content)
        
        message['embeds'] = []
        if "embeds" in content and type(content["embeds"]) == dict:
            for em in content["embeds"]:
                nextcord.Embed.from_dict(em)
        
        if "content" in message:
            message['content'] = content['content']
        
        if "flags" in message:
            message['flag'] = nextcord.MessageFlags()
            message['flag'].value = content["flags"]
    except orjson.JSONDecodeError:
        message['content'] = content
    return message

async def check_invite(content):
    regex_string = '(https:\/\/discord.gg\/|https:\/\/discord.com\/invite\/)([a-zA-Z0-9_-]+)(\/|\s|\?|$)'
    pattern = re.fullmatch(regex_string,content)
    if pattern:
        return pattern.groups()[1]

async def generator_captcha(num):
    text = "".join([random.choice(string.ascii_uppercase) for _ in range(num)])
    captcha_image = ImageCaptcha(
        width=400,
        height=220,
        font_sizes=(40,70,100)
    )
    data:BytesIO = captcha_image.generate(text)
    return data,text
