import nextcord

token = "MTE3MzIwNDIzMTc3MjE4ODcyNA.GrExcU.IJKVMcndr6ArG4lusC_si9J2x24HDAUG1fro5A"

client = nextcord.Client(intents=nextcord.Intents.all())


async def clone_message(message: nextcord.Message) -> dict:
    content = message.content
    embeds = message.embeds

    files = []
    for attach in message.attachments:
        filebytes = await attach.read()
        files.append(nextcord.File(
            fp=filebytes,
            filename=attach.filename,
            description=attach.description,
            spoiler=attach.is_spoiler()
        ))

    return {
        "content": content,
        "embeds": embeds,
        "files": files
    }

reaction_data_ch = {
    1153047978769133568: 1210941887108743218,
    1153051615121649896: 1210945846296846346,
    1211220580670373919: 1211220639634034699,
    1212086116031660072: 1212086745479520386
}


@client.event
async def on_ready():
    print("Start client as {}".format(client.user))


@client.event
async def on_message(message: nextcord.Message):
    if message.content != "bot.shutdown" or message.author.id != 636824998123798531:
        return
    await client.close()


@client.event
async def on_raw_reaction_add(payload: nextcord.RawReactionActionEvent):
    if payload.channel_id not in reaction_data_ch:
        return

    guild = client.get_guild(payload.guild_id)
    channel = guild.get_channel(payload.channel_id)
    try:
        message = await channel.fetch_message(payload.message_id)
    except nextcord.HTTPException:
        return

    for react in message.reactions:
        if str(react.emoji) == str(payload.emoji):
            reaction = react
            break
    else:
        return

    if reaction.count > 1:
        return
    if reaction.emoji != "✅":
        return

    message_data = await clone_message(reaction.message)
    channel = reaction.message.guild.get_channel(
        reaction_data_ch[reaction.message.channel.id])
    await channel.send(**message_data)


if __name__ == "__main__":
    client.run(token)
