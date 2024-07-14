
import asyncio
import time
import math
import nextcord
from nextcord.ext import commands

from bot.databases import localdb
from bot.misc.lordbot import LordBot
from bot.misc.music import current_players
from bot.misc.tempvoice import TempVoiceModule


class VoiceStateEvent(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: nextcord.Member, before: nextcord.VoiceState, after: nextcord.VoiceState) -> None:
        if before.channel is None and after.channel is not None:
            await asyncio.gather(
                TempVoiceModule.connect_voice(member, after.channel),
                self.connect_to_voice(member)
            )
        if before.channel is not None and after.channel is None:
            await asyncio.gather(
                TempVoiceModule.disconnect_voice(member, before.channel),
                self.disconnect_from_voice(member),
                self.check_bot_player(before.channel)
            )

    async def check_bot_player(self, channel: nextcord.VoiceChannel):
        if (1 == len(channel.members)
            and self.bot.user == channel.members[0]
                and channel.guild.id in current_players):
            await current_players[channel.guild.id].point_not_user()

    async def connect_to_voice(self, member: nextcord.Member) -> None:
        state = await localdb.get_table('temp_voice_state')
        await state.set(member.id, time.time())

    async def disconnect_from_voice(self, member: nextcord.Member) -> None:
        state = await localdb.get_table('voice_state')
        temp_state = await localdb.get_table('temp_voice_state')
        member_started_at = await temp_state.get(member.id)
        await temp_state.delete(member.id)

        if member_started_at is None:
            return

        voice_time = time.time()-member_started_at
        await state.increment(member.id, voice_time)

        await self.give_score(member, voice_time)

    async def give_score(self, member: nextcord.Member, voice_time: float) -> None:
        state = await localdb.get_table('score')

        multiplier = 1
        user_level = 1

        await state.increment(member.id, voice_time * 0.5
                              * multiplier / math.sqrt(user_level))


def setup(bot: LordBot):
    bot.add_cog(VoiceStateEvent(bot))
