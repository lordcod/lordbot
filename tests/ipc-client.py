import asyncio
from nextcord.ext import ipc


async def main():
    ipc_client = ipc.Client(host="192.168.1.15", secret_key="my_secret_key")

    await asyncio.sleep(5)

    member_count = await ipc_client.request("get_member_count", guild_id=1165681101294030898)
    print(member_count)

    await asyncio.sleep(5)

    await ipc_client.session.close()


if __name__ == "__main__":
    asyncio.run(main())
