import nextcord
token = "MTE3MzIwNDIzMTc3MjE4ODcyNA.GrExcU.IJKVMcndr6ArG4lusC_si9J2x24HDAUG1fro5A"

client = nextcord.Client(intents=nextcord.Intents.all())


@client.event
async def on_ready():
    print("Start client as {}".format(client.user))

if __name__ == "__main__":
    client.run(token)
