import nextcord
from nextcord.ext import commands

from bot.misc.lordbot import LordBot


class InteractionsEvent(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        bot.add_event(self.on_interaction)
        super().__init__()

    async def on_interaction(self, interaction: nextcord.Interaction):
        await self.bot.process_application_commands(interaction)


def setup(bot):
    bot.add_cog(InteractionsEvent(bot))
