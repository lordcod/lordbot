

import nextcord
from nextcord.ext import commands

from bot.misc.lordbot import LordBot
from bot.misc.tempchannels import TempChannels, TempChannelsDataBases, _guild_data


class voice_state_event(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: nextcord.Member,
        before: nextcord.VoiceState,
        after: nextcord.VoiceState
    ) -> None:
        self.member = member
        self.before = before
        self.after = after

        await self.process_create()
        await self.process_delete()

    async def process_create(self) -> None:
        if self.before.channel == self.after.channel or not (
            self.after.channel and
            self.after.channel.id == _guild_data.get('trigger_channel_id')
        ):
            return

        if channel_id := TempChannelsDataBases.get(self.member.guild.id, self.member.id):
            voice = self.member.guild.get_channel(channel_id)
            await self.member.move_to(voice)
            return

        await TempChannels.create(self.member.guild, self.member)

    async def process_delete(self) -> None:
        if not self.before.channel or len(self.before.channel.members) > 0:
            return
        await TempChannels(self.before.channel).delete()


def setup(bot):
    bot.add_cog(voice_state_event(bot))
