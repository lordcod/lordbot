
import time
import nextcord
from nextcord.ext import commands

from bot.databases import localdb
from bot.databases.handlers.guildHD import GuildDateBases
from bot.misc.lordbot import LordBot
from bot.misc.time_transformer import display_time
from bot.misc.utils import translate_to_timestamp, randquan


REMINDER_DB = localdb.get_table('')


class Reminder(commands.Cog):
    def __init__(self, bot: LordBot):
        self.bot = bot

    @commands.command()
    async def reminder(self, ctx: commands.Context, time_now: translate_to_timestamp, *, text: str) -> None:
        if time.time() > time_now:
            await ctx.send("You must specify a time that is later than the current time.")
            return
        self.bot.lord_handler_timer.create_timer_handler(
            time_now-time.time(),
            self.process_reminder(time.time(), ctx.author, ctx.channel, text),
            f"reminder:{ctx.guild.id}:{ctx.guild.id}:{time_now :.0f}:{randquan(17)}"
        )
        await ctx.send(f"🛎️ OK, I'll mention you here on <t:{time_now :.0f}:f>(<t:{time_now :.0f}:R>)")

    async def process_reminder(self, time_old: float, member: nextcord.Member, channel: nextcord.TextChannel, text: str) -> None:
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

        await channel.send(member.mention, embed=embed)


def setup(bot):
    bot.add_cog(Reminder(bot))
