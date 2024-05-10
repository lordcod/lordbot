import nextcord
from nextcord.ext import commands

from bot.databases import GuildDateBases
from bot.misc import logstool
from bot.misc.lordbot import LordBot
from bot.languages import i18n

import googletrans

translator = googletrans.Translator()


class message_event(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        self.bot
        super().__init__()

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
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

    @commands.Cog.listener()
    async def on_message_edit(self, before: nextcord.Message, after: nextcord.Message):
        await logstool.Logs(before.guild).edit_message(before, after)

    @commands.Cog.listener()
    async def on_message_delete(self, message: nextcord.Message):
        await logstool.pre_message_delete_log(message)

    @commands.Cog.listener()
    async def on_guild_audit_log_entry_create(self, entry: nextcord.AuditLogEntry):
        if entry.action != nextcord.AuditLogAction.message_delete:
            return
        await logstool.set_message_delete_audit_log(entry.user, entry.extra.channel.id, entry.target.id)


def setup(bot):
    bot.add_cog(message_event(bot))
