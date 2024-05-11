import re
import nextcord
from nextcord.ext import commands

from bot.databases import localdb
from bot.databases.handlers.guildHD import GuildDateBases
from bot.misc.lordbot import LordBot

CONFESSIONS_STATE_DB = localdb.get_table('confessions')
GUILD_CONFESSIONS_DATA = {
    'channel_id': 1238802130702438491,
    'role_moderator_ids': [],
}


class Confessions(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot

    @nextcord.slash_command(guild_ids=[1179069504186232852])
    async def confessions(self, interaction: nextcord.Interaction):
        pass

    @confessions.subcommand(name='create')
    async def confessions_create(
        self,
        interaction: nextcord.Interaction,
        confession: str = nextcord.SlashOption(),
        user: nextcord.Member = nextcord.SlashOption(required=False),
        attachment: nextcord.Attachment = nextcord.SlashOption(required=False)
    ):
        gdb = GuildDateBases(interaction.guild_id)
        color = gdb.get('color')
        channel_id = GUILD_CONFESSIONS_DATA['channel_id']
        channel = interaction.guild.get_channel(channel_id)

        if user is None:
            content = 'A new anonymous message has been received'
        else:
            content = f'A new anonymous message sent to the {user.mention} has been received'

        embed = nextcord.Embed(
            title='Confession',
            description=confession,
            color=color
        )
        if attachment:
            embed.set_image(attachment.url)

        message = await channel.send(content, embed=embed)

        CONFESSIONS_STATE_DB[message.id] = {
            'author_id': interaction.user.id,
            'confession': confession,
            'user_id': user.id,
            'attachment_url': attachment.url
        }

    @confessions.subcommand(name='report')
    async def confessions_report(
        self,
        interaction: nextcord.Interaction,
        message: str
    ):
        if match := re.fullmatch(r'(https:\/\/discord.com\/channels\/\d+\/\d+\/)?(\d+)', message):
            message_id = match.group(2)
        else:
            return
        data = CONFESSIONS_STATE_DB.get(message_id)
        # TODO LOGS CONFESSIONS

    @confessions.subcommand(name='block')
    async def confessions_block(self, interaction: nextcord.Interaction):
        # TODO LOGS CONFESSIONS


def setup(bot):
    bot.add_cog(Confessions(bot))
