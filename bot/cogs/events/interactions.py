import nextcord
import asyncio
from nextcord.ext import commands

from bot.databases import GuildDateBases
from bot.misc.lordbot import LordBot


class InteractionsEvent(commands.Cog):
    def __init__(self, bot: LordBot) -> None:
        self.bot = bot
        bot.set_event(self.on_interaction)
        super().__init__()

    async def dis_interaction_failed(self, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        color = gdb.get('color')

        if interaction.type not in {2, 3, 5}:
            return

        await asyncio.sleep(2.5-self.bot.latency)
        if interaction.response.is_done():
            return

        embed = nextcord.Embed(
            title="The interaction time has expired",
            description="If you need to use the interaction, call the associated command",
            color=color
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def on_interaction(self, interaction: nextcord.Interaction):
        await self.bot.process_application_commands(interaction)


def setup(bot):
    bot.add_cog(InteractionsEvent(bot))
