import nextcord
from nextcord.ext import commands, ipc

from os import environ

token = environ["lordkind_token"]

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ipc = ipc.Server(self, host="192.168.1.15", secret_key="my_secret_key")  # create our IPC Server

    async def on_ready(self):
        """Called upon the READY event"""
        print(f"{[g.id for g in self.guilds]}")
        print("Bot is ready.")

    async def on_ipc_ready(self):
        """Called upon the IPC Server being ready"""
        print("Ipc is ready.")

    async def on_ipc_error(self, endpoint, error):
        """Called upon an error being raised within an IPC route"""
        print(endpoint, "raised", error)


my_bot = MyBot(command_prefix="!", intents=nextcord.Intents.all())


@my_bot.ipc.route()
async def get_member_count(data):
    guild = my_bot.get_guild(data.guild_id)  # get the guild object using parsed guild_id
    
    return guild.member_count  # return the member count to the client


if __name__ == "__main__":
    my_bot.ipc.start()  # start the IPC Server
    my_bot.run(token)