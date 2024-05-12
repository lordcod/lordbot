import os
from pprint import pprint

import nextcord

token = os.environ['lordcord_token']
client = nextcord.Client()


@client.event
async def on_ready():
    _guild_list = {}
    for guild in client.guilds:
        _guild_list[guild.member_count] = guild

    pprint(dict(sorted(_guild_list.items(),
           key=lambda item: item[0], reverse=False)))

    await client.close()

client.run(token)
