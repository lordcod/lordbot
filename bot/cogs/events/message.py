import nextcord
from nextcord.ext import commands

from bot.databases import GuildDateBases
from bot.misc.lordbot import LordBot
from bot.languages import i18n

import googletrans

translator = googletrans.Translator()


class message_event(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.guild is None:
            return

        gdb = GuildDateBases(message.guild.id)

        color = gdb.get('color')
        locale = gdb.get('language')
        prefix = gdb.get('prefix')

        reactions: dict = gdb.get('reactions')

        data_reactions = reactions.get(message.channel.id)

        if data_reactions:
            for reat in data_reactions:
                try:
                    await message.add_reaction(reat)
                except nextcord.HTTPException:
                    break

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

            await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(message_event(bot))
