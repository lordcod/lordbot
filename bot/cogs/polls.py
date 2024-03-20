
import nextcord
from nextcord.ext import commands


from bot.databases import localdb
from bot.misc.lordbot import LordBot
from bot.views.create_poll import CreatePoll

db = localdb.get_table('polls')
alphabet = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯',
            '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹',
            '🇺', '🇻', '🇼', '🇽', '🇾', '🇿']


class Polls(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot

    @nextcord.slash_command(name="poll", guild_ids=[1179069504186232852])
    async def poll(self, interaction: nextcord.Interaction):
        await interaction.response.send_modal(CreatePoll())

    @nextcord.message_command("Finish Poll", guild_ids=[1179069504186232852])
    async def finish_poll(self, interaction: nextcord.Interaction, message: nextcord.Message):
        await interaction.response.defer(ephemeral=True, with_message=False)

        poll_data: dict = db.get(message.id, {})

        user_id = poll_data.get('user_id')
        title = poll_data.get('title')
        options = poll_data.get('options')

        if not interaction.user.id == user_id:
            await interaction.edit_original_message(content=("This is not your survey.\n"
                                                             "You do not have the right to complete this vote!"))
            return

        total_count = sum(
            [react.count for react in message.reactions], start=-len(message.reactions))
        text = ''
        for num, opt in enumerate(options):
            percent = (0 if total_count == 0 else (
                message.reactions[num])/total_count) * 100
            text += f'* **{percent :.0f}%**  |  {alphabet[num]} `{opt}`\n'

        embed = nextcord.Embed(
            title=title,
            description=text,
            color=0xffba08,
            timestamp=interaction.created_at
        )
        embed.set_footer(text="The voting has been completed!")

        await message.edit(embed=embed)
        await interaction.edit_original_message(content="The voting has been completed successfully!")


def setup(bot):
    cog = Polls(bot)

    bot.add_cog(cog)
