import nextcord,string,random,re
from captcha.image import ImageCaptcha
from io import BytesIO
from PIL import Image

async def get_webhook(channel: nextcord.TextChannel) -> nextcord.Webhook:
    if channel.type.value not in [0,2,5,13]:
        raise ErrorTypeChannel("Channel error")
    webhooks = await channel.webhooks()
    for wh in webhooks:
        if wh.user==bot.user:
            return wh
    else:
        wh = await channel.create_webhook(name=bot.user.global_name,avatar=bot.user.avatar)
        return wh

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
    text = "".join([random.choice(string.ascii_uppercase) for i in range(num)])
    image = ImageCaptcha(width = 280, height = 90)
    captcha_image = ImageCaptcha(
        width=400,
        height=220,
        fonts=[
            'SF-Pro',
            'SF-Compact-Rounded-Black',
            'SF-Pro-UltraLightItalic',
            'Neoneon'
        ],
        font_sizes=(40,70,100)
    )
    data:BytesIO = image.generate(text)
    return data,text