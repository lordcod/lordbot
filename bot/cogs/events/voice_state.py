
import time
import nextcord
from nextcord.ext import commands

from bot.databases import localdb
from bot.misc.lordbot import LordBot


VOICE_STATE_DB = localdb.get_table('voice_state')
SCORE_STATE_DB = localdb.get_table('score')
TEMP_VOICE_STATE_DB = {}


class voice_state_event(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState) -> None:
        if before.channel is None and after.channel is not None:
            await self.connect_to_voice(member)
        if before.channel is not None and after.channel is None:
            await self.disconnect_from_voice(member)

    async def connect_to_voice(self, member: nextcord.Member) -> None:
        TEMP_VOICE_STATE_DB[member.id] = time.time()

    async def disconnect_from_voice(self, member: nextcord.Member) -> None:
        member_started_at = TEMP_VOICE_STATE_DB.get(member.id)

        if member_started_at is None:
            return

        voice_time = time.time()-member_started_at
        total_voice_time = VOICE_STATE_DB.get(member.id, 0)

        VOICE_STATE_DB[member.id] = total_voice_time+voice_time

        await self.give_score(member, voice_time)

    async def give_score(self, member: nextcord.Member, voice_time: float) -> None:
        multiplier = 0.1
        user_level = 1

        SCORE_STATE_DB.setdefault(member.id, 0)
        SCORE_STATE_DB[member.id] += voice_time * 0.5 * multiplier / user_level

        print(
            f"Current exp is {SCORE_STATE_DB[member.id]}")


def setup(bot):
    bot.add_cog(voice_state_event(bot))
