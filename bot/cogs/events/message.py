import asyncio
import random
import time
import nextcord
import math
from nextcord.ext import commands

from bot.databases import GuildDateBases, localdb
from bot.misc.lordbot import LordBot
from bot.languages import i18n

import googletrans

translator = googletrans.Translator()

MESSAGE_STATE_DB = localdb.get_table('messages')
SCORE_STATE_DB = localdb.get_table('score')
BETWEEN_MESSAGES_TIME = {}
LAST_MESSAGES_USER = {}


class MessageEvent(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.guild is None:
            return
        await asyncio.gather(
            self.add_reactions(message),
            self.process_mention(message),
            self.give_score(message),
            self.give_message_score(message)
        )

    async def add_reactions(self, message: nextcord.Message) -> None:
        gdb = GuildDateBases(message.guild.id)

        if (reactions := gdb.get('reactions')) and (data_reactions := reactions.get(message.channel.id)):
            for reat in data_reactions:
                try:
                    asyncio.create_task(message.add_reaction(reat))
                except nextcord.HTTPException:
                    break

    async def process_mention(self, message: nextcord.Message) -> None:
        gdb = GuildDateBases(message.guild.id)

        color = gdb.get('color')
        locale = gdb.get('language')
        prefix = gdb.get('prefix')

        if message.content.strip() == self.bot.user.mention:
            embed = nextcord.Embed(
                title=i18n.t(locale, 'bot-info.title',
                             name=self.bot.user.display_name),
                description=i18n.t(locale, 'bot-info.description'),
                color=color
            )
            embed.add_field(
                name=i18n.t(locale, 'bot-info.info-server'),
                value=i18n.t(locale, 'bot-info.prefix-server', prefix=prefix)
            )

            asyncio.create_task(message.channel.send(embed=embed))

    async def give_message_score(self, message: nextcord.Message) -> None:
        MESSAGE_STATE_DB.setdefault(message.author.id, 0)
        MESSAGE_STATE_DB[message.author.id] += 1
        
        print(
            f"{message.author.display_name} M Current count message is {MESSAGE_STATE_DB[message.author.id]}")

    async def give_score(self, message: nextcord.Message) -> None:
        if message.author.bot:
            return
        lmu = LAST_MESSAGES_USER.get(
            f"{message.guild.id}:{message.channel.id}")
        LAST_MESSAGES_USER[f"{message.guild.id}:{message.channel.id}"] = message.author.id
        if lmu == message.author.id and BETWEEN_MESSAGES_TIME.get(message.author.id, 0) > time.time():
            return

        multiplier = 1
        user_level = 1

        SCORE_STATE_DB.setdefault(message.author.id, 0)
        SCORE_STATE_DB[message.author.id] += random.randint(
            0, 10) * multiplier / math.sqrt(user_level)
        BETWEEN_MESSAGES_TIME[message.author.id] = time.time() + 10

        print(
            f"{message.author.display_name} M Current score is {SCORE_STATE_DB[message.author.id]}")


def setup(bot):
    bot.add_cog(MessageEvent(bot))
