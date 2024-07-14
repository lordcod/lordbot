import asyncio
import logging
import nextcord
import os

token = os.environ.get("lordclassic_token")

logging.basicConfig(level=logging.INFO)
client = nextcord.Client(intents=nextcord.Intents.all())


@client.event
async def on_member_join(member: nextcord.Member):
    role = member.guild.get_role(1178294479283814421)
    await member.add_roles(role)


@client.event
async def on_ready():
    print('Start')
    guild = client.get_guild(1178294479267045466)
    role = guild.get_role(1178294479283814421)
    tasks = []
    async for member in guild.fetch_members(limit=None):
        if role not in member.roles:
            tasks.append(member.add_roles(role))
    await asyncio.gather(*tasks)
    print('Ready', len(tasks), len(guild.members))


if __name__ == '__main__':
    print('run')
    client.run(token)
