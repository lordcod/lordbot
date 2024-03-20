
import time
import nextcord
from nextcord.ext import commands

from bot.databases import localdb
from bot.misc.lordbot import LordBot


VOICE_STATE_DB = localdb.get_table('voice_state')
EXP_STATE_DB = localdb.get_table('exps')
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

        await self.give_exp(member, voice_time)

    async def give_exp(self, member: nextcord.Member, voice_time: float) -> None:
        print(
            f"Give {voice_time * EXP_STATE_DB.get(member.id, 0) * 0.5} exp")
        EXP_STATE_DB[member.id] = voice_time * \
            EXP_STATE_DB.get(member.id, 0) * 0.5


def setup(bot):
    bot.add_cog(voice_state_event(bot))
