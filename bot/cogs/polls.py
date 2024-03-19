
import nextcord
from nextcord.ext import commands


from bot.databases import localdb
from bot.misc.lordbot import LordBot

db = localdb.get_table('polls')
alphabet = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯',
            '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇽', '🇾', '🇿']


class CreatePoll(nextcord.ui.Modal):
    def __init__(self) -> None:
        super().__init__("Create pool", timeout=300)

        self.question = nextcord.ui.TextInput(
            label='Question',
            placeholder='Write a question',
            max_length=100
        )
        self.choices = nextcord.ui.TextInput(
            label='Choices',
            placeholder='Write the options of choice through the line each',
            style=nextcord.TextInputStyle.paragraph
        )
        self.description = nextcord.ui.TextInput(
            label='Description',
            style=nextcord.TextInputStyle.paragraph,
            required=False,
            max_length=1500
        )

        self.add_item(self.question)
        self.add_item(self.choices)
        self.add_item(self.description)

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer()

        question = self.question.value
        choices = self.choices.value.split('\n')[:len(alphabet)]
        sketch = self.description.value

        if 1 >= len(choices):
            await interaction.followup.send(content=(
                "There must be more than 1 choice option\n"
                "To specify more options, move the line"
            ), ephemeral=True)
            return

        description = '\n'.join(
            [f'* {alphabet[num]} `{choice}`' for num, choice in enumerate(choices)])

        embed = nextcord.Embed(
            title=question,
            description=description,
            color=0xffba08
        )
        if sketch:
            embed.add_field(name='Description:', value=sketch)

        message = await interaction.channel.send(embed=embed)

        for serial, _ in enumerate(choices):
            await message.add_reaction(alphabet[serial])

        poll_data = {
            'title': question,
            'sketch': sketch,
            'user_id': interaction.user.id,
            'options': choices,
        }
        db[message.id] = poll_data


class Polls(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot

    @nextcord.slash_command(name="poll", guild_ids=[1179069504186232852])
    async def poll(self, interaction: nextcord.Interaction):
        await interaction.response.send_modal(CreatePoll())

    @nextcord.message_command("Finish Poll", guild_ids=[1179069504186232852])
    async def finish_poll(self, interaction: nextcord.Interaction, message: nextcord.Message):
        await interaction.response.defer(ephemeral=True, with_message=False)

        poll_data: dict = db.get(message.id)

        user_id = poll_data.get('user_id')
        title = poll_data.get('title')
        options = poll_data.get('options')

        if not interaction.user.id == user_id:
            await interaction.edit_original_message(content=("This is not your survey.\n"
                                                             "You do not have the right to complete this vote!"))
            return

        general_count = sum(
            [react.count for react in message.reactions], start=-len(message.reactions))
        text = ''
        for num, react in enumerate(message.reactions):
            text += f'* **{(0 if general_count == 0 else (react.count-1)/general_count) * 100 :.0f}%**  |  {alphabet[num]} `{options[num]}`\n'

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
