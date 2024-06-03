import nextcord
from nextcord.ext import commands

from bot.databases import GuildDateBases
from bot.misc import utils

import googletrans

from bot.misc.lordbot import LordBot

translator = googletrans.Translator()


class ThreadEvent(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_thread_create(self, thread: nextcord.Thread):
        guild_data = GuildDateBases(thread.guild.id)
        afm = await guild_data.get('thread_messages')
        thread_data = afm.get(thread.parent_id)

        if not thread_data:
            return

        content = await utils.generate_message(thread_data)
        await thread.send(**content)


def setup(bot):
    bot.add_cog(ThreadEvent(bot))
