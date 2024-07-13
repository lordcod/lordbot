import asyncio
import logging
import time
import nextcord
from nextcord.ext import commands
from bot.databases import localdb
from bot.misc.lordbot import LordBot
from bot.misc.time_transformer import display_time


_log = logging.getLogger(__name__)


class PresenceEvent(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        super().__init__()

    async def _update_presence(self, user_id: int, time_now: int):
        presence_db = await localdb.get_table('presence_db')
        exists = await presence_db.exists(user_id)
        if not exists:
            await presence_db.set(user_id, time_now)

    async def _delete_presence(self, user_id: int, time_now: int):
        presence_db = await localdb.get_table('presence_db')
        online_db = await localdb.get_table('online_db')
        time_now = await presence_db.get(user_id)
        await presence_db.delete(user_id)
        online_time = time_now-time_now
        await online_db.increment(user_id, online_time)

    @commands.Cog.listener()
    async def on_ready(self):
        time_now = time.time()
        tasks = []
        for user in self.bot.get_all_members():
            if user.status == 'offline':
                tasks.append(self._update_presence(user.id, time_now))
            else:
                tasks.append(self._update_presence(user.id, time_now))
        await asyncio.gather(*tasks)

    @commands.command()
    async def userinfo(self, ctx: commands.Context, member: nextcord.Member):
        return
        device = self.get_device_status(member)

        embed = nextcord.Embed(color=2829617)
        embed.set_author(name=f'Information about {member.display_name} ({member.name})',
                         icon_url=member.display_avatar)
        embed.description = (
            f"User id: {member.id}\n"
            f"Badges: missing\n"
            f"Created: {format_dt(member.created_at, 'D')} ({format_dt(member.created_at, 'R')})\n"
            f"Joined: {format_dt(member.joined_at, 'D')} ({format_dt(member.joined_at, 'R')})\n"
            f"Voice time: 20 minutes\n"
            f"Message count: {random.randint(80, 120)}\n"
            f"Status: <:online:1260211416212963349> online\n"
            f"Device: {device}\n"
            f"Online time: 2 hours\n"
            f"Permission: Administrator"
        )
        if roles := [role.mention for role in reversed(member.roles) if role != member.guild.default_role]:
            embed.add_field(
                name='Roles',
                value=' • '.join(roles)
            )
        embed.set_thumbnail(member.display_avatar)
        embed.set_image(member.banner)

        await ctx.send(embed=embed)

    def get_device_status(self, member: nextcord.Member):
        status_list = ["mobile", "desktop", "web"]
        for status in status_list:
            if member._client_status.get(status):
                return status
        return "offline"

    @commands.Cog.listener()
    async def on_presence_update(self, before: nextcord.Member, after: nextcord.Member):
        if before.status == after.status:
            return

        online_db = await localdb.get_table('online_db')
        presence_db = await localdb.get_table('presence_db')

        embed = None
        exists = await presence_db.exists(after.id)

        if after.status == 'offline' and exists:
            time_now = await presence_db.get(after.id)
            await presence_db.delete(after.id)
            online_time = time.time()-time_now
            await online_db.increment(after.id, online_time)

            embed = nextcord.Embed(
                title="The status has changed",
                color=2829617,
                description=(
                    f"User: {after.name} ({after.id})\n"
                    f"Online time: {display_time(online_time)}\n"
                    f"Status: {after.status}"
                )
            )
        if after.status != 'offline' and not exists:
            await presence_db.set(after.id, time.time())

            embed = nextcord.Embed(
                title="The status has changed",
                color=2829617,
                description=(
                    f"User: {after.name} ({after.id})\n"
                    f"Status: {after.status}\n"
                    f"Device: {self.get_device_status(after)}"
                )
            )

        if embed is not None:
            channel = self.bot.get_channel(1210578994726969384)
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(PresenceEvent(bot))
