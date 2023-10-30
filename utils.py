def generate_message(content):
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

def check_invite(content):
    regex_string = '(https:\/\/discord.gg\/|https:\/\/discord.com\/invite\/)([a-zA-Z0-9_-]+)(\/|\s|\?|$)'
    pattern = re.fullmatch(regex_string,content)
    if pattern:
        return pattern.groups()[1]

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

class ErrorTypeChannel(Exception):
    pass
