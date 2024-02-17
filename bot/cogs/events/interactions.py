import nextcord
from nextcord.ext import commands

from bot.misc.lordbot import LordBot


class interactions_event(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        super().__init__()

        bot.event(self.on_interaction)

    async def on_interaction(self, interaction: nextcord.Interaction):
        await self.bot.process_application_commands(interaction)


def setup(bot):
    bot.add_cog(interactions_event(bot))
