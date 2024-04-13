
import asyncio
import time
import nextcord
from nextcord.ext import commands

from bot.databases import localdb
from bot.databases.handlers.guildHD import GuildDateBases
from bot.misc.lordbot import LordBot
from bot.misc.time_transformer import display_time
from bot.misc.utils import calculate_time

REMINDER_DB = localdb.get_table('')


class Reminder(commands.Cog):
    def __init__(self, bot: LordBot):
        self.bot = bot

    @commands.command()
    async def reminder(self, ctx: commands.Context, time_now: calculate_time, *, text: str) -> None:
        self.bot.loop.call_later(
            time_now, asyncio.create_task, self.process_reminder(time.time(), ctx.channel, text))
        await ctx.send(f"🛎️ OK, I'll mention you here on <t:{time.time() + time_now :.0f}:f>(<t:{time.time() + time_now :.0f}:R>)")

    async def process_reminder(self, time_old: float, channel: nextcord.TextChannel, text: str) -> None:
        gdb = GuildDateBases(channel.guild.id)
        color = gdb.get('color')
        embed = nextcord.Embed(
            title="🛎️ Reminder",
            description=f"{display_time(time.time()-time_old)} ago you asked me to remind you",
            color=color
        )
        embed.add_field(
            name="Remind",
            value=text
        )

        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Reminder(bot))
